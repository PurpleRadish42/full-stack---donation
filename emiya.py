from flask import *
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'emiya_db'

mysql = MySQL(app)

# # Mail configuration
# app.config['MAIL_SERVER'] = 'smtp.mailgun.org'  # Replace with your email provider
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'postmaster@emiyasusan.me'
# app.config['MAIL_PASSWORD'] = 'dc6954c76690ddc07dca25af1ca634ca-da554c25-47e4a873'

# mail = Mail(app)

# # Temporary storage for OTP and user data
# temp_user_data = {}

# import requests

# def send_otp_email(email, otp):
#     # Mailgun API URL for sending messages
#     api_url = "https://api.mailgun.net/v3/sandboxc66dd56c4838437ab4f70881c111aaf7.mailgun.org/messages"
    
#     # Mailgun credentials (API key)
#     api_key = "834f80bc3a8fc0e72160a5dbe9b4073f-da554c25-ac74d598"
    
#     # Sender's email (Mailgun)
#     from_email = "Excited User <mailgun@sandboxc66dd56c4838437ab4f70881c111aaf7.mailgun.org>"
    
#     # Recipient email
#     to_email = email
    
#     # Subject and body of the email
#     subject = "OTP for Registration"
#     body = f"Your OTP for registration is: {otp}"

#     # Sending the request to Mailgun
#     response = requests.post(
#         api_url,
#         auth=("api", api_key),
#         data={
#             "from": from_email,
#             "to": [to_email],
#             "subject": subject,
#             "text": body
#         }
#     )

#     # You can log the response or handle it based on success/failure
#     if response.status_code == 200:
#         print("OTP sent successfully!")
#     else:
#         print("Failed to send OTP:", response.text)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         email = request.form['email']

#         if password != confirm_password:
#             flash("Passwords do not match.")
#             return redirect(url_for('register'))

#         # Generate OTP and store user data temporarily
#         otp = random.randint(100000, 999999)
#         temp_user_data[email] = {
#             'username': username,
#             'password': generate_password_hash(password),
#             'role': 'user',
#             'otp': otp
#         }

#         # Send OTP to the user's email
#         try:
#             msg = Message('OTP Verification', sender='postmaster@emiyasusan.me', recipients=[email])
#             msg.body = f'Your OTP for registration is: {otp}'
#             mail.send(msg)
#             flash('OTP sent to your email. Please verify.')
#             return redirect(url_for('otp_verification', email=email))
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             flash(f"Error sending email: {str(e)}")
#             return redirect(url_for('register'))

#     return render_template('register.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         email = request.form['email']

#         if password != confirm_password:
#             flash("Passwords do not match.")
#             return redirect(url_for('register'))

#         # Generate OTP and store user data temporarily
#         otp = random.randint(100000, 999999)
#         temp_user_data[email] = {
#             'username': username,
#             'password': generate_password_hash(password),
#             'role': 'user',
#             'otp': otp
#         }

#         # Send OTP to the user's email using Mailgun
#         try:
#             send_otp_email(email, otp)  # Send OTP via Mailgun
#             flash('OTP sent to your email. Please verify.')
#             return redirect(url_for('otp_verification', email=email))
#         except Exception as e:
#             flash(f"Error sending email: {str(e)}")
#             return redirect(url_for('register'))

#     return render_template('register.html')


# @app.route('/otp-verification/<email>', methods=['GET', 'POST'])
# def otp_verification(email):
#     if request.method == 'POST':
#         entered_otp = request.form['otp']

#         # Validate OTP
#         if email in temp_user_data and temp_user_data[email]['otp'] == int(entered_otp):
#             user_data = temp_user_data.pop(email)
#             cur = mysql.connection.cursor()
#             cur.execute("INSERT INTO login (username, password, role, email) VALUES (%s, %s, %s, %s)",
#                         (user_data['username'], user_data['password'], user_data['role'], email))
#             mysql.connection.commit()
#             cur.close()
#             flash('Registration successful. Please log in.')
#             return redirect(url_for('login'))
#         else:
#             flash('Invalid OTP. Please try again.')
#             return redirect(url_for('otp_verification', email=email))

#     return render_template('otp_verification.html', email=email)

@app.route('/')
def home():
    return redirect(url_for('login'))
