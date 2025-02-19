import asyncpg
from dotenv import load_dotenv
import os
from .schema import CREATE_ORDERS_TABLE_QUERY, INSERT_DUMMY_RECORDS

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
DATABASE_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# Global connection pool
pool = None


async def get_db_connection():
    # Get an asynchronous database connection from the pool.
    global pool
    if pool is None:
        # Create a connection pool if it doesn't exist
        pool = await asyncpg.create_pool(
            min_size=5,  # Minimum number of connections
            max_size=50,  # Maximum number of connections
            **DATABASE_CONFIG
        )
    return await pool.acquire()


async def release_db_connection(conn):
    # Release a database connection back to the pool.
    await pool.release(conn)


async def create_orders_table_if_not_exists():
    # Create the 'orders' table if it doesn't exist.
    conn = await get_db_connection()
    try:
        await conn.execute(CREATE_ORDERS_TABLE_QUERY)
    finally:
        await release_db_connection(conn)


async def enable_uuid_extension_if_not_exists():
    # Enable the 'uuid-ossp' extension if it doesn't exist.
    conn = await get_db_connection()
    try:
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    finally:
        await release_db_connection(conn)


async def populate_sample_data():
    conn = await get_db_connection()
    try:
        await conn.execute(INSERT_DUMMY_RECORDS)
    finally:
        await release_db_connection(conn)
