from flask import *
from flask_mysqldb import MySQL


app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'   
app.config['MYSQL_PASSWORD'] = '@Bhijit6151'
app.config['MYSQL_DB'] = 'donation'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/center1')
def center1():
    return render_template('center1.html')

@app.route('/donate', methods=['POST'])
def donate():
    try:
        # Get form data
        donor_type = request.form.get('donor-type')
        name = request.form.get('name')
        email = request.form.get('email')
        delivery_type = request.form.get('delivery-type')

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

        donation_summary = "; ".join(donation_details)  # Combine details into a single string

        # Insert the single entry into the database if not already present
        cur = mysql.connection.cursor()
        query = """
            INSERT INTO donations (donor_type, name, email, donation_details, delivery_type)
            SELECT %s, %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM donations
                WHERE name = %s AND email = %s AND donation_details = %s AND delivery_type = %s
            )
        """
        cur.execute(query, (
            donor_type, name, email, donation_summary, delivery_type,
            name, email, donation_summary, delivery_type
        ))

        mysql.connection.commit()
        cur.close()

        # Redirect to message.html with success message
        return render_template('message.html', message="Thank you for your donation!")

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

app.run(debug=True)