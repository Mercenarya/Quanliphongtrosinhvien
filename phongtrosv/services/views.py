from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from django.template import loader
from django.views.decorators.csrf import csrf_exempt #skip csrf của react để tương tác API
from django.views.decorators.http import require_http_methods
from asgiref.sync import sync_to_async
import json
# import asyncio
import os
import sys

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
 
from .models import Contract, Room  # đổi lại đường dẫn import cho đúng project
from datetime import date


'''thêm hợp đồng mới vào dữ liệu'''
@require_http_methods(['POST'])
def add_new_contracts(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            
            contract_id = str(data.get("contract_id", "")).strip().upper()
            room_id = str(data.get("room_id", "")).strip()
            tenant_name = str(data.get("tenant_name", "")).strip()
            tenant_id_card = str(data.get("tenant_id_card", "")).strip()
            duration = str(data.get("duration_months", "")).strip()
            
            '''kiểm tra tồn tại'''
            with transaction.atomic():
                room = Room.objects.select_for_update().filter(pk=room_id).first() #records ưu tiên 
                if room is None:
                    return JsonResponse({"error": "Phòng không tồn tại."}, status=404)
                
                if room.status != Room.FREE:
                    return JsonResponse({"error": "Phòng này đã được thuê."}, status=409)

                contract = Contract.objects.create(
                    id=contract_id,
                    room=room,
                    tenant_name=tenant_name,
                    tenant_id_card=tenant_id_card,
                    contract_date=date.today(),  # luôn là ngày hiện tại
                    duration_months=int(duration),
                )
                room.status = Room.RENTED
                room.save(update_fields=["status"])
                
            # trả về kết quả hợp lệ thành công
            return JsonResponse(
            {
                "message": "Added Contract.",
                "data": {
                    "contract":{
                        "id": contract.id,
                        "room_id": room.id,
                        "tenant_name": contract.tenant_name,
                        "contract_date": contract.contract_date.strftime("%d/%m/%Y"),
                        "duration_months": contract.duration_months,
                        "total_price": room.price * contract.duration_months,
                    }
                },
            },
            status=201,
        )
            
    except Exception as error:
        return JsonResponse(
            {
                "error":"An error occured during adding new contract",
                "details":f"{error}"
            },status=500
        )


'''Xoá hợp đông thuê '''
@require_http_methods(['DELETE'])
def delete_contracts(request,contract_id):
    try:
        if request.method == "POST":
            # data = json.load(request.body)
                
            
            # lỗi load dữ liệu contract id từ body json (Fetch từ JS)
            if not contract_id:
                return JsonResponse(
                    {
                        "error":"Cannot get contract information",
                        
                    },status = 500
                )
            
            
            with transaction.atomic():
                contract = (
                    Contract.objects.select_related("room")
                    .select_for_update()
                    .filter(pk=contract_id)
                    .first()
                )
                if contract is None:
                    return JsonResponse({"error": "contract doesnt exists yet."}, status=404)
    
                room = contract.room
                contract.delete()
                room.status = Room.FREE
                room.save(update_fields=["status"])
    
            return JsonResponse(
                {
                    "data":{
                        "message": f"Already deleted {contract_id}.",
                        "room_id": room.id
                    }
                },
                status=200,
            )
            
    except Exception as error:
        return JsonResponse(
            {
                "error":"An error occured during deleting contract",
                "details":f"{error}"
            },status=500
        )


'''Hiển thị danh sách hợp đồng cho thuê'''
@require_http_methods(["GET"])
def view_list_contracts(request):
    try:
        # select_related lấy luôn phòng trong 1 câu truy vấn 
        contracts = Contract.objects.select_related("room").order_by("id") # sắp xếp theo ID
        '''
        SELECT * FROM Room 
        '''
        
 
        data = [
            {
                "id": c.id,
                "room_id": c.room_id,
                "tenant_name": c.tenant_name,
                "contract_date": c.contract_date.strftime("%d/%m/%Y"),
                "duration_months": c.duration_months,
                "total_price": c.room.price * c.duration_months, # tom
            }
            # truy vấn danh sách (SELECT * FROM contract )
            for c in contracts
        ]
 
        return JsonResponse(
            {
                "data":{
                    "contracts": data,
                    "count": len(data)
                }
            }, status=200)
 
    except Exception as error:
        return JsonResponse(
            {
                "error": "An error occured during review list of contracts",
                "details": f"{error}",
            },
            status=500,
        )
        
        
@require_http_methods(["GET"])
def view_list_rooms(request):
 
    try:
        rooms = Room.objects.order_by("id")
        if request.GET.get("status") == "free":
            rooms = rooms.filter(status=Room.FREE)
 
        data = [
            {"id": r.id, "name": r.name, "area": r.area, "price": r.price, "status": r.status}
            for r in rooms
        ]
        return JsonResponse(
            {
                "data":{
                    "rooms": data,
                    "count": len(data)
                }
             
            }, status=200)
 
    except Exception as error:
        return JsonResponse(
            {"error": "An error occured during review list of rooms", "details": f"{error}"},
            status=500,
        )