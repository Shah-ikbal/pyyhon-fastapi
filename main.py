from fastapi import FastAPI
from databases.postgresdb import (
    create_orders_table_if_not_exists,
    populate_sample_data,
)
from utils.queue_processor import process_orders
import asyncio
from routes.routes import routes
from utils.shared import order_queue


app = FastAPI()

app.include_router(routes)


# Create the orders table and enable UUID extension on startup
# Start the process_orders task as a background task when the application starts:
@app.on_event("startup")
async def createTable():
    await create_orders_table_if_not_exists()
    # Uncomment this inorder to populate sample data
    # await populate_sample_data()
    asyncio.create_task(process_orders(order_queue))


@app.get("/")
async def root():
    return {"message": "Order System is running!"}
