import os

from config import UPLOAD_FOLDER, JSON_FOLDER, LOG_FOLDER

from database.init_db import create_database, create_tables

def initialize():
    # Create necessary directories if they don't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(JSON_FOLDER, exist_ok=True)
    os.makedirs(LOG_FOLDER, exist_ok=True)

    # Create the database and tables
    create_database()
    create_tables()

    print("Initialization complete. Directories created and database setup done.")