import uuid
from fastapi import APIRouter
from services.metrics_svc import get_metrics


router = APIRouter()


@router.get("/order-metrics")
async def get_status():
    return await get_metrics()