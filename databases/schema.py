CREATE_ORDERS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id INTEGER NOT NULL,
        item_ids INTEGER[] NOT NULL,
        total_amount FLOAT NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

INSERT_DUMMY_RECORDS = """
    INSERT INTO orders (user_id, item_ids, total_amount, status)
    VALUES
        (1, '{101, 102}', 200.00, 'Pending'),    
        (2, '{103, 104}', 150.50, 'Processing'),
        (3, '{105, 106}', 300.75, 'Completed'), 
        (1, '{107, 108}', 99.99, 'Pending'),    
        (4, '{109, 110}', 450.00, 'Processing'),
        (5, '{111, 112}', 120.00, 'Completed'), 
        (2, '{113, 114}', 75.25, 'Pending'),    
        (3, '{115, 116}', 500.00, 'Processing'),
        (4, '{117, 118}', 250.50, 'Completed'), 
        (5, '{119, 120}', 99.99, 'Pending');    
    SELECT * FROM orders;
"""