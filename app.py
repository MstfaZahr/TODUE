from flask import Flask, redirect, render_template, url_for, request, session, flash
from functools import wraps

app = Flask(__name__)

''' a decorater to require user to login to access site '''
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.user is None:
            return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/sign-in", methods = ["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("sign-in.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        return redirect("todos.html")

@app.route("/sign-up", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("sign-up.html")
    else:
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]

        ''' validates inputted data '''
        if not username or not password:
            return render_template("error.html", error="You must enter a username and a password")
        elif not username.isalnum():
            return render_template("error.html", error="Your username must only contain characters and numbers")
        elif len(password) < 8:
            return render_template("error.html", error="Your password must be longer than 8 characters")
        elif " " in password:
            return render_template("error.html", error="Your password can't contain spaces")
        elif not password == confirmation:
            return render_template("error.html", error="Your passwords do not match")

        return redirect(url_for("signin"))

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("signin"))

if __name__ == "__main__":
    app.run()