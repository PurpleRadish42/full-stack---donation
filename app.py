from flask import *
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_mail import Mail, Message
import random
from functools import wraps
import matplotlib
matplotlib.use('Agg')  # Set backend to Agg (non-interactive)
import matplotlib.pyplot as plt
import io
import base64
# import requests

app = Flask(__name__)
app.secret_key = 'Dustbin'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@Bhijit6151'
app.config['MYSQL_DB'] = 'finaldb'

mysql = MySQL(app)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.mailgun.org'  # Replace with your email provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'postmaster@mg.emiyasusan.me'
app.config['MAIL_PASSWORD'] = '3a30746c967057d0d41781a842653921-da554c25-373e8430'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
app.secret_key = 'Dustbin'

# Temporary storage for OTP and user data
temp_user_data = {}

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM centers")
    centers = cur.fetchall()
    cur.close()
    return render_template('index.html', centers=centers)

@app.route('/donation')
def donation():
    return render_template('donation.html')

# Decorators for role-based access control
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin login required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('User login required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the username or email already exists in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE username = %s", (username,))
        username_exists = cur.fetchone()
        cur.execute("SELECT * FROM login WHERE email = %s", (email,))
        email_exists = cur.fetchone()
        cur.close()

        if username_exists:
            flash("Username already exists. Please choose a different one.", "error")
            return render_template('register.html')

        if email_exists:
            flash("Email already exists. Please use a different email.", "error")
            return render_template('register.html')

        # Password match validation
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('register.html')

        # Generate OTP and store temporary user data
        generated_otp = random.randint(100000, 999999)
        temp_user_data[email] = {
            'username': username,
            'password': generate_password_hash(password),
            'otp': generated_otp,
            'role': 'user'
        }

        try:
            # Send OTP via email
            msg = Message('Your OTP for Registration', sender='verify-otp@sea.org', recipients=[email])
            msg.body = f"Your OTP is {generated_otp}. It is valid for 5 minutes."
            mail.send(msg)
            return render_template('otp-verification.html', email=email, message=f"OTP sent to your email: {email}")
        except Exception as e:
            flash('Failed to send OTP. Please try again.', "error")
            return render_template('register.html')

    return render_template('register.html')


@app.route('/otp-verification/<email>', methods=['GET', 'POST'])
def otp_verification(email):
    if request.method == 'POST':
        entered_otp = request.form['otp']

        # Validate OTP
        if email in temp_user_data and temp_user_data[email]['otp'] == int(entered_otp):
            user_data = temp_user_data.pop(email)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO login (username, password, role, email) VALUES (%s, %s, %s, %s)",
                        (user_data['username'], user_data['password'], user_data['role'], email))
            mysql.connection.commit()
            cur.close()

            # Send a confirmation email after successful registration
            try:
                msg = Message('Registration Successful', sender='registrations@sea.org', recipients=[email])
                msg.html = render_template('email_template.html', username=user_data['username'])
                mail.send(msg)
            except Exception as e:
                flash('Failed to send confirmation email.', 'error')

            # Render the success message page
            return render_template('message.html', 
                                   message="Thank you for joining our family, we have sent an email confirming the same. We hope to SEA you soon.")
        else:
            flash('Invalid OTP. Please try again.', 'error')
            return redirect(url_for('otp_verification', email=email))

    return render_template('otp-verification.html', email=email)


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
    # Fetch data from the POST form
    name = request.form.get('name')
    email = request.form.get('email')
    amount = request.form.get('amount')
    payment_method = request.form.get('paymentMethod')

    try:
        # Store payment details in the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO payments (name, email, amount, payment_method) VALUES (%s, %s, %s, %s)', 
                       (name, email, amount, payment_method))
        mysql.connection.commit()

        # Redirect to the message page on success with a custom message
        message = f"Thank you {name}, We appre-sea-ite your kindness"
        return redirect(url_for('message', message=message))
    
    except Exception as e:
        # If there's a failure, flash a failure message and stay on the same page
        flash('Payment failure')
        return redirect(url_for('payment'))

@app.route('/message')
def message():
    message = request.args.get('message', 'Default message')
    back_url = request.args.get('back_url', url_for('home'))
    return render_template('message.html', message=message, back_url=back_url)




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
    
