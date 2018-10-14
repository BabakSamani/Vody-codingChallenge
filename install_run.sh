#!/usr/bin/env bash
echo "Checking Python3 version..."
python -V

echo "Installing python pip for package installation..."
sudo apt-get install python-pip

echo "Installing required packages..."
pip install pymongo requests python-dotenv flask flask_caching

echo "Installing mongodb...."
sudo apt-get update
sudo apt-get install -y mongodb

echo "Creating logs directory"
mkdir logs

echo "Setting up the database"
python setupDatabase.py

echo "Running the server ..."
python server.py