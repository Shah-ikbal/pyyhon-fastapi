from databases.postgresdb import get_db_connection, release_db_connection


async def get_metrics():
    conn = await get_db_connection()
    try:
        # Get total orders
        total_orders = await conn.fetchval("SELECT COUNT(*) FROM orders")

        # Get counts by status
        status_counts = await conn.fetch(
            "SELECT status, COUNT(*) as count FROM orders GROUP BY status"
        )
        status_counts = {row["status"]: row["count"] for row in status_counts}

        # Calculate average processing time for completed orders
        avg_processing_time = (
            await conn.fetchval(
                """
            SELECT AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) as avg_time
            FROM orders
            WHERE status = 'Completed'
        """
            )
            or 0
        )

        return {
            "total_orders": total_orders,
            "avg_processing_time": avg_processing_time,
            "pending_orders": status_counts.get("Pending", 0),
            "processing_orders": status_counts.get("Processing", 0),
            "completed_orders": status_counts.get("Completed", 0),
        }
    finally:
        await release_db_connection(conn)