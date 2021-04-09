# -*- coding: utf-8 -*-
import flask

app = flask.Flask(__name__)


@app.route('/')
def index_page():
    return 'index page'


@app.route('/hello')
def hello():
    return 'hello world!'


@app.route('/user/<username>')
def show_user(username):
    return 'Hi! User: %s ' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post: %d' % post_id


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()


def do_the_login():
    return 'login in'


def show_the_login_form():
    return 'start to login'


app.run()
