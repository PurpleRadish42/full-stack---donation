CREATE DATABASE emiya_db;
USE emiya_db;


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
ALTER TABLE login ADD COLUMN email VARCHAR(255);

select*from login;

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,         -- Unique identifier for each payment
    name VARCHAR(100) NOT NULL,                -- Donor's name
    email VARCHAR(150) NOT NULL,               -- Donor's email address
    amount DECIMAL(10, 2) NOT NULL,            -- Donation amount (supports values up to 10 digits with 2 decimals)
    payment_method VARCHAR(50) NOT NULL,       -- Payment method (e.g., Credit Card, Debit Card, UPI)
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date and time of the payment
);

select*from payments;

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    center VARCHAR(50),
    type VARCHAR(20),
    name VARCHAR(100),
    date DATE,
    time VARCHAR(20),
    occasion VARCHAR(100)
);
select*from bookings;
CREATE TABLE contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select*from contact;



