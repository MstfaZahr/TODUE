import os
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = sqlite3.connect('todo.db')
db = conn.cursor()

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/sign-in", methods=["GET", "POST"])
def login():
    
    session.clear()
    
    if request.method == "GET":
        return render_template("sign-in.html")

    else:
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username=?", username)
        conn.commit()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/sign-up", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("sign-up.html")
    
    else:

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("You must choose a username", 403)
        elif not password:
            return apology("You must choose a password", 403)
        elif password != request.form.get("confirmation"):
            return apology("Passwords do not match", 403)

        checkAvailableUser = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        if len(checkAvailableUser) != 0:
            return apology("Sorry! Username is already taken.", 403)

        passwordHash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, passwordHash)
        conn.commit()

        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)