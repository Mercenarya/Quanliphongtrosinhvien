# Giải thích các kiến thức web development

## 1. Khi nào dùng async/await

**Async/await** là cú pháp làm việc với Promise trong JavaScript (hoặc tương đương trong các ngôn ngữ như Python/C#) để viết mã không đồng bộ trở nên gần giống mã đồng bộ hơn.

### Khi nào nên dùng trong Django/Python:

- **I/O-bound operations** (độc립 với CPU, chờ đợi nguồn bên ngoài):
  - Truy vấn database (ngoài ORM sync)
  - Gọi API bên thứ 3 (payment gateway, social media, v.v.)
  - Đọc/ghi file hệ thống
  - Truy vấn cache (Redis, Memcached)
  - WebSocket connections

```python
# Django async view example (Django 3.1+)
import asyncio
from django.http import JsonResponse
import aiohttp

async def fetch_weather(request):
    # Giả sử chúng ta có một service API thời tiết bên ngoài
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.weather.com/data') as resp:
            data = await resp.json()
    return JsonResponse({'weather': data})
```

### Khi KHÔNG nên dùng:
- CPU-bound tasks (phức tạp tính toán, xử lý hình ảnh) - sẽ-block event loop
- Khi không có thực sự bất đồng bộ nào (sử dụng sync function trong async context)
- Over-engineering cho các thao tác đơn giản (truy vấn DB nhỏ wewnątrz jednej aplikacji)

**Lợi ích**: Tăng throughput cho ứng dụng web khi xử lý nhiều request cùng lúc (đặc biệt với I/O chờ đợi lâu), giảm resources consumption per request.

## 2. Tại sao một số trường hợp dùng method POST để xoá thay vì dùng Delete

Trong thiết kế REST API理想, chúng ta nên sử dụng:
- `DELETE /resources/{id}` để xóa một resource
- Tuy nhiên, trong thực tế có nhiều lý do khiến developers dùng `POST`:

### Lý do thực tế:

1. **Hạn chế của HTML forms**:
   - Các form HTML estándar chỉ hỗ trợ `GET` và `POST` (trước HTML5)
   - Không thể tạo form với `method="DELETE"` mà không dùng JavaScript
   - Giải pháp: Dùng `POST` với hidden field `_method=DELETE` (Django có hỗ trợ qua `django.middleware.csrf.CsrfViewMiddleware` và template tag `{% csrf_token %}` + xử lý trong view)

2. **Proxy/Firewall restrictions**:
   - Một số corporate proxy/chéo tường lửa chặn methods非凡 như `PUT`, `DELETE`, `PATCH` vì považъются за небезопасные
   - `POST` là method "an toàn" nhất được cho phép rộng rãi

3. **Idempotency concerns**:
   - `DELETE` nên là idempotent (gọi nhiều lần có cùng effect)
   - Nhưng trong một số logic nghiệp vụ, xóa có thể có side effects khác nhau tùy trạng thái (ví dụ: chỉ xóa khi chưa thanh toán, hoặc tạo log khác nhau)
   - Dùng `POST` cho phép biểu diễn hành động phức tạp hơn không thuần túy idempotent

4. **CSRF Protection**:
   - Trong Django, việc bảo vệ CSRF cho `DELETE` request mà không có JavaScript và tokens phức tạp
   - Nhiều dự án Django đơn giản hoá bằng cách dùng `POST` cho tất cả các thao tác thay đổi state (CREATE, UPDATE, DELETE) và bảo vệ bằng CSRF token chuẩn

5. **Khả năngCacheability**:
   - `POST` Responses thường không được cache bởi mặc định (an toàn hơn cho thao tác thay đổi state)
   - Mặc dù `DELETE` cũng không nên được cache, nhưng một số hệ thống có thể cấu hình sai

### Best practice trong Django:
- Dùng `POST` cho delete actions trong HTML forms (đơn giản, an toàn với CSRF)
- Dùng `DELETE`/`PUT`/`PATCH` cho API纯粹 (chỉ dùng bởi JavaScript/Mobile clients)
- Coi việc chuyển đổi method trong view nếu cần:
```python
# Trong Django view
def delete_item(request, item_id):
    if request.method == 'POST':
        # Xử lý logic xóa
        item = get_object_or_404(Item, pk=item_id)
        item.delete()
        return redirect('item-list')
    # GET request hiển thị form xác nhận
    return render(request, 'delete_confirm.html', {'item': item})
```

## 3. Danh sách các status code HTTP và ý nghĩa

HTTP status codes được chia thành 5 nhóm:

### 1xx: Informational (Thông tin)
- `100 Continue`: Server đã nhận được request headers, client nên gửi body
- `101 Switching Protocols`: Đang thay đổi protocol (WebSocket upgrade)

### 2xx: Success (Thành công)
- `200 OK`: Request thành công (GET, PUT, POST, etc.)
- `201 Created`: Resource mới đã được tạo (thường sau POST/PUT)
- `202 Accepted`: Request đã được chấp nhận để xử lý, nhưng chưa hoàn thành
- `204 No Content`: Request thành công nhưng không có content để trả về (thường dùng sau DELETE thành công)
- `206 Partial Content`: Partial response (dùng cho range requests, resumable downloads)

### 3xx: Redirection (Chuyển hướng)
- `301 Moved Permanently`: Resource đã vĩnh viễn chuyển tới URL mới (clients nên cập nhật bookmark)
- `302 Found` (temporary redirect): Resource tạm thời ở URL khác (POST method không đổi)
- `303 See Other`: Response có thể trovato ở另一 URL bằng GET (sau POST/PUT để tránh resubmit)
- `304 Not Modified`: Resource không đổi kể từ lần request trước (dùng cho caching)
- `307 Temporary Redirect`: Giống 302 nhưng giữ nguyên method và body
- `308 Permanent Redirect`: Giống 301 nhưng giữ nguyên method và body

### 4xx: Client Error (Lỗi phía client)
- `400 Bad Request`: Request không hợp lệ (syntax error, missing params, etc.)
- `401 Unauthorized`: Cần authentication (phải gửi credentials hợp lệ)
- `403 Forbidden`: Server hiểu request nhưng từ chối thực thi (không có quyền)
- `404 Not Found`: Resource không tồn tại tại URL đã cho
- `405 Method Not Allowed`: Method được sử dụng không được phép cho resource này
- `409 Conflict`: Request bị xung đột với trạng thái hiện tại của server (ví dụ: tạo duplicate)
- `429 Too Many Requests`: Vượt quá rate limit

### 5xx: Server Error (Lỗi phía server)
- `500 Internal Server Error`: Lỗi chung phía server (exception không xử lý được)
- `501 Not Implemented`: Server không biết how to thực hiện request
- `502 Bad Gateway**: Server làm gateway/proxy nhận được phản hồi invalid từ upstream
- `503 Service Unavailable**: Server tạm thời không thể xử lý requests (overload, maintenance)
- `504 Gateway Timeout**: Gateway không nhận được kịp thời phản hồi từ upstream

### Codes đặc biệt thường thấy trong entwickeln Django:
- `200`: Trang HTML bình thường, API response thành công
- `201`: Sau tạo object mới qua API (DRF thường trả về này sau POST)
- `204`: Sau DELETE thành công (không cần trả về data)
- `302`: Sau successful form submission (redirect để tránh F5 resubmit)
- `400`: Validation errors trong form/API
- `401`: View yêu cầu login nhưng user chưa auth
- `403`: User đã auth nhưng không có quyền truy cập view/resource này
- `404`: URL không tồn tại hoặc object không tìm thấy
- `405`: Gọi API với method sai (ví dụ: GET tới endpoint chỉ chấp nhận POST)
- `500`: Exception không được catch trong view (check logs!)
```

**Ghi chú**: Trong thực tế, codes `200`, `201`, `204`, `302`, `400`, `401`, `403`, `404`, `500` là những codes bạn sẽ gặp thường xuyên nhất khi phát triển ứng dụng web với Django.