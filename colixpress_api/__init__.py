from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy_core import FlaskSQLAlchemy
from sqlalchemy import MetaData
from flask import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@0.0.0.0/bdd_colixpress'
db = FlaskSQLAlchemy(app.config['SQLALCHEMY_DATABASE_URI'])
metadata = MetaData(bind=db)

auth = HTTPBasicAuth()

app.config['SECRET_KEY'] = ''

from colixpress_api import routes