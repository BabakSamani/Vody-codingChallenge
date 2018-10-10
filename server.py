#!/usr/bin/python
from Models import Media
from flask_caching import Cache
from flask import Flask, jsonify, render_template

# Create an instance of the application
app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
def mainRoute():
    return jsonify({'Error': "Sorry, Neither is an authenticated user, nor a valid key is entered!"})


@app.route('/movie/id=<movie_id>', methods=['GET'])
def getMovieByID(movie_id):
    return Media.retrieve(_id=movie_id, key='media type', value='movie')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
