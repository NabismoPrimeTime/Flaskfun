from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta


app = Flask(__name__)



@app.route("/", methods=['POST','GET'])
def index():
    if request.method == "POST":
        user = request.form["ent"]
        print(user)
        return render_template('base.html')
    return render_template('index.html')

"""@app.route("/entry", methods=["POST", "GET"])
def entry():
    if request.method == "POST":
        user = request.form["ent"]
        print(user)
        return render_template('base.html')
"""
if __name__ == "__main__":
    app.run(debug=True)