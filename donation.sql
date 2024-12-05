CREATE DATABASE donation;
USE donation;

create table monetary (
	id INT PRIMARY KEY AUTO_INCREMENT,
    name text,
    email text,
    phone VARCHAR(10),
    amount VARCHAR(255));
    
create table special (
	id INT PRIMARY KEY AUTO_INCREMENT,
    individual text,
    occasion text,
    email text,
    phone VARCHAR(10));

create table joiners (
	id INT PRIMARY KEY AUTO_INCREMENT,
    name text,
    email text,
    phone VARCHAR(10));
    
insert into monetary (name, email, phone, amount) values 
	('Abhijit', 'abhijit.7472@gmail.com', '7259134284', 300);

INSERT INTO monetary (name, email, phone, amount) VALUES 
	('Abhijit', 'abhijit.7472@gmail.com', 7259134284, '300');
    
alter table monetary
modify phone varchar(255);

alter table special
modify phone varchar(255);

alter table joiners
modify phone varchar(255);

INSERT INTO special (individual, occasion, email, phone) values
	('Corporate', 'Birthday', '19pc9053abhijit2c9@gmail.com', 7259134284);
    
INSERT INTO joiners (name, email, phone) values
	('Abhijit', 'abhijit.7472@gmail.com', 7259134284);
