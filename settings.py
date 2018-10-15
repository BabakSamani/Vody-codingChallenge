# settings.py
# A python script to read the .env file and read the required parameters from this file to pass to other parts of the
# application
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Accessing database variables.
host = os.getenv('MONGO_DB_HOST')
port = os.getenv('MONGO_DB_PORT')
database = os.getenv('MONGO_DB_NAME')
collection = os.getenv('MONGO_COLLECTION')

# API URLs with two different keys
api_url_1 = os.getenv('MEDIA_API_URL_1')
api_url_2 = os.getenv('MEDIA_API_URL_2')

# Server configuration
server_ip = os.getenv('HOST_IP')
server_port = os.getenv('HOST_PORT')

# User's token for using this api
user_token = os.getenv('API_USER_TOKEN')