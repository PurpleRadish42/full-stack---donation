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

@app.route('/center1')
def center1():
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
        return render_template('center1.html', center=center)  # Pass a single center object
    else:
        return render_template('message.html', message="Center not found.")

@app.route('/donation')
def donation():
    return render_template('donation.html')

app.run(debug=True)