# Setting up the Project

    # Create a virtual environment and excute the following commands
        - python3 -m parspec-assignment venv
        - source parspec-assignment/bin/activate

    # Install the respective packages from requirements.txt file
        - pip install -r requirements.txt (pip3 incase of using pip3)

    # Run the server using the following command
        - uvicorn main:app --reload   

    # Use the following url to get the documentation of the APIs
        Swaggger Docs URL - http://localhost:8000/docs#/   


# Design Decisions and Assumption

1. Use of FastAPI
    Decision: FastAPI was chosen as the web framework for building the RESTful API.

Why:

    Asynchronous Support: FastAPI natively supports asynchronous programming, which is essential for handling concurrent requests efficiently.
    Performance: FastAPI is one of the fastest Python web frameworks, making it suitable for high-throughput systems.
    Ease of Use: FastAPI provides automatic validation, serialization, and documentation (via Swagger UI), reducing development time.

Trade-offs:

    Learning Curve: Developers unfamiliar with asynchronous programming or Pydantic models may face a learning curve.
    Dependency on Async Libraries: FastAPI works best with asynchronous libraries, which may limit the choice of compatible tools.

2. Use of PostgreSQL
    Decision: PostgreSQL was chosen as the database for storing orders.

Why:

    Reliability: PostgreSQL is a robust, production-ready relational database with ACID compliance.
    Scalability: PostgreSQL can handle large datasets and complex queries efficiently.

Trade-offs:

    Complexity: Setting up and managing PostgreSQL requires more effort compared to SQLite.
    Performance: While PostgreSQL is performant, it may require tuning (e.g., indexing, connection pooling) for very high loads.

3. Use of asyncpg
    Decision: asyncpg was chosen as the database driver for interacting with PostgreSQL.

Why:

    Asynchronous Support: asyncpg is designed for async programming, making it a natural fit for FastAPI.
    Performance: asyncpg is one of the fastest PostgreSQL drivers for Python, offering low-level access to the database.
    Connection Pooling: asyncpg provides built-in support for connection pooling, which is essential for handling concurrent database operations.

Trade-offs:

    Complexity: asyncpg requires manual SQL query writing, which can be error-prone compared to ORMs like SQLAlchemy.
    sLearning Curve: Developers unfamiliar with raw SQL may find it challenging to use asyncpg effectively.

4. In-Memory Queue for Order Processing
    Decision: An in-memory queue (Python queue.Queue) was used to simulate asynchronous order processing.

Why:

    Simplicity: An in-memory queue is easy to implement and suitable for small-scale systems or prototypes.
    Low Latency: Since the queue is in-memory, it offers very low latency for enqueueing and dequeueing operations.
    Decoupling: The queue decouples the order creation and processing logic, allowing for asynchronous processing.

Trade-offs:

    Scalability: An in-memory queue is not suitable for distributed systems or high-availability setups. If the application crashes, all queued orders are lost.
    Persistence: The queue does not persist data, making it unsuitable for systems requiring fault tolerance.
    Concurrency: Python’s queue.Queue is thread-safe but not optimized for async programming. In this implementation, it works because the queue is only used to pass data to the async processor.

5. Asynchronous Order Processing
    Decision: Orders are processed asynchronously using a background task.

Why:

    Scalability: Asynchronous processing allows the system to handle multiple orders concurrently without blocking the main application.
    Simulated Processing Time: The asyncio.sleep(5) simulates a delay in order processing, mimicking real-world scenarios.
    Efficiency: By using asyncio.create_task, the system can process multiple orders in parallel without creating separate threads.

Trade-offs:

    Complexity: Asynchronous programming can be harder to debug and reason about compared to synchronous code.
    Error Handling: Proper error handling is required to ensure that failed orders are retried or logged.

6. Modular Design
    Decision: The application is divided into modular components (e.g., API endpoints, queue processor, database operations).

Why:

    Separation of Concerns: Each component has a single responsibility, making the code easier to maintain and test.
    Reusability: Modular components can be reused or replaced independently (e.g., switching from an in-memory queue to a message broker like RabbitMQ).
    Scalability: Modular design allows for horizontal scaling (e.g., running the queue processor as a separate service).

Trade-offs:

    Initial Complexity: Designing modular components requires more upfront effort compared to a monolithic design.
    Overhead: Modularity can introduce some overhead in terms of code organization and communication between components.

7. Metrics API
    Decision: A separate API endpoint was implemented to fetch key metrics (e.g., total orders, average processing time, order status counts).

Why:

    Monitoring: Metrics provide insights into the system’s performance and help identify bottlenecks.
    Transparency: Users can track the status of their orders and understand system behavior.
    Scalability: Metrics can be used to monitor the system as it scales.

Trade-offs:

    Performance Impact: Calculating metrics (e.g., average processing time) can be computationally expensive for large datasets.
    Real-Time Accuracy: Metrics may not reflect real-time data if the system is under heavy load.

#Assumptions
    Design Assumptions:

        Small to Medium Scale: The system is designed for small to medium-scale e-commerce platforms. For larger systems, a distributed message broker (e.g., RabbitMQ, Kafka) and a more robust database setup would be required.
        Single Instance: The application assumes a single instance of the service. For high availability, multiple instances with load balancing would be needed.
        Simulated Processing Time: The 5-second delay in order processing is a simulation. In a real-world scenario, processing time would depend on the complexity of the order.
        No Authentication: The API does not include authentication or authorization. In a production system, this would be essential for security.

    Trade-offs Summary
        Decision	Advantages	Trade-offs
        FastAPI	High performance, async support, automatic docs	Learning curve, dependency on async libraries
        PostgreSQL	Reliability, JSONB support, scalability	Setup complexity, requires tuning for high loads
        asyncpg	High performance, async support, connection pooling	Manual SQL, learning curve
        In-Memory Queue	Simplicity, low latency, decoupling	Not scalable, no persistence, not fault-tolerant
        Asynchronous Processing	Scalability, efficiency, parallel processing	Complexity, requires proper error handling
        Modular Design	Separation of concerns, reusability, scalability	Initial complexity, overhead
        Metrics API	Monitoring, transparency, scalability insights	Performance impact, real-time accuracy

    Future Improvements
        Use a Message Broker: Replace the in-memory queue with a distributed message broker like RabbitMQ or Kafka for better scalability and fault tolerance.
        Add Authentication: Implement API authentication (e.g., OAuth2, JWT) to secure the endpoints.
        Database Indexing: Add indexes to frequently queried fields (e.g., order_id, status) to improve query performance.
        Distributed Processing: Use a task queue like Celery or RQ for distributed order processing.
        Persistence: Persist the queue state to a database or file system to prevent data loss during crashes. 
