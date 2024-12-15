from flask import *
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
import matplotlib
matplotlib.use('Agg')  # Set backend to Agg (non-interactive)
import matplotlib.pyplot as plt
import io
import base64


app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'   
app.config['MYSQL_PASSWORD'] = '@Bhijit6151'
app.config['MYSQL_DB'] = 'donation'

mysql = MySQL(app)

# Mailgun SMTP Configuration
app.config['MAIL_SERVER'] = 'smtp.mailgun.org'  # Mailgun SMTP server
app.config['MAIL_PORT'] = 587                   # SMTP port
app.config['MAIL_USERNAME'] = 'postmaster@mg.emiyasusan.me'  # Your Mailgun SMTP username
app.config['MAIL_PASSWORD'] = '3a30746c967057d0d41781a842653921-da554c25-373e8430'  # Your Mailgun SMTP password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# @app.route('/send-email')
# def send_email():
#     try:
#         msg = Message(
#             'Hello',                  # Subject
#             sender='verify-otp@sea.org', # Replace with your Mailgun verified sender email
#             recipients=['abhijit.srivathsan@msds.christuniversity.in']  # Replace with the recipient's email
#         )
#         msg.body = 'Hello World!'  # Email body
#         mail.send(msg)
#         return 'Email sent successfully!'
#     except Exception as e:
#         return f'Error: {str(e)}'

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM centers")
    centers = cur.fetchall()
    cur.close()
    return render_template('index.html', centers=centers)


    
# @app.route('/submit_donation', methods=['POST'])
# def submit_donation():
#     if request.method == 'POST':
#         # Retrieve form data
#         donor_type = request.form['donor-type']
#         name = request.form['name']
#         email = request.form['email']
#         delivery_type = request.form['delivery-type']
#         pickup_address = request.form['pickup_address']
#         city = request.form['city']
        
#         # Quantities for each item (default to 0 if input is empty)
#         clothes = int(request.form.get('quantity_clothes', '0') or '0')
#         necessary_items = int(request.form.get('quantity_items', '0') or '0')
#         food = int(request.form.get('quantity_food', '0') or '0')
#         healthcare_products = int(request.form.get('quantity_healthcare', '0') or '0')
        
#         # Validate at least one quantity is non-zero
#         if not (clothes > 0 or necessary_items > 0 or food > 0 or healthcare_products > 0):
#             message = "Error: You must donate at least one item."
#             return render_template('message.html', message=message)

#         try:
#             # Database Insert Query
#             cur = mysql.connection.cursor()
#             query = """
#                 INSERT INTO donations (donor_type, name, email, delivery_type, city, clothes, necessary_items, food, healthcare_products, pickup_address)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             values = (donor_type, name, email, delivery_type, city, clothes, necessary_items, food, healthcare_products, pickup_address)
#             cur.execute(query, values)
#             mysql.connection.commit()
#             cur.close()
            
#             # Success message
#             message = f"Thank you {name}! Your donation has been received successfully. We SEA your kindness :)"
#             return render_template('message.html', message=message)
#         except Exception as e:
#             # Error handling
#             message = f"Error: {str(e)}"
#             return render_template('message.html', message=message)

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
            
            # Send Thank You Email
            subject = "Donation Confirmation - SEA Organisation"
            msg = Message(subject=subject, sender='donations@sea.org', recipients=[email])
            
            # HTML Content for the email
            if delivery_type == 'doorstep pick':
                email_body = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333333;
                        }}
                        h2 {{
                            color: #2c3e50;
                        }}
                        .content {{
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                            padding: 20px;
                            border-radius: 5px;
                        }}
                        .details {{
                            margin-top: 10px;
                            margin-bottom: 20px;
                        }}
                        .footer {{
                            font-size: 0.9em;
                            color: #888888;
                            margin-top: 20px;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <div class="content">
                        <h2>Thank You, {name}!</h2>
                        <p>We <strong>SEA</strong> your kindness and appreciate your generous donation!</p>
                        <div class="details">
                            <p><strong>Your donation details are:</strong></p>
                            <ul>
                                <li><strong>Clothes:</strong> {clothes}</li>
                                <li><strong>Necessary Items:</strong> {necessary_items}</li>
                                <li><strong>Food:</strong> {food}</li>
                                <li><strong>Healthcare Products:</strong> {healthcare_products}</li>
                                <li><strong>Pickup Address:</strong> {pickup_address}</li>
                            </ul>
                        </div>
                        <p>Since you have opted for <strong>Doorstep Pickup</strong>, please ensure that your packages are tightly packed for us to pick up easily.</p>
                    </div>
                    <div class="footer">
                        &copy; 2024. SEA Organisation. All Rights Reserved.
                    </div>
                </body>
                </html>
                """
            else:
                email_body = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333333;
                        }}
                        h2 {{
                            color: #2c3e50;
                        }}
                        .content {{
                            background-color: #f9f9f9;
                            border: 1px solid #ddd;
                            padding: 20px;
                            border-radius: 5px;
                        }}
                        .details {{
                            margin-top: 10px;
                            margin-bottom: 20px;
                        }}
                        .footer {{
                            font-size: 0.9em;
                            color: #888888;
                            margin-top: 20px;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <div class="content">
                        <h2>Thank You, {name}!</h2>
                        <p>We <strong>SEA</strong> your kindness and appreciate your generous donation!</p>
                        <div class="details">
                            <p><strong>Your donation details are:</strong></p>
                            <ul>
                                <li><strong>Clothes:</strong> {clothes}</li>
                                <li><strong>Necessary Items:</strong> {necessary_items}</li>
                                <li><strong>Food:</strong> {food}</li>
                                <li><strong>Healthcare Products:</strong> {healthcare_products}</li>
                            </ul>
                        </div>
                        <p>Since you have opted for <strong>Courier Service</strong>, please ensure that your packages are tightly packed. We hope to receive your donations at the earliest :)</p>
                    </div>
                    <div class="footer">
                        &copy; 2024. SEA Organisation. All Rights Reserved.
                    </div>
                </body>
                </html>
                """
            
            # Send the email
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
        print(city)
        return render_template('center.html', city=city,center=center)  # Pass a single center object
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





app.run(debug=True)