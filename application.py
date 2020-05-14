from flask import Flask, redirect, render_template, url_for, request
from functools import wraps

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.user is None:
            return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/sign-in")
def signin():
    return render_template("sign-in.html")

@app.route("/sign-up")
def signup():
    return render_template("sign-up.html")

@app.route("/todues")
@login_required
def todues_index():
    return render_template("todues.html")

if __name__ == "__main__":
    app.run(debug=True)