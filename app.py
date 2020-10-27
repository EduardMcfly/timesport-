import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request, url_for
from sqlalchemy.sql import text

from blueprints import trainigBp, signUpBp, trackBp
from database import db, getSession, migrate
from models import *
from utils import ext, query_to_dict
from blueprints.competence import competenceBp


static_url_path = '/static'
app = Flask(__name__, static_url_path=static_url_path)

app.register_blueprint(competenceBp)

for extension in [ext.JinjaStatic, ext.JinjaUrl]:
    # pylint: disable=no-member
    app.jinja_env.add_extension(extension)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'development' == app.env
print(os.getenv('DATABASE_URL'))
print(os.getenv('SECRET_KEY'))
db.init_app(app)
migrate.init_app(app)

app.register_blueprint(trainigBp)
app.register_blueprint(signUpBp)
app.register_blueprint(trackBp)


@app.template_filter('date_format')
def filter_datetime(value: datetime, fmt="%Y:%M:%d"):
    return value.strftime(fmt)


@app.context_processor
def inject_dict_for_all_templates():
    return dict(
        static=lambda path: url_for('static', filename=path),
        url=lambda path: url_for(path)
    )


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/login/")
@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/users")
def users():
    session = getSession()
    connection = session.connection()
    results = connection.execute(
        'SELECT id as id_user, name as name_user, password, created_at FROM users'
    )
    users = query_to_dict(results)
    return render_template('users.html', users=users)
