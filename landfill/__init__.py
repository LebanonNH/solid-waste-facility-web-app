import os
import base64
import boto3
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

load_dotenv()

aws_secret_key_id = os.getenv("AWS_SECRET_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
def get_secret(secret_name, region_name="us-east-2"):

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    if secret:
        return secret
    elif decoded_binary_secret:
        return decoded_binary_secret
            


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
    else:
        db_url += ":" + get_secret('DB_PASS', 'us-east-2')
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