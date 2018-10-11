#!/usr/bin/python
import json
import settings
from Models import Media
# from flask_caching import Cache
from flask import Flask, jsonify, render_template

# Create an instance of the application
app = Flask(__name__, template_folder='templates')
IP = settings.server_ip
PORT = settings.server_port


@app.route('/', methods=['GET'])
def mainRoute():
    return jsonify({'Error': "Sorry, Neither is an authenticated user, nor a valid key is entered!"})


@app.route('/<media_type>/<movie_id>', methods=['GET'])
def getMovieByID(media_type, movie_id):
    result = json.loads(Media.retrieve(_id=movie_id, key='media type', value=media_type))
    if result:
        return jsonify(result)
    else:
        return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})


@app.route('/search/query=<title>', methods=['GET'])
def searchMediaByKeyValue(title):
    result = json.loads(Media.retrieve(_id=None, key='title', value=title))
    if result:
        return jsonify(result)
    else:
        return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})


@app.route('/search/query=<key>:<value>', methods=['GET'])
def searchMediaByQuery(key, value):
    r = Media.retrieve(_id=None, key=key, value=value)

    if len(r) == 1:
        result = json.loads(r)
        return jsonify(result)
    elif len(r) > 1:
        output = []
        for i in r:
            t = json.loads(i)
            output.append(t)
        return output
    else:
        return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})


if __name__ == '__main__':
    app.run(host=IP, port=PORT, debug=True)
