from pydantic import BaseModel


class MetricsResponse(BaseModel):
    total_orders: int
    avg_processing_time: float
    pending_orders: int
    processing_orders: int
    completed_orders: int