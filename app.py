#. .venv/bin/activate
# flask --app app.py --debug run
from cs50 import SQL
from flask import Flask, jsonify, render_template, request, redirect
from datetime import date

app = Flask(__name__)

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
        return render_template("comment_form_err.html")

    else:
        print(img, name, comment)
        db.execute("INSERT INTO messages (name, comment, img, date) VALUES (?, ?, ?, ?)", name, comment, img, date_now)
        return redirect("/messages")

    # https://api.github.com/users/{username}}


@app.route("/error")
def errormsg():
    return render_template("comment_form_err.html")
# @app.route("/comments")
# def index():
#     return render_template("index.html")

# @app.route("/login")
# def index():
#     return render_template("index.html")

# @app.route("/register")
# def index():
#     return render_template("index.html")