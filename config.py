# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "files_uploaded")
EXCEL_FOLDER = os.path.join(BASE_DIR, "excel_files")

# Define the database - we are working with
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'