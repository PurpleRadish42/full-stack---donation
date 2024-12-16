create database finaldb;
use finaldb;

CREATE TABLE login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Insert an admin user into the login table
ALTER TABLE login
MODIFY password
varchar(255);
ALTER TABLE login ADD COLUMN email VARCHAR(255);

select*from login;

insert into login(username,password,role,email) values ('admin','admin123','admin','your_email');


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

CREATE TABLE donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    delivery_type VARCHAR(50),
    city VARCHAR(50),
    clothes INT DEFAULT 0,
    necessary_items INT DEFAULT 0,
    food INT DEFAULT 0,
    healthcare_products INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    donor_type VARCHAR(255)
);


ALTER TABLE donations ADD COLUMN pickup_address VARCHAR(255);

select * from donations;

create table centers(
	id INT PRIMARY KEY AUTO_INCREMENT,
    city text,
    col1 text,
    col2 text,
    col3 text,
    img1 text,
    img2 text,
    img3 text,
    address text);

alter table bookings add column email varchar(255);

CREATE TABLE volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);