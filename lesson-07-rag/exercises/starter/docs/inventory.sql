CREATE TABLE IF NOT EXISTS inventory (
    product_id VARCHAR(255) PRIMARY KEY,
    quantity INT NOT NULL
);

INSERT INTO inventory (product_id, quantity) VALUES
("P001", 100),
("P002", 50),
("P003", 200),
("P004", 75);
