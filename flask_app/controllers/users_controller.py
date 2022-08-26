from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app.models.book_model import Books
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

# HOME PAGE - I am
@app.route('/')
def index():
    return render_template("index.html") 

def logged_in():
    return session.get('first_name') and session.get('user_id')

# FORM PAGE - where to login/register
@app.route('/quote/login')
def form_page():
    # if user is logged in, they should be redirected to the dashboard page
    # if not "user_id" in session:
    #     return redirect('/dashboard')
    return render_template("form_page.html")

# REGISTER 
@app.route('/register', methods=["POST"])
def register():
    # Get all the data that was submitted into our form
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]

    # validate the data tha we awere given
    if not User.validate_reg(request.form, "register"):
        return redirect('/quote/login')

    # Did they submit an already registered email
    user = User.get_by_email({'email': email})
    if user != False:
        flash("invalid email/password", "register")
        return redirect("/quote/login")

    #encrypt our password
    password = bcrypt.generate_password_hash(password)

    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password
    }
    # create the new user and store their ssession data: logging them in
    session['user_id'] = User.create(data)
    session['first_name'] = first_name
    return redirect('/dashboard')

# LOGIN 
@app.route('/login', methods=["POST"])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/quote/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/quote/login')
    # validate email exists 
    #validate passwords matches
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    user = User.get_by_id({'id':session['user_id']})
    return redirect('/dashboard')
    # return render_template("dashboard.html", user=user)

# DASHBOARD - books can be searched
@app.route('/dashboard')
def dashboard():
    if not "user_id" in session:
        return redirect('/quote/login')
    user = User.get_by_id({'id':session['user_id']})
    return render_template("dashboard.html", user=user)

@app.route('/my_books')
def my_books():
    if not "user_id" in session:
        return redirect('/quote/login')
    user = User.get_by_id({'id':session['user_id']})
    return render_template('create.html', user=user)


# END SESSION, LOG OUT, RETURN TO HOME, DON'T SAVE INFO
@app.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('first_name')
    return redirect('/')


