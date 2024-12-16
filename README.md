# 🌟 Donation Website for 4 Cities 🌍

Welcome to our **Donation Website**! This project is a platform designed to connect donors with meaningful causes across **4 cities**. With robust backend support, seamless email integrations, and user-friendly features, this project showcases the power of Flask, MySQL, and modern APIs. 🚀

---

## ✨ Features

### 🔒 User Authentication
- Secure **login** and **logout** sessions.  
- **OTP-based verification** for password changes and other sensitive actions.  

### 📧 Email Notifications
- Automated **booking confirmations** and **OTP emails** using:
  - **Flask-Mail** for SMTP-based email functionality.  
  - **Mailgun** API for reliable and scalable email delivery.  

### 📊 City-specific Donation Management
- Covers **4 cities**, each with its own donation database and tracking.  
- Backend powered by **MySQL**, with efficient table structures for managing donors, donations, and user data.

### 🛠️ Backend Architecture
- Built with **Flask** and **Flask-MySQLdb** for database integration.  
- Email functionalities powered by **Flask-Mail** and **Mailgun SMTP**.

---

## 🗂️ Database Overview

The backend is designed with **MySQL**, featuring well-structured tables for:

- **Users**: Storing user login credentials and profiles.  
- **Donations**: Tracking donation records for the 4 cities.  
- **OTP Requests**: Managing OTPs for password resets and verification.  
- **Bookings**: Storing and confirming donation bookings.  

---

Here’s the entire content formatted for your README.md. You can copy and paste it directly:

markdown
Copy code
# 🌟 Donation Website for 4 Cities 🌍

Welcome to our **Donation Website**! This project is a platform designed to connect donors with meaningful causes across **4 cities**. With robust backend support, seamless email integrations, and user-friendly features, this project showcases the power of Flask, MySQL, and modern APIs. 🚀

---

## ✨ Features

### 🔒 User Authentication
- Secure **login** and **logout** sessions.  
- **OTP-based verification** for password changes and other sensitive actions.  

### 📧 Email Notifications
- Automated **booking confirmations** and **OTP emails** using:
  - **Flask-Mail** for SMTP-based email functionality.  
  - **Mailgun** API for reliable and scalable email delivery.  

### 📊 City-specific Donation Management
- Covers **4 cities**, each with its own donation database and tracking.  
- Backend powered by **MySQL**, with efficient table structures for managing donors, donations, and user data.

### 🛠️ Backend Architecture
- Built with **Flask** and **Flask-MySQLdb** for database integration.  
- Email functionalities powered by **Flask-Mail** and **Mailgun SMTP**.

---

## 🗂️ Database Overview

The backend is designed with **MySQL**, featuring well-structured tables for:

- **Users**: Storing user login credentials and profiles.  
- **Donations**: Tracking donation records for the 4 cities.  
- **OTP Requests**: Managing OTPs for password resets and verification.  
- **Bookings**: Storing and confirming donation bookings.  

---

## 🚀 Installation and Setup

Follow these steps to set up the project locally:  

### 1️⃣ Prerequisites
- Python 3.x 🐍  
- MySQL installed and configured.  
- Flask dependencies (listed in `requirements.txt`).  



4️⃣ Configure MySQL Database
Create a MySQL database and import the schema provided in database/finaldb.sql.
Update your database credentials in app.py:
python
Copy code
app.config['MYSQL_USER'] = 'your-username'
app.config['MYSQL_PASSWORD'] = 'your-password'
app.config['MYSQL_DB'] = 'your-database-name'
app.config['MYSQL_HOST'] = 'localhost'


5️⃣ Set Up Mailgun and Flask-Mail
Add your Mailgun API Key and domain to the environment variables or directly in the app:
python
Copy code
MAILGUN_API_KEY = 'your-api-key'
MAILGUN_DOMAIN = 'your-domain.com'
Configure your SMTP settings for Flask-Mail.

6️⃣ Run the Application
bash
Copy code
python app.py
Visit http://127.0.0.1:5000 to access the website.

🎨 Screenshots
Homepage	Login Page
Donation Confirmation	OTP Email

🌟 Why This Project is Awesome
1. Full-stack integration with Flask and MySQL.
2. Demonstrates secure user authentication and session management.
3. Real-world implementation of email automation using Flask-Mail and Mailgun.
4. A scalable database design tailored for real-world applications.
