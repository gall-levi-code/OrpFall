from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/select', methods=['post'])
def selected():

    name = request.form.get("name")
    selection = request.form.get("Character")

    if not name or not selection:
        return "failure"
    return render_template("successful.html")

# @app.route('/reject')
# def rejects():