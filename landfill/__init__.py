import os
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

load_dotenv()

# Set root user info for webapp
bcrypt = Bcrypt()

root_user = ""
root_password = ""

if os.getenv('ROOT_USER'):
    root_user = os.getenv('ROOT_USER')

if os.getenv('ROOT_PASSWORD'):
    root_password = bcrypt.generate_password_hash(os.getenv('ROOT_PASSWORD')).decode('utf-8')


# Setup DB Connection 
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

tls_cert = os.getenv('DB_TLS_CERT')
if tls_cert:
    db_url += "?ssl_ca=" + os.path.join(os.getcwd(), 'landfill/', tls_cert)

print(db_url)

#Setup App
app = Flask(__name__)
app.config['SECRET_KEY'] =  os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

#setup login manager
login_manager = LoginManager(app)


from landfill import routes
login_manager.unauthorized_handler(routes.login)