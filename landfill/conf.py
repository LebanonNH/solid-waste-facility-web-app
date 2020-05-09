import os
from dotenv import load_dotenv
load_dotenv()

db_path = os.getenv("DB_PATH")
db_user = os.getenv("DB_USER")
db_passwd = os.getenv("DB_PASSWORD")
secret_key = os.getenv("SECRET_KEY")