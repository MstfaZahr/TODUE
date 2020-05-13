from flask import Flask, redirect, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return " "


@app.route("/sign-in")
def signin():
    return render_template("sign-in.html")


@app.route("/sign-up")
def signup():
    return render_template("sign-up.html")

@app.route("/todues")
def todues_index():
    return render_template("todues.html")

if __name__ == "__main__":
    app.run(debug=True)