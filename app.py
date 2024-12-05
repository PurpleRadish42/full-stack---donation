from flask import *
from flask_mysqldb import MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'   
# app.config['MYSQL_PASSWORD'] = '@Bhijit6151'
# app.config['MYSQL_DB'] = 'donation'

# mysql = MySQL(app)\

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


app.run(debug=True)

