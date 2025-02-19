import asyncio
from databases.postgresdb import get_db_connection


async def process_order(order_id):
    conn = await get_db_connection()
    try:
        await conn.execute("UPDATE orders SET status = 'Processing' WHERE order_id = $1", order_id)
        await asyncio.sleep(5)
        await conn.execute("UPDATE orders SET status = 'Completed', updated_at = NOW() WHERE order_id = $1", order_id)
    finally:
        await conn.close()

async def process_orders(order_queue):
    while True:
        if not order_queue.empty():
            order_id = order_queue.get()
            asyncio.create_task(process_order(order_id))
        await asyncio.sleep(2)  # Sleep to avoid busy-waiting