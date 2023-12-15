#. .venv/bin/activate
# flask --app app.py --debug run
from cs50 import SQL
from flask import Flask, jsonify, render_template, session, request, redirect
from flask_session import Session
from datetime import date, datetime 
import bcrypt

from helpers import login_required

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
    return render_template("comments.html")

@app.route("/messages/api")
@login_required
def loadComments():
    messages = db.execute("SELECT * FROM messages ORDER BY date DESC, time DESC")
    return jsonify(messages)

@app.route("/send", methods=["POST"])
@login_required
def sendComment():
    img = request.form.get("img")
    name = request.form.get("name")
    comment = request.form.get("comment")

    # get date
    date_now = date.today()
    # get time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time_now = current_time

    if name == "" or comment == "":
        err = "400"
        message = "Must add name and comment."
        print("All fields must be filled")
        return render_template("err/err_layout.html", err=err, message=message)
    
    if img == "none":
        err = "400"
        message = "Must select an image."
        print("All fields must be filled")
        return render_template("err/err_layout.html", err=err, message=message)

    else:
        print(img, name, comment)
        db.execute("INSERT INTO messages (name, comment, img, date, time, user_id) VALUES (?, ?, ?, ?, ?, ?)", name, comment, img, date_now, time_now, session["user_id"])
        return redirect("/messages")

@app.route("/myprofile")
@login_required
def myprofile():
    userData = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    userComments = db.execute("SELECT * FROM messages WHERE user_id=?", session["user_id"])
    print(userData[0])
    return render_template("myprofile.html", userData=userData, userComments=userComments)

@app.route("/myprofile/users/api")
@login_required
def loadUsers():
    users = db.execute("SELECT username FROM users")
    return jsonify(users)

@app.route("/delete-comment", methods=["POST"])
@login_required
def deleteComment():
    comment_id = request.form.get("comment_id")

    find_comment = db.execute("SELECT * FROM messages WHERE id=?", comment_id)
    if not find_comment:
        message="Comment not found."
        err="403"
        return render_template("err/err_layout.html", message=message, err=err)

    db.execute("DELETE FROM messages WHERE id=?", comment_id)
    userData = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    userComments = db.execute("SELECT * FROM messages WHERE user_id=?", session["user_id"])
    
    return render_template("myprofile.html", userData=userData, userComments=userComments)


################################################################ AUTH ################################################################

################################ LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        if not username or not password:
            message="Must enter a valid username & password"
            err="403"
            return render_template("err/err_layout.html", message=message, err=err)

        # find username in db
        usernameInDB = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists (WE MUST GET ONLY 1 ROW = 1 UNIQUE USERNAME) and password is correct
        if len(usernameInDB) != 1: 
            message="Username not found in database."
            err="403"
            return render_template("err/err_layout.html", message=message, err=err)

        # select password of username
        hash_password = usernameInDB[0]["hash"]

        # check password hash
        check_password_hash = bcrypt.checkpw(password.encode(), hash_password)

        if not check_password_hash:
            message="Incorrect password."
            err="403"
            return render_template("err/err_layout.html", message=message, err=err)

        # Remember which user has logged in -> keep track of info; store current user ID
        session["user_id"] = usernameInDB[0]["id"]

        # Redirect user to profile
        return redirect("/myprofile")

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
        passconfirm = request.form.get("passconfirm")

        # Ensure username was submitted
        if not username:
            message = "Must fill out all fields."
            err= "400"
            return render_template("err/err_layout.html", message=message, err=err)

        # Ensure password was submitted
        elif not password or not passconfirm:
            message = "Must fill out all fields."
            err= "400"
            return render_template("err/err_layout.html", message=message, err=err)

        # check if username exists
        elif db.execute("SELECT * FROM users WHERE username = ?", username):
            message = "Username already taken :("
            err= "400"
            return render_template("err/err_layout.html", message=message, err=err)

        # check password is confirmed
        elif password != passconfirm:
            message = "Password must be the same as confirmation."
            err= "400"
            return render_template("err/err_layout.html", message=message, err=err)


        # Generate a salt
        salt = bcrypt.gensalt() 

        # hash password
        hash = bcrypt.hashpw(password.encode(), salt)
        print(hash)

        # insert data in users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # store session
        user_data = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = user_data[0]["id"]

        return redirect("/saythanks")

    # GET -> display form to register
    else:
        return render_template("register.html")
