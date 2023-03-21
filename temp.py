from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = "secret_key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            if bcrypt.checkpw(password, user[2].encode('utf-8')):
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                return redirect('/dashboard')
            else:
                error = 'Invalid email or password.'
                return render_template('login.html', error=error)
        else:
            error = 'Invalid email or password.'    
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        confirm_password = request.form['confirm_password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if user:
            error = 'Email already exists.'
            return render_template('register.html', error=error)
        elif password != confirm_password:
            error = 'Passwords do not match.'
            return render_template('register.html', error=error)
        else:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password,))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_name = session['user_name']
        return render_template('dashboard.html', user_id=user_id, user_name=user_name)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
