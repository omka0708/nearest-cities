from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DADATA_API_KEY = os.environ.get("DADATA_API_KEY")
DADATA_SECRET_KEY = os.environ.get("DADATA_SECRET_KEY")
