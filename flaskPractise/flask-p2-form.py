# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = StringField('what is your name', validators=[Required()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.secret_key = "meimeidada"
app.template_folder = "templates"


bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    nameForm = NameForm()
    if nameForm.validate_on_submit():
        session['name'] = nameForm.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=nameForm, name=session.get('name'))

app.run(debug=True)
