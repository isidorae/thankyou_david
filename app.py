#. .venv/bin/activate
# flask --app app.py --debug run
from cs50 import SQL
from flask import Flask, jsonify, render_template, session, request, redirect
from flask_session import Session
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///thankyou.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saythanks")
def chooseImg():
    return render_template("choose_img.html")

@app.route("/messages")
def checkComments():
    messages = db.execute("SELECT * FROM messages ORDER BY date")
    print(messages)
    return render_template("comments.html", messages=messages)

@app.route("/messages/api")
def loadComments():
    messages = db.execute("SELECT * FROM messages ORDER BY date DESC")
    return jsonify(messages)

@app.route("/send", methods=["POST"])
def sendComment():
    img = request.form.get("img")
    name = request.form.get("name")
    comment = request.form.get("comment")

    # get date
    date_now = date.today()


    if name == "" or comment == "" or img =="none":
        print("All fields must be filled")
        return render_template("err/comment_form_err.html")

    else:
        print(img, name, comment)
        db.execute("INSERT INTO messages (name, comment, img, date) VALUES (?, ?, ?, ?)", name, comment, img, date_now)
        return redirect("/messages")

    # https://api.github.com/users/{username}}

@app.route("/myprofile")
def myprofile():
    return render_template("myprofile.html")

@app.route("/error")
def errormsg():
    return render_template("err/comment_form_err.html")


################################################################ AUTH ################################################################

################################ LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            message="Must enter a valid username & password"
            err="403"
            return render_template("err/login_form_error.html", message=message, err=err)

        # find username in db
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists (WE MUST GET ONLY 1 ROW = 1 UNIQUE USERNAME) and password is correct
        if len(rows) != 1: 
            message="Username not found in database."
            err="403"
            return render_template("err/invalid_login.html")
        
        if not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            message="Incorrect password."
            err="403"
            return render_template("err/invalid_login.html")

        # Remember which user has logged in -> keep track of info; store current user ID
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


################################ LOGOUT
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


################################ REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # POST -> check errors & submit data to table database -> log user in
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        passconfirm = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            message = "Must fill out all fields."
            err= "400"
            return render_template("err/register_form_err.html", message=message, err=err)

        # Ensure password was submitted
        elif not password or not passconfirm:
            message = "Must fill out all fields."
            err= "400"
            return render_template("err/register_form_err.html", message=message, err=err)

        # check if username exists
        elif db.execute("SELECT * FROM users WHERE username = ?", username):
            message = "Username already taken :("
            err= "400"
            return render_template("err/register_form_err.html", message=message, err=err)

        # check password is confirmed
        elif password != passconfirm:
            message = "Password must be the same as confirmation."
            err= "400"
            return render_template("err/register_form_err.html", message=message, err=err)

        # hash password
        hash = generate_password_hash(password)

        # insert data in users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # store session
        user_data = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = user_data[0]["id"]

        return redirect("/")

    # GET -> display form to register
    else:
        return render_template("register.html")
