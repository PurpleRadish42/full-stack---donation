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

INSERT INTO login(username,password, role) VALUES ('emiya', 'emiya123', 'user');
ALTER TABLE login
MODIFY password
varchar(255);

select*from login;

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method ENUM('Credit Card', 'Debit Card', 'UPI') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select*from payments;


