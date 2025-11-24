CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    cart JSON,
    address JSON,
    order_status VARCHAR(50),
    shipping_cost FLOAT,
    tax_amount FLOAT,
    total_cost FLOAT
);

INSERT INTO orders (order_id, user_id, cart, address, order_status) VALUES
(1001, 'user', '["P001", "P002"]', '{"name": "John Doe", "address_1": "123 Main St", "city": "Anytown", "state": "CA", "postal_code": "90210"}', 'placed'),
(1002, 'user', '["P002", "P004"]', NULL, NULL),
(1003, 'user3', '["P001"]', NULL, NULL);
