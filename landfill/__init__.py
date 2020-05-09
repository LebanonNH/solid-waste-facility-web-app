from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from landfill.conf import db_path, secret_key


app = Flask(__name__)
app.config['SECRET_KEY'] =  secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
db = SQLAlchemy(app)

from landfill import routes