INSERT INTO centers (city, col1, col2, col3, img1, img2, img3)
VALUES ('Hyderabad', 'Cloth donation', 'Medical camp', 'Education drive', 
        'static/images/cloth.jpeg', 'static/images/health.jpeg', 'static/images/smtg.jpeg');


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
