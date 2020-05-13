import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DB_TYPE')
db_path = os.getenv('DB_PATH')
db_name = os.getenv('DB_NAME')
if not db_url:
    raise ValueError('please set environmental variable DB_TYPE to type of DB to be used. Ex. "sqlite", "mysql", etc')
if not db_path:
    raise ValueError('please set environmental variable DB_PATH to the database path. Ex. local sqlite db "//data.db" or remote "db.example.com"')
if os.getenv('DB_DRIVER'):
    db_url = db_url + "+" + os.getenv('DB_DRIVER')
db_url += "://"

if os.getenv('DB_USER'):
    db_url += os.getenv('DB_USER')
    if os.getenv('DB_PASS'):
        db_url += ":" + os.getenv('DB_PASS')
    db_url += "@"

db_url += db_path
if db_url:
    db_url += "/" + db_name
print(db_url)
app = Flask(__name__)
app.config['SECRET_KEY'] =  os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

from landfill import routes