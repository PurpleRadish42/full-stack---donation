from flask import*
app = Flask(__name__)
@app.route('/login', methods=['GET', 'POST'])
def login():
    # verify various logins from database
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return redirect(url_for('success'))
        else:
            abort(401)
    else:
        return render_template('login.html')
@app.route('/success')
def success():
    return 'Logged in successfully'
from flask import Flask, url_for

app = Flask(__name__)

@app.route('/logo')
def logo():
    return render_template('logo.html')
app.run(debug=True)


