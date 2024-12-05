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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard2.html')

@app.route('/get_data/<category>', methods=['GET'])
def get_data(category):
    # Map categories to table names
    table_mapping = {
        "monetary": "monetary",
        "special": "special",
        "joiners": "joiners"
    }
    table_name = table_mapping.get(category)
    if not table_name:
        return jsonify([])

    # Query the database
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    rows = cur.fetchall()

    # Get column names
    column_names = [desc[0] for desc in cur.description]

    # Convert the result to a list of dictionaries
    results = [dict(zip(column_names, row)) for row in rows]
    cur.close()
    return jsonify(results)

app.run(debug=True)

