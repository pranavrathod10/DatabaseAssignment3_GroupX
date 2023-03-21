# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')

# def index():
#     return 'Hello'

# @app.route('/book')

# def book_search():
#     cur = 

# if __name__ == '__main__':
#     app.run(debug = True)

from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
# Configure db
db = yaml.safe_load(open('E:\VScode_files\Database assignment\CS432_Database\db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        email = request.values.get("email")
        password = request.values.get('password').encode('utf-8')
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login_db WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        print(user)
        passcode = 0
        if 1:
            if user: 
                passcode = user[1].encode('utf-8')

            if password == passcode:
                session['user_name'] = user[0]
                return redirect('/DBMS')
            else:
                # error = 'Invalid email or password.'
                return redirect('/dbmsuser')
        # else:
        #     error = 'Invalid email or password.'    
        #     return render_template('loginpage.html', error=error)

    return render_template('loginpage.html')

@app.route('/dbmsuser', methods=['GET', 'POST'])
def dbms():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        book_name = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("select * from book where title = '" + book_name + "';")  #LIKE '" + name + "%';
        if resultValue > 0:
            temp = cur.fetchall()
            return render_template('books.html', rows = temp)
        
        mysql.connection.commit()
        cur.close()
        return 'not'
    return render_template('dbmsuser.html')

@app.route('/DBMS', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        book_name = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("select * from book where title = '" + book_name + "';")  #LIKE '" + name + "%';
        if resultValue > 0:
            temp = cur.fetchall()
            return render_template('books.html', rows = temp)
        
        mysql.connection.commit()
        cur.close()
        return 'not'
    return render_template('DBMS.html')

@app.route('/books', methods =['GET', 'POST'])
def book():
    if request.method == 'GET':
        cur  = mysql.connection.cursor()
        resultvalue = cur.execute("SELECT * from book")
        if(resultvalue > 0):
            userDetails =  cur.fetchall()
        return render_template('users.html',  userDetails = userDetails)

@app.route('/libuser', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        resultvalue = cur.execute("SELECT * from users")
        if resultvalue > 0:
            userDetails = cur.fetchall()
            return render_template('libuser.html', userDetails=userDetails)
        else:
            return "No users found."
    return render_template('libuser.html')

# @app.route('/rename', methods=['GET', 'POST'])
# def rename():
#     if request.method == 'POST':
#         userDetails = request.form
#         old_col_name = userDetails['old_col_name']
#         new_col_name = userDetails['new_col_name']
#         cur = mysql.connection.cursor()
#         cur.execute("ALTER TABLE `users` RENAME COLUMN `%s` TO `%s`;", [old_col_name, new_col_name])
#         mysql.connection.commit()
#         cur.close()
#         return redirect('/libuser')
#     return render_template('rename.html')

@app.route('/rename', methods=['GET', 'POST'])
def rename():
    if request.method == 'POST':
        userDetails = request.form
        old_col_name = userDetails['old_col_name']
        new_col_name = userDetails['new_col_name']
        cur = mysql.connection.cursor()
        cur.execute("ALTER TABLE `users` RENAME COLUMN `old_col_name` TO `new_col_name`;", [])
        mysql.connection.commit()
        cur.close()
        render_template('libuser.html')
        return redirect('/libuser')
    return render_template('rename.html')


    # if request.method == 'POST':
    #     userDetails = request.form
    #     name = userDetails['name']
    #     email = userDetails['email']
    #     cur  = mysql.connection.cursor()
    #     cur.execute(" INSERT INTO user(name, email) VALUES(%s,%s)" , (name, email))
    #     mysql.connection.commit()
    #     cur.close()

# @app.route('/add', methods =['GET', 'POST'])
# def add():
#     if request.method == 'POST':
#         userDetails = request.form
#         book_name = userDetails['title']
#         book_id = userDetails['book_id']
#         edition = userDetails['edition']
#         copies = userDetails['copies']
#         availaibility = userDetails['availaibility']
#         author_id = userDetails['author_id']
#         cur  = mysql.connection.cursor()
#         cur.execute(" INSERT INTO book(book_id, book_name, edition, copies, availaibility, author_id) VALUES(%s,%s, %s,%s, %s,%s )" , (book_id, book_name, edition, copies, availaibility, author_id))
#         mysql.connection.commit()
#         cur.close()
#         return redirect("/books")

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        userDetails = request.form
        book_id = userDetails['book_id']
        title = userDetails['title']
        edition = userDetails['edition']
        copies = userDetails['copies']
        Availability_status = userDetails['Availability_status']
        author_id = userDetails['author_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO book(book_id, title, edition, copies, Availability_status, author_id) VALUES(%s,%s,%s,%s,%s,%s)", (book_id, title, edition, copies, Availability_status, author_id))
        mysql.connection.commit()
        cur.close()
        return redirect('/books')
    return render_template('add.html')

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        userDetails = request.form
        book_id = userDetails['book_id']

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM book WHERE book_id = %s", [book_id])
        mysql.connection.commit()
        cur.close()
        return redirect("/books")
    return render_template('delete.html')


# @app.route('/updateuser', methods=['POST', 'GET'])
# def delete():
#     if request.method == 'POST':
#         userDetails = request.form
#         UserID = userDetails['UserID']
#         upt = userDetails['Contact']
#         cur = mysql.connection.cursor()
#         cur.execute("UPDATE users SET Contact = %s WHERE UserID = %s ", [upt,UserID])

#         mysql.connection.commit()
#         cur.close()
#         return redirect("/libuser")
#     return render_template('updateuser.html')

@app.route('/updateuser', methods=['POST', 'GET'])
def update_user():
    if request.method == 'POST':
        userDetails = request.form
        UserID = userDetails['UserID']
        Contact = userDetails['Contact']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE UserID = %s", [UserID])
        user = cur.fetchone()

        if user:
            cur.execute("UPDATE users SET Contact = %s WHERE UserID = %s", [Contact, UserID])
            mysql.connection.commit()
            cur.close()
            flash('User updated successfully!', 'success')
            return redirect("/libuser")
        else:
            flash('User ID not found!', 'error')
            return redirect("/updateuser")

    return render_template('updateuser.html')


@app.route('/authors')
def authors():
    cur  = mysql.connection.cursor()
    resultvalue = cur.execute("SELECT * from author")
    if(resultvalue > 0):
        userDetails =  cur.fetchall()
    return render_template('authors.html',  userDetails = userDetails)


# @app.route('/books')
# def books():
#     cur = mysql.connection.cursor()
#     resultValue = cur.execute("SELECT * FROM books")
#     if resultValue > 0:
#         userDetails = cur.fetchall()
#         return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)

