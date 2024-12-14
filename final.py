from flask import *
from flask_mysqldb import MySQL
from flask_mail import Mail, Message


app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'   
app.config['MYSQL_PASSWORD'] = '@Bhijit6151'
app.config['MYSQL_DB'] = 'donation'

mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM centers")
    centers = cur.fetchall()
    cur.close()
    return render_template('index.html', centers=centers)



@app.route('/donate', methods=['POST'])
def donate():
    try:
        # Get form data
        donor_type = request.form.get('donor-type')
        name = request.form.get('name')
        email = request.form.get('email')
        delivery_type = request.form.get('delivery-type')
        city = request.form.get('city')  # Fetch city from hidden input
        center_id = request.form.get('center_id')  # Optional

        # Combine categories and quantities into a single string
        categories = request.form.getlist('categories[]')
        donation_details = []
        if categories:
            quantities = {
                'clothes': request.form.get('quantity_clothes', 0),
                'necessary items': request.form.get('quantity_items', 0),
                'food': request.form.get('quantity_food', 0),
                'healthcare products': request.form.get('quantity_healthcare', 0)
            }

            for category in categories:
                quantity = int(quantities.get(category, 0))
                if quantity > 0:
                    donation_details.append(f"{category}: {quantity}")

        donation_summary = "; ".join(donation_details)

        # Insert the entry into the database
        cur = mysql.connection.cursor()
        query = """
            INSERT INTO donations (donor_type, name, email, donation_details, delivery_type, city)
            SELECT %s, %s, %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM donations
                WHERE name = %s AND email = %s AND donation_details = %s AND delivery_type = %s AND city = %s
            )
        """
        cur.execute(query, (
            donor_type, name, email, donation_summary, delivery_type, city,
            name, email, donation_summary, delivery_type, city
        ))

        mysql.connection.commit()
        cur.close()

        # Redirect to success message
        return render_template('message.html', message=f"Thank you for your donation, {name} !")

    except Exception as e:
        print(f"Error: {e}")
        return render_template('message.html', message="Some error occurred, please try again later.")

    
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

app.run(debug=True)