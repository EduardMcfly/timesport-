import os

from flask import Flask, jsonify, render_template, url_for

from database import db, getSession, migrate
from models import *
from utils import ext

static_url_path = '/static'
app = Flask(__name__, static_url_path=static_url_path)

for extension in [ext.JinjaStatic, ext.JinjaUrl]:
    # pylint: disable=no-member
    app.jinja_env.add_extension(extension)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'development' == app.env

db.init_app(app)
migrate.init_app(app)


@app.context_processor
def inject_dict_for_all_templates():
    return dict(
        static=lambda path: url_for('static', filename=path),
        url=lambda path: url_for(path)
    )


@app.route("/")
def index():
    return "Hello, World!"


def query_to_dict(ret):
    if ret is not None:
        return [{key: value for key, value in row.items()} for row in ret if row is not None]
    else:
        return []


@app.route("/login/")
@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/signUp")
def signUp():
    return render_template('signUp.html')


@app.route("/users")
def users():
    session = getSession()
    connection = session.connection()
    results = connection.execute('SELECT * FROM users')
    users = query_to_dict(results)
    return render_template('users.html', users=users)


@app.route("/competencias")
def competencias():
    session = getSession()
    connection = session.connection()
    results = connection.execute('SELECT * FROM competencia')
    competencias = query_to_dict(results)
    return render_template('competencias.html', competencias=competencias)
 
