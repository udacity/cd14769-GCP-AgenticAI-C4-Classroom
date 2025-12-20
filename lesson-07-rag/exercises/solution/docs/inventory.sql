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
("P004", 500),
("P005", 100),
("P006", 75),
("P007", 200),
("P008", 40),
("P009", 300),
("P010", 60),
("P011", 80),
("P012", 45),
("P013", 120),
("P014", 25);

INSERT INTO products (product_id, name, description, price) VALUES
("P001", "Wireless Headphones", "Noise cancelling over-ear headphones", 299.99),
("P002", "Smartphone Stand", "Adjustable aluminum stand for all smartphones", 19.99),
("P003", "Bluetooth Speaker", "Portable waterproof speaker with 20h battery life", 59.99),
("P004", "USB-C Cable", "2-meter braided fast charging cable", 12.99),
("P005", "Portable Charger", "10000mAh power bank with fast charging", 29.99),
("P006", "Laptop Sleeve", "Protective sleeve for 13-inch laptops", 24.99),
("P007", "Wireless Mouse", "Ergonomic wireless mouse with USB receiver", 19.99),
("P008", "Mechanical Keyboard", "RGB backlit mechanical gaming keyboard", 89.99),
("P009", "HDMI Cable", "3-meter high-speed HDMI 2.1 cable", 14.99),
("P010", "Smart Watch", "Fitness tracker with heart rate monitor", 149.99),
("P011", "Tablet Case", "Rugged protective case for 10-inch tablets", 19.99),
("P012", "Webcam", "1080p HD webcam with built-in microphone", 49.99),
("P013", "USB Hub", "4-port USB 3.0 data hub", 15.99),
("P014", "Monitor Stand", "Dual monitor desk mount stand", 39.99);