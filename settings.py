# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Accessing variables.
host = os.getenv('MONGO_DB_HOST')
port = os.getenv('MONGO_DB_PORT')
database = os.getenv('MONGO_DB_NAME')
collection = os.getenv('MONGO_COLLECTION')

api = os.getenv('API_KEY')