from fastapi import APIRouter
from routes.orders import router as orders_router
from routes.metrics import router as metrics_router

routes = APIRouter()

routes.include_router(
    orders_router,
    prefix="/api/v1/orders",
    tags=["orders-api"],
    responses={418: {"description": "responsible for creating and quering orders"}},
)

routes.include_router(
    metrics_router,
    prefix="/api/v1/metrics",
    tags=["metrics-api"],
    responses={418: {"description": "responsible for getting metrics"}},
)
