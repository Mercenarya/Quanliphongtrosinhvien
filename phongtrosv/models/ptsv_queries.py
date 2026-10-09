from django.db import models
from django.db import transaction

import os,sys

CURRENT = os.getcwd()
ROOT = os.path.join(CURRENT,"..")
sys.path.append(ROOT)

from services.models import Room, Contract

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

def delete_contracts_records(contract_id):
    try:
        with transaction.atomic():
            contract_data = {
                Contract.objects.select_related("room")
                .select_for_update()
                .filter(pk=contract_id).first()
            }
            if contract_data is None:
                return {
                    "message":f"Contract {contract_id} doesn't exists yet"
                }
                
            room = contract_data.room
            contract_data.delete()
            room.status = Room.FREE
            room.save(update_fields=['status'])
            return {
                "message":f"Already deleted {contract_id}."
            }
            
    except Exception as error:
        return error


def add_new_contract():
    pass

def update_contract():
    pass

def view_contract_details():
    pass