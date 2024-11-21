from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "f2b6e36d3e61c78ba849aef749f6c94c3ed948b8f3ec7f9c4329347b0b1e5c7e"

def db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Deep@$915736",
        db="auth_system",
        cursorclass=pymysql.cursors.DictCursor
    )
    
    
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/")
def signup():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def handle_signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']


    if password != confirm_password:
        flash("Passwords do not match! Please try again.", "error")
        return redirect(url_for('signup'))


    hashed_password = generate_password_hash(password)


    connection = db_connection()
    cursor = connection.cursor()
    try:
    
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        connection.commit()
        flash("Signup successful! Please login.", "success")
        return redirect(url_for('login'))
    except pymysql.err.IntegrityError:
    
        flash("Email already exists! Please try logging in.", "error")
        return redirect(url_for('signup'))
    finally:
        cursor.close()
        connection.close()

        
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email, ))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if user and check_password_hash(user["password"], password):
            flash("Login successful!")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password! Please try again", "error")
            return redirect(url_for("login"))
        
    return render_template("login.html")

@app.route('/logout')
def logout():
    """Log out the user."""
    session.pop('user_id', None) 
    flash("You have been logged out.", "success") 
    return redirect(url_for('login')) 

if __name__ == "__main__":
    app.run(debug=True)