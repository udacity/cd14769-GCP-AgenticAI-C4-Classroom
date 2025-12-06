CREATE TABLE IF NOT EXISTS inventory (
    product_id VARCHAR(255) PRIMARY KEY,
    quantity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO inventory (product_id, quantity) VALUES
("P001", 50),
("P002", 150),
("P003", 0),
("P004", 100);

INSERT INTO products (product_id, name, description, price) VALUES
("P001", "Wireless Headphones", "Noise cancelling over-ear headphones", 299.99),
("P002", "Smartphone Stand", "Adjustable aluminum stand for all smartphones", 19.99),
("P003", "Bluetooth Speaker", "Portable waterproof speaker with 20h battery life", 59.99),
("P004", "USB-C Cable", "2-meter braided fast charging cable", 12.99);