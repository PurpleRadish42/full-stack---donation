from flask import *
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'   
app.config['MYSQL_PASSWORD'] = '@Bhijit6151'
app.config['MYSQL_DB'] = 'donation'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')
