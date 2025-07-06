from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@ssword1'
app.config['MYSQL_DB'] = 'to_dos'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("Received email:", email)
        print("Received password:", password)

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users2 WHERE email=%s AND password=%s", (email, password))
        account = cursor.fetchone()
        cursor.close()

        print("Query result:", account)

        if account:
            return "✅ Login successful!"
        else:
            return "❌ Incorrect email or password."

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
