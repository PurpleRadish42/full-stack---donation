from flask import *
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'   
app.config['MYSQL_PASSWORD'] = '@Bhijit6151'
app.config['MYSQL_DB'] = 'donation'

mysql = MySQL(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/locateus')
def locateus():
    return render_template('locateus.html')

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

    cur.close()

    # Render data into the HTML template
    return render_template(
        'dashboard.html',
        monetary_data=monetary_data,
        special_data=special_data,
        joiners_data=joiners_data,
    )

app.run(debug=True)

