from locust import HttpUser, task, between

class ECommerceUser(HttpUser):
    wait_time = between(1, 5)  # Simulate users waiting between 1 and 5 seconds

    @task
    def create_order(self):
        # Simulate creating an order
        order_data = {
            "user_id": 1,
            "item_ids": [101, 102],
            "total_amount": 200.0
        }
        self.client.post("/api/v1/orders/create-order", json=order_data)

    # @task(3)
    # def check_order_status(self):
    #     # Simulate checking the status of an order
    #     order_id = 1  # Replace with a valid order ID
    #     self.client.get(f"/api/v1/orders/order-status/{order_id}")