@app.route('/submit_donation', methods=['POST'])
def submit_donation():
    if request.method == 'POST':
        # Retrieve form data
        donor_type = request.form['donor-type']
        name = request.form['name']
        email = request.form['email']
        delivery_type = request.form['delivery-type']
        pickup_address = request.form['pickup_address']
        city = request.form['city']
        address = request.form['address']
        
        # Quantities for each item (default to 0 if input is empty)
        clothes = int(request.form.get('quantity_clothes', '0') or '0')
        necessary_items = int(request.form.get('quantity_items', '0') or '0')
        food = int(request.form.get('quantity_food', '0') or '0')
        healthcare_products = int(request.form.get('quantity_healthcare', '0') or '0')
        
        # Validate at least one quantity is non-zero
        if not (clothes > 0 or necessary_items > 0 or food > 0 or healthcare_products > 0):
            message = "Error: You must donate at least one item."
            return render_template('message.html', message=message)

        try:
            # Database Insert Query
            cur = mysql.connection.cursor()
            query = """
                INSERT INTO donations (donor_type, name, email, delivery_type, city, clothes, necessary_items, food, healthcare_products, pickup_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (donor_type, name, email, delivery_type, city, clothes, necessary_items, food, healthcare_products, pickup_address)
            cur.execute(query, values)
            mysql.connection.commit()
            cur.close()
            
            # Prepare the email
            subject = "Donation Confirmation - SEA Organisation"
            msg = Message(subject=subject, sender='donations@sea.org', recipients=[email])
            
            # Render the appropriate HTML template for the email
            if delivery_type == 'doorstep pick':
                email_body = render_template('email_doorstep.html', name=name, clothes=clothes, necessary_items=necessary_items, food=food, healthcare_products=healthcare_products, pickup_address=pickup_address)
            else:
                email_body = render_template('email_courier.html', name=name, clothes=clothes, necessary_items=necessary_items, food=food, healthcare_products=healthcare_products, address=address)
            
            # Attach the email body
            msg.html = email_body
            mail.send(msg)
            
            # Success message
            message = f"Thank you {name}! Your donation has been received successfully. We SEA your kindness :)"
            return render_template('message.html', message=message)
        
        except Exception as e:
            # Error handling
            message = f"Error: {str(e)}"
            return render_template('message.html', message=message)
    
@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Fetch data from all tables
    cur = mysql.connection.cursor()

    # Monetary donations
    cur.execute("SELECT * FROM monetary")
    monetary_data = cur.fetchall()
    # monetary_columns = [desc[0] for desc in cur.description]

    # Special occasions
    cur.execute("SELECT * FROM special")
    special_data = cur.fetchall()
    # special_columns = [desc[0] for desc in cur.description]

    # People who've joined
    cur.execute("SELECT * FROM joiners")
    joiners_data = cur.fetchall()
    # joiners_columns = [desc[0] for desc in cur.description]

    cur.execute("SELECT * FROM donations")
    donations_data = cur.fetchall()

    cur.close()

    # Render data into the HTML template
    return render_template(
        'dashboard.html',
        monetary_data=monetary_data,
        special_data=special_data,
        joiners_data=joiners_data,
        donations_data=donations_data
    )

@app.route('/center')
def center():
    center_id = request.args.get('id')

    # Validate if center_id exists and is numeric
    if not center_id or not center_id.isdigit():
        return render_template('message.html', message="Invalid center ID.")

    center_id = int(center_id)

    # Fetch the center's details from the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM centers WHERE id = %s", (center_id,))
    center = cursor.fetchone()  # Fetch one center
    cursor.close()

    if center:
        city = center[1]
        address = center[8]
        print(city)
        return render_template('center.html', city=city,address=address,center=center)  # Pass a single center object
    else:
        return render_template('message.html', message="Center not found.")
    


@app.route('/charts')
def show_charts():
    try:
        cur = mysql.connection.cursor()

        # Fetch data for pie charts: Total donations grouped by city
        pie_query = """
            SELECT city, SUM(clothes), SUM(necessary_items), SUM(food), SUM(healthcare_products)
            FROM donations
            GROUP BY city
        """
        cur.execute(pie_query)
        pie_rows = cur.fetchall()

        # Fetch data for bar charts: Count of delivery types (doorstep pick & courier service)
        bar_delivery_query = """
            SELECT city,
                   SUM(CASE WHEN delivery_type = 'doorstep pick' THEN 1 ELSE 0 END) AS doorstep_pick_count,
                   SUM(CASE WHEN delivery_type = 'courier service' THEN 1 ELSE 0 END) AS courier_service_count
            FROM donations
            GROUP BY city
        """
        cur.execute(bar_delivery_query)
        bar_delivery_rows = cur.fetchall()

        # Fetch data for bar charts: Count of Individual vs Company donors
        bar_donor_query = """
            SELECT city,
                   SUM(CASE WHEN donor_type = 'Individual' THEN 1 ELSE 0 END) AS individual_count,
                   SUM(CASE WHEN donor_type = 'Company' THEN 1 ELSE 0 END) AS company_count
            FROM donations
            GROUP BY city
        """
        cur.execute(bar_donor_query)
        bar_donor_rows = cur.fetchall()

        # Map delivery and donor data for quick access
        delivery_data = {row[0]: {'doorstep_pick': row[1], 'courier_service': row[2]} for row in bar_delivery_rows}
        donor_data = {row[0]: {'individual': row[1], 'company': row[2]} for row in bar_donor_rows}

        charts = []
        for row in pie_rows:
            city, clothes, necessary_items, food, healthcare = row

            # Data for the pie chart
            pie_labels = ['Clothes', 'Necessary Items', 'Food', 'Healthcare']
            pie_values = [clothes, necessary_items, food, healthcare]
            pie_colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99']

            # Generate the pie chart
            plt.figure(figsize=(5, 5))
            plt.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=140, colors=pie_colors)
            plt.title(f"{city} Donations Breakdown")
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            pie_chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close()

            # Generate bar chart for delivery methods
            doorstep = delivery_data[city]['doorstep_pick']
            courier = delivery_data[city]['courier_service']
            bar_labels_delivery = ['Doorstep Pick', 'Courier Service']
            bar_values_delivery = [doorstep, courier]
            bar_colors_delivery = ['#FF5733', '#33FF57']

            plt.figure(figsize=(5, 5))
            plt.bar(bar_labels_delivery, bar_values_delivery, color=bar_colors_delivery)
            plt.title(f"{city} Delivery Methods")
            plt.ylabel("Total Count")
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            bar_delivery_chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close()

            # Generate bar chart for donor type
            individual = donor_data[city]['individual']
            company = donor_data[city]['company']
            bar_labels_donor = ['Individual', 'Company']
            bar_values_donor = [individual, company]
            bar_colors_donor = ['#FFC300', '#581845']

            plt.figure(figsize=(5, 5))
            plt.bar(bar_labels_donor, bar_values_donor, color=bar_colors_donor)
            plt.title(f"{city} Donor Types")
            plt.ylabel("Total Count")
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            bar_donor_chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close()

            # Append chart data
            charts.append({
                'city': city,
                'pie_chart_base64': f"data:image/png;base64,{pie_chart_base64}",
                'bar_delivery_chart_base64': f"data:image/png;base64,{bar_delivery_chart_base64}",
                'bar_donor_chart_base64': f"data:image/png;base64,{bar_donor_chart_base64}"
            })

        cur.close()
        return render_template('charts.html', charts=charts)

    except Exception as e:
        # Error handling
        message = f"Error: {str(e)}"
        return render_template('message.html', message=message)

@app.route('/halloffame')
def top_donors():
    try:
        cur = mysql.connection.cursor()

        # Query for Top 3 Individual Donors (Include City)
        query_individual = """
            SELECT name, city, SUM(clothes + necessary_items + food + healthcare_products) AS total_donation
            FROM donations
            WHERE donor_type = 'Individual'
            GROUP BY email, name, city
            ORDER BY total_donation DESC
            LIMIT 3
        """
        cur.execute(query_individual)
        individual_donors = cur.fetchall()

        # Query for Top 3 Company Donors (Include City)
        query_company = """
            SELECT name, city, SUM(clothes + necessary_items + food + healthcare_products) AS total_donation
            FROM donations
            WHERE donor_type = 'Company'
            GROUP BY email, name, city
            ORDER BY total_donation DESC
            LIMIT 3
        """
        cur.execute(query_company)
        company_donors = cur.fetchall()

        # Format data for the template
        top_individuals = [{'name': row[0], 'city': row[1], 'total_donation': row[2]} for row in individual_donors]
        top_companies = [{'name': row[0], 'city': row[1], 'total_donation': row[2]} for row in company_donors]

        cur.close()

        return render_template('top_donors.html', top_individuals=top_individuals, top_companies=top_companies)

    except Exception as e:
        # Error handling
        message = f"Error: {str(e)}"
        return render_template('message.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)