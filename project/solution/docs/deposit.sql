CREATE TABLE IF NOT EXISTS accounts (
  id INT PRIMARY KEY,
  customer_id INT NOT NULL,
  account_type VARCHAR(255) NOT NULL,
  balance DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  account_id INT NOT NULL,
  transaction_date DATE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  description VARCHAR(255) NOT NULL,
  FOREIGN KEY (account_id) REFERENCES accounts(id)
);

INSERT INTO accounts (id, customer_id, account_type, balance) VALUES
(1, 1, 'vacation', 1500.00),
(2, 1, 'primary', 5230.50);

INSERT INTO transactions (account_id, transaction_date, amount, description) VALUES
(1, '2025-09-12', -50.00, 'Lunch'),
(1, '2025-09-11', -200.00, 'Hotel'),
(1, '2025-09-10', 1000.00, 'Paycheck'),
(2, '2025-09-13', -15.25, 'Coffee'),
(2, '2025-09-12', -80.00, 'Groceries'),
(2, '2025-09-11', -120.00, 'Gas');
