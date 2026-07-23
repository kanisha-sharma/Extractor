import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")

# Encode special characters like @, #, %, !
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
JSON_FOLDER = os.getenv("JSON_FOLDER")
LOG_FOLDER = os.getenv("LOG_FOLDER")

DATABASE_URL = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")