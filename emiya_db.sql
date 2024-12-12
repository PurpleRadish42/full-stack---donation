CREATE DATABASE emiya_db;
USE emiya_db;

CREATE TABLE payment(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Display the records in the payments table
SELECT * FROM payment;

CREATE TABLE login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Insert an admin user into the login table
INSERT INTO login (username, password, role) VALUES ('admin', 'admin123', 'admin');