@app.route('/logo')
def logo():
    return render_template('logo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Database query to fetch user information
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password, role FROM login WHERE username=%s", [username])
        user = cur.fetchone()
        cur.close()

        if user:
            user_id, hashed_password, user_role = user

            # Check if the entered password matches the stored hash
            if check_password_hash(hashed_password, password):
                if role == user_role:  # Validate the role selected
                    session['id'] = user_id
                    session['username'] = username
                    session['role'] = user_role

                    flash('Login successful!', 'success')

                    # Redirect based on role
                    if role == 'admin':
                        return redirect(url_for('dashboard'))
                    elif role == 'user':
                        return redirect(url_for('home'))
                else:
                    flash('Invalid role selection.', 'error')
            else:
                flash('Invalid username or password.', 'error')
        else:
            flash('User not found. Please register as a new user.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = 'user'  # Default role for new users

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO login (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')




@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        if session['role'] == 'admin':
            return render_template('dashboard.html', role='Admin')
        elif session['role'] == 'user':
            return render_template('dashboard.html', role='User')
    flash('Please log in to access this page.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payments.html')

@app.route('/payment-success', methods=['POST'])
def payment_success():
    # Fetch data from the form
    name = request.form.get['name']
    email = request.form.get['email']
    amount = request.form.get['amount']
    payment_method = request.form.get['paymentMethod']

    # Store payment details in the database
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO payments (name, email, amount, payment_method) VALUES (%s, %s, %s, %s)', 
                   (name, email, amount, payment_method))
    mysql.connection.commit()

    return 'Success', 200

@app.route('/message')
def message():
    message = request.args.get('message', 'Default message')
    back_url = request.args.get('back_url', url_for('home'))
    return render_template('message.html', message=message, back_url=back_url)

# @app.route('/confirmation')
# def confirmation():
#     # Fetching the payment details from the URL parameters
#     name = request.args.get('name')
#     email = request.args.get('email')
#     amount = request.args.get('amount')
#     method = request.args.get('method')
#     return render_template('confirmation.html', name=name, email=email, amount=amount, method=method)

@app.route('/donation',methods=['GET','POST'])
def donation():
    return render_template('donation.html')



@app.route('/special')
def special():
    return render_template('special.html')

@app.route('/book-slot', methods=['POST'])
def book_slot():
    center = request.form['center']
    type_ = request.form['type']
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    occasion = request.form['occasion']

    # Check if the slot is already booked
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bookings WHERE date = %s AND time = %s AND center = %s", (date, time, center))
    existing_booking = cur.fetchone()

    if existing_booking:
        cur.close()
        return "<script>alert('Sorry, the slot is already booked.'); window.location.href = '/';</script>"

    # Insert booking into the database
    cur.execute("INSERT INTO bookings (center, type, name, date, time, occasion) VALUES (%s, %s, %s, %s, %s, %s)",
                (center, type_, name, date, time, occasion))
    mysql.connection.commit()
    cur.close()

    return "<script>alert('Booking successful!'); window.location.href = '/';</script>"

@app.route('/available-slots', methods=['GET'])
def available_slots():
    cur = mysql.connection.cursor()
    cur.execute("SELECT date, time FROM bookings")
    booked_slots = cur.fetchall()
    cur.close()

    # Convert booked slots to a list of dictionaries
    booked_slots_list = [{'date': slot[0].strftime('%Y-%m-%d'), 'time': slot[1]} for slot in booked_slots]
    return jsonify(booked_slots_list)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Insert data into the database
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
            mysql.connection.commit()
            cur.close()

            # Pass the success message to the message.html template
            success_message = "We have received your message. Thank you for reaching out!"
            return render_template('message.html', 
                                   title="Message Status", 
                                   message=success_message, 
                                   back_url=url_for('contact'))

        except Exception as e:
            # Log the error and return an error message
            print("Error: ", e)
            error_message = "Something went wrong. Please try again later."
            return render_template('message.html', 
                                   title="Error", 
                                   message=error_message, 
                                   back_url=url_for('contact'))
    return render_template('contactus.html')

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    return render_template('volunteer.html')

@app.route('/submit_application', methods=['POST'])
def submit_application():
    # Get data from the form
    name = request.form['name']
    email = request.form['email']
    interest = request.form['interest']
    
    # Insert data into the database
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO volunteers (name, email, interest) VALUES (%s, %s, %s)", (name, email, interest))
        mysql.connection.commit()
        cur.close()

        # Pass the success message to the message.html template
        success_message = "Thank you for applying! We appreciate your interest and will contact you soon."
        return render_template('message.html', 
                               title="Application Status", 
                               message=success_message, 
                               back_url=url_for('volunteer'))

    except Exception as e:
        # Log the error and return an error message
        print("Error: ", e)
        error_message = "Something went wrong. Please try again later."
        return render_template('message.html', 
                               title="Error", 
                               message=error_message, 
                               back_url=url_for('volunteer'))

if __name__ == '__main__':
    app.run(debug=True)




