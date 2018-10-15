#!/usr/bin/python
import json
import settings
from Models import Media
from Logger import Logger
from flask import Flask, jsonify, render_template, request

# Create an instance of the application
app = Flask(__name__, template_folder='views')

# Define server IP and port number
IP = settings.server_ip
PORT = settings.server_port

# Get token of a specific user for this api
USER_TOKEN = settings.user_token
logger = Logger()


@app.route('/', methods=['GET'])
@app.route('/api/', methods=['GET'])
def home():
    """ A router function with GET method request for loading the landing page of the API."""
    try:
        return render_template('index.html', title="Home|API")
    except Exception as error:
        logger.Error("Error in server mainRuote: ", str(error))


@app.route('/api/<user_token>/<media_type>/all', methods=['GET'])
def getAllMediaByType(user_token, media_type):
    """ A router function with GET request for retrieving all media based on the type, show or movie."""
    # Check if the user is a valid user
    if user_token == USER_TOKEN:
        try:
            limit = request.args.get('limit', None)
            offset = request.args.get('offset', None)
            # Do the pagination here
            if limit and offset:
                result = Media.retrieveAll(key='media type', value=media_type, limit=int(limit), offset=int(offset))
                return jsonify(
                    {'next_url': "/all?limit=" + limit + "&offset=" + str(int(offset) + int(limit)),
                     'prev_url': "/all?limit=" + limit + "&offset=" + str(int(offset) - int(limit)),
                     'result': result
                     }
                    )
            else:
                return jsonify({'Error': "Values for limit and offset should be defined. "
                                         "Usage: /api/<user_token>/<media_type>/all?limit=<limit>&offset=<offset> "})

        except Exception as error:
            logger.Error("Error in server getAllMediaType: ", str(error))
    else:
        return jsonify({'Error': "Sorry, you are not a valid user to use this API."})


@app.route('/api/<user_token>/<media_type>/<movie_id>', methods=['GET'])
def getMediaByID(user_token, media_type, movie_id):
    """ A GET method request router for retrieving a media by its id and type, show or movie."""
    # Check if the user is a valid user
    if user_token == USER_TOKEN:
        result = json.loads(Media.retrieve(_id=movie_id, key='media type', value=media_type))
        if result:
            return jsonify(result)
        else:
            return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})
    else:
        return jsonify({'Error': "Sorry, you are not a valid user to use this API."})


@app.route('/api/<user_token>/search', methods=['GET'])
def searchMediaByQuery(user_token):
    """ A GET method request router for retrieving a media by its title."""
    # Check if the user is a valid user
    if user_token == USER_TOKEN:
        title = request.args.get('query', None)
        r = Media.retrieve(_id=None, key='title', value=title)
        logger.Info("Result of request: ", str(r))
        if r:
            result = json.loads(r)
            return jsonify(result)
        else:
            return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})
    else:
        return jsonify({'Error': "Sorry, you are not a valid user to use this API."})


@app.route('/api/<user_token>/search/key=<key>&value=<value>', methods=['GET'])
def searchMediaByKeyValue(user_token, key, value):
    """ A GET method request router to get any key-value passing parameters. The result can be a single document or
    an array of document objects."""
    r = Media.retrieve(_id=None, key=key, value=value)
    # Check if the user is a valid user
    if user_token == USER_TOKEN:
        if len(r) == 1:
            result = json.loads(r)
            return jsonify(result)
        elif len(r) > 1:  # Do the pagination here
            return jsonify(r)
        else:
            return jsonify({'Error': "Sorry, we couldn't find the media that you requested."})
    else:
        return jsonify({'Error': "Sorry, you are not a valid user to use this API."})


if __name__ == '__main__':
    app.run(host=IP, port=PORT, debug=True)
