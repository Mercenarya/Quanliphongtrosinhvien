from django.db import models


class Room(models.Model):
    FREE = "Chưa được thuê"
    RENTED = "Đã được thuê"

    id = models.CharField(max_length=10, primary_key=True)   # Mã phòng: P101
    name = models.CharField(max_length=100)
    area = models.IntegerField()
    price = models.IntegerField()                            # Giá thuê / tháng
    status = models.CharField(max_length=20, default=FREE)   # Tình trạng thuê

    def __str__(self):
        return self.id


class Contract(models.Model):
    id = models.CharField(max_length=7, primary_key=True)    # HD-0001
    room = models.ForeignKey(Room, on_delete=models.PROTECT)  # Khoá ngoại -> room_id
    tenant_name = models.CharField(max_length=150)
    tenant_id_card = models.CharField(max_length=12)
    contract_date = models.DateField()
    duration_months = models.IntegerField()                  # 3, 6 hoặc 12

    def __str__(self):
        return self.id


def seed_data():
    """Thêm dữ liệu mẫu. Chạy nhiều lần cũng không bị trùng (get_or_create)."""
    from datetime import date

    rooms = [
        ("P101", "Phòng 101", 20, 3000000, Room.RENTED),
        ("P102", "Phòng 102", 25, 3500000, Room.FREE),
        ("P203", "Phòng 203", 30, 3500000, Room.RENTED),
        ("P204", "Phòng 204", 22, 3200000, Room.FREE),
        ("P305", "Phòng 305", 28, 3500000, Room.RENTED),
    ]
    for id, name, area, price, status in rooms:
        Room.objects.get_or_create(
            id=id, defaults={"name": name, "area": area, "price": price, "status": status}
        )

    contracts = [
        ("HD-0001", "P101", "Nguyễn Văn An",  "012345678901", date(2026, 9, 1),  6),
        ("HD-0002", "P203", "Trần Thị Bình",  "098765432109", date(2026, 9, 15), 12),
        ("HD-0003", "P305", "Lê Hoàng Cường", "024681357911", date(2026, 9, 20), 3),
    ]
    for id, room_id, name, id_card, day, months in contracts:
        Contract.objects.get_or_create(
            id=id,
            defaults={
                "room_id": room_id,
                "tenant_name": name,
                "tenant_id_card": id_card,
                "contract_date": day,
                "duration_months": months,
            },
        )