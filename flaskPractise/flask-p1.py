# -*- coding: utf-8 -*-
from flask import Flask,flash,render_template,redirect
from flask_script import Manager


app = Flask(__name__)

# app.config["SECRET_KEY"] = "meimeida"
app.secret_key = "meimeidada"
app.template_folder = "templates"
@app.route('/')
def index():
    flash("my first flask app")
    # return render_template("index.html")
    return redirect('/user/Root')

@app.route('/user/<name>')
def user(name):
    flash("hello %s this is flask app" % name)
    return render_template("index.html")

manager = Manager(app)
manager.run()