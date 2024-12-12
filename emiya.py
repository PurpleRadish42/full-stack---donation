from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'emiya_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password, role FROM login WHERE username=%s", [username])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            session['id'] = user[0]
            session['username'] = username
            session['role'] = user[2]
            if role == user[2]:
                if role == 'admin':
                    return redirect(url_for('dashboard'))
                elif role == 'user':
                    return redirect(url_for('home'))
            else:
                flash('Invalid role selection.')
        else:
            flash('Invalid username or password.')

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

        flash('Registration successful. Please log in.')
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

if __name__ == '__main__':
    app.run(debug=True)

