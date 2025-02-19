import queue
import uuid
from fastapi import HTTPException
from databases.postgresdb import get_db_connection, release_db_connection
from models.order_models import OrderCreate, OrderStatus
from utils.shared import order_queue

# order_queue = queue.Queue()


async def create_order(order: OrderCreate):
    conn = await get_db_connection()
    try:
        # Generate a UUID for the order
        order_id = uuid.uuid4()
        print(order_id)
        # Insert the new order with UUID
        await conn.execute(
            "INSERT INTO orders (order_id, user_id, item_ids, total_amount, status) VALUES ($1, $2, $3, $4, 'Pending')",
            order_id,
            order.user_id,
            order.item_ids,
            order.total_amount,
        )

        # Add the order to the processing queue
        order_queue.put(order_id)

        return {"order_id": order_id, "status": "Pending"}
    finally:
        await release_db_connection(conn)


async def get_all_orders():
    conn = await get_db_connection()
    try:
        order = await conn.fetch("SELECT order_id, status FROM orders")
        if not order:
            raise HTTPException(status_code=404, detail="Orders not found")
        return [
            OrderStatus(order_id=order["order_id"], status=order["status"])
            for order in order
        ]
    finally:
        await release_db_connection(conn)


async def get_order_status(order_id: uuid.UUID):
    conn = await get_db_connection()
    try:
        order = await conn.fetchrow(
            "SELECT order_id, status FROM orders WHERE order_id = $1", order_id
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"order_id": order["order_id"], "status": order["status"]}
    finally:
        await release_db_connection(conn)
