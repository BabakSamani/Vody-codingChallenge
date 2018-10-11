#!/usr/bin/env bash
echo "Checking Python3 version..."
python -V

echo "Installing python pip for package installation..."
sudo apt-get install python-pip

echo "Installing required packages..."
pip install bson
pip install pymongo
pip install requests
pip install python-dotenv
pip install flask
pip install flask_caching

echo "Installing mongodb...."
sudo apt-get update
sudo apt-get install -y mongodb

