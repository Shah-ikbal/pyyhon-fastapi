import uuid
from fastapi import APIRouter
from models.order_models import OrderCreate

from services.orders_svc import create_order, get_all_orders, get_order_status


router = APIRouter()

@router.post("/create-order")
async def create_orders(order: OrderCreate):
    return await create_order(order)

@router.get("/all-orders")
async def get_orders():
    return await get_all_orders()

@router.get("/order-status/{order_id}")
async def get_status(order_id: uuid.UUID):
    return await get_order_status(order_id)