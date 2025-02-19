from typing import List
import uuid
from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    item_ids: List[int]  # Array of integers
    total_amount: float


class OrderStatus(BaseModel):
    order_id: uuid.UUID  # Use UUID instead of int
    status: str