#. .venv/bin/activate
# flask --app app.py --debug run
from cs50 import SQL
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saythanks")
def chooseImg():
    return render_template("choose_img.html")

@app.route("/saythanks/comment")
def sendComment():
    return render_template("form.html")

@app.route("/comments")
def checkComments():
    return render_template("comments.html")
# @app.route("/comments")
# def index():
#     return render_template("index.html")

# @app.route("/login")
# def index():
#     return render_template("index.html")

# @app.route("/register")
# def index():
#     return render_template("index.html")