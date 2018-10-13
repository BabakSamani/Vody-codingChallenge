#!/usr/bin/python
import json
import settings
from Models import Media
from Logger import Logger
# from flask_caching import Cache
from flask import session, redirect, url_for, escape
from flask import Flask, jsonify, render_template, request


# Create an instance of the application
app = Flask(__name__, template_folder='views')

# Define server IP and port number
IP = settings.server_ip
PORT = settings.server_port

logger = Logger()


@app.route('/', methods=['GET'])
@app.route('/api/', methods=['GET'])
def mainRoute():
    try:
        print(request.path)
        return render_template('index.html', title="Home|API")
        # return jsonify({'Error': "Sorry, Neither is an authenticated user, nor a valid key is entered!"})
    except Exception as error:
        logger.Error("Error in server mainRuote", str(error))


@app.route('/api/<media_type>/all', methods=['GET'])
def getAllMediaByType(media_type):
    r = Media.retrieve(_id=None, key='media type', value=media_type)
    return jsonify(r)


@app.route('/api/<media_type>/<movie_id>', methods=['GET'])
def getMediaByID(media_type, movie_id):
    result = json.loads(Media.retrieve(_id=movie_id, key='media type', value=media_type))
    if result:
        return jsonify(result)
    else:
        return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})


@app.route('/api/search/query=<title>', methods=['GET'])
def searchMediaByQuery(title):
    # searchword = request.args.get('query', title)
    # print(searchword)
    r = Media.retrieve(_id=None, key='title', value=title)
    print("Result of request: ", r)
    if r:
        result = json.loads(r)
        return jsonify(result)
    else:
        return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})


@app.route('/api/search/key=<key>&value=<value>', methods=['GET'])
def searchMediaByKeyValue(key, value):
    r = Media.retrieve(_id=None, key=key, value=value)

    if len(r) == 1:
        result = json.loads(r)
        return jsonify(result)
    elif len(r) > 1:
        return jsonify(r)
        # output = []
        # for i in r:
        #     t = json.loads(i)
        #     output.append(t)
        # return output
    else:
        return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})


if __name__ == '__main__':
    app.run(host=IP, port=PORT, debug=True)
