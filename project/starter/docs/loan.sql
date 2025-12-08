CREATE TABLE loans (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  loan_type VARCHAR(255) NOT NULL,
  origination_date DATE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  outstanding_balance DECIMAL(10, 2) NOT NULL,
  terms INT NOT NULL,
  monthly_payment DECIMAL(10, 2) NOT NULL,
  next_payment_date DATE NOT NULL
);

INSERT INTO loans (customer_id, loan_type, origination_date, amount, outstanding_balance, terms, monthly_payment, next_payment_date) VALUES
(1, 'auto', '2023-01-15', 25000.00, 12024.04, 60, 471.78, '2025-10-01'),
(1, 'personal', '2024-05-20', 15000.00, 10159.25, 48, 359.19, '2025-10-15');
