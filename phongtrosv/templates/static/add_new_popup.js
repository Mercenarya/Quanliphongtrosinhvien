const FREE = 'Chưa được thuê', RENTED = 'Đã được thuê';

// Dữ liệu mẫu, thay bằng dữ liệu lấy từ database (API) của bạn
// const rooms = [
//     { id: 'P101', name: 'Phòng 101', area: 20, price: 3000000, status: RENTED },
//     { id: 'P102', name: 'Phòng 102', area: 25, price: 3500000, status: FREE },
//     { id: 'P203', name: 'Phòng 203', area: 30, price: 3500000, status: RENTED },
//     { id: 'P204', name: 'Phòng 204', area: 22, price: 3200000, status: FREE },
//     { id: 'P305', name: 'Phòng 305', area: 28, price: 3500000, status: RENTED }
// ];
// const contracts = [
//     { id: 'HD-0001', roomId: 'P101', tenant: 'Nguyễn Văn An', idCard: '012345678901', date: '01/09/2026', months: 6 },
//     { id: 'HD-0002', roomId: 'P203', tenant: 'Trần Thị Bình', idCard: '098765432109', date: '15/09/2026', months: 12 },
//     { id: 'HD-0003', roomId: 'P305', tenant: 'Lê Hoàng Cường', idCard: '024681357911', date: '20/09/2026', months: 3 }
// ];

const money = n => n.toLocaleString('vi-VN') + ' đ';
const $ = id => document.getElementById(id);
const modal = new bootstrap.Modal($('contractModal'));

function todayStr() {
    const d = new Date();
    const p = n => String(n).padStart(2, '0');
    return `${p(d.getDate())}/${p(d.getMonth() + 1)}/${d.getFullYear()}`;
}

function render() {
    $('contractBody').innerHTML = contracts.map(c => {
        const room = rooms.find(r => r.id === c.roomId);
        return `<tr>
        <td>${c.id}</td><td>${c.roomId}</td><td>${c.tenant}</td>
        <td>${c.date}</td><td>${c.months} tháng</td>
        <td class="text-end">${money(room.price * c.months)}</td>
        <td class="text-center"><button type="button" class="btn btn-sm btn-outline-danger" data-del="${c.id}">Xoá</button></td>
      </tr>`;
    }).join('') || '<tr><td colspan="7" class="text-center text-muted">Chưa có hợp đồng nào.</td></tr>';

    $('roomBody').innerHTML = rooms.map(r => `<tr>
      <td>${r.id}</td><td>${r.name}</td><td>${r.area} m²</td>
      <td class="text-end">${money(r.price)}</td>
      <td><span class="badge text-bg-${r.status === FREE ? 'success' : 'danger'}">${r.status}</span></td>
    </tr>`).join('');
}

// Chỉ đưa các phòng chưa được thuê vào dropdown
function fillRoomOptions() {
    const free = rooms.filter(r => r.status === FREE);
    $('roomId').innerHTML = free.length
        ? '<option value="">-- Chọn phòng --</option>' +
        free.map(r => `<option value="${r.id}">${r.id} - ${r.name} (${money(r.price)}/tháng)</option>`).join('')
        : '<option value="">Không còn phòng trống</option>';
}

$('btnCreate').addEventListener('click', () => {
    $('contractForm').reset();
    $('contractForm').classList.remove('was-validated');
    $('contractId').setCustomValidity('');
    $('contractDate').value = todayStr();
    fillRoomOptions();
    modal.show();
});

// Chỉ cho nhập số ở ô CMND
$('tenantIdCard').addEventListener('input', e => e.target.value = e.target.value.replace(/\D/g, ''));

$('contractForm').addEventListener('submit', e => {
    e.preventDefault();
    const idInput = $('contractId');
    const id = idInput.value.trim().toUpperCase();

    // Kiểm tra định dạng HD-XXXX và trùng mã
    if (!/^HD-\d{4}$/.test(id)) {
        $('contractIdError').textContent = 'Mã hợp đồng phải có dạng HD-XXXX (X là số).';
        idInput.setCustomValidity('invalid');
    } else if (contracts.some(c => c.id === id)) {
        $('contractIdError').textContent = 'Mã hợp đồng đã tồn tại.';
        idInput.setCustomValidity('invalid');
    } else {
        idInput.setCustomValidity('');
    }

    // Ngày hợp đồng luôn là ngày hiện tại
    $('contractDate').value = todayStr();

    e.target.classList.add('was-validated');
    if (!e.target.checkValidity()) return;

    contracts.push({
        id,
        roomId: $('roomId').value,
        tenant: $('tenantName').value.trim(),
        idCard: $('tenantIdCard').value,
        date: $('contractDate').value,
        months: Number($('duration').value)
    });

    // Cập nhật tình trạng thuê: Chưa được thuê -> Đã được thuê
    rooms.find(r => r.id === $('roomId').value).status = RENTED;

    render();
    modal.hide();
});

// Xoá hợp đồng: trả phòng về "Chưa được thuê"
$('contractBody').addEventListener('click', e => {
    const id = e.target.dataset.del;
    if (!id || !confirm(`Xoá hợp đồng ${id}?`)) return;
    const i = contracts.findIndex(c => c.id === id);
    rooms.find(r => r.id === contracts[i].roomId).status = FREE;
    contracts.splice(i, 1);
    render();
});

render();