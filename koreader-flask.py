import os
import time
import json
import argparse
import logging
import traceback
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify

# TODO return content type application/vnd.koreader.v1+json

## Database stuff. Easy to replace with anything: MySql, sqlite, whatever...

# UserDB:
# {
#    'username' : {
#        'username': "username", // Duplicated for convenience
#        'userkey' : "key",
#        'documents' : {
#            'document' : {
#                'progress' : "progress",
#                'percentage' : percentage,
#                'device' : "device",
#                'device_id': "deviceId",
#                'timestamp': timestamp
#        }
#    }
#}

def loadDb():
    global users

    if os.path.isfile(USERSDB):
        theFile = open(USERSDB, 'r', encoding='utf-8')
        users = json.load(theFile)
        theFile.close()
    else:
        users = dict()
    return users;

def saveDb():
    global users

    theFile = open(USERSDB, 'w+', encoding='utf-8')
    print(json.dumps(users, indent=2), file=theFile)
    theFile.close()

def getUser(userName):
    global users

    loadDb()
    return users.get(userName)

def addUser(userName, userKey):
    global users

    if (getUser(userName) != None):
        return False
    users[userName] = dict(username=userName, userkey=userKey)
    saveDb()
    return True

def getPosition(username, document):
    user = getUser(username)
    doc = dict();
    documents = user.get('documents')
    if (documents != None):
        doc = documents.get(document)
        if (doc != None):
            doc['document'] = document
    return doc

def updatePosition(username, document, position):
    user = getUser(username)
    doc = dict()
    timestamp = int(time.time())
    doc['percentage'] = position.get('percentage')
    doc['progress'] = position.get('progress')
    doc['device'] = position.get('device')
    doc['device_id'] = position.get('device_id')
    doc['timestamp'] = timestamp

    if (user.get('documents') == None):
        user['documents'] = dict()
    user['documents'][document] = doc
    saveDb()
    return timestamp

### Database stuff ends here

# Web Server stuff

app = Flask(__name__)

class ServiceError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        super(ServiceError, self).__init__(message)
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        thePayload = self.payload
        if (thePayload):
            # Convert non-iterable payload to an iterable
            try:
                iter(thePayload)
            except:
                thePayload = (thePayload)
        rv = dict(thePayload or ())
        rv['message'] = str(self)
        return rv

def logException(exception):
    app.logger.error("".join(traceback.format_exception(type(exception), exception, exception.__traceback__)))

@app.errorhandler(ServiceError)
def handle_service_error(error):
    logException(error)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def authorizeRequest(request):
    username = request.headers.get("x-auth-user")
    userkey = request.headers.get("x-auth-key")
    if (username == None or userkey == None):
        raise ServiceError('Unauthorized', status_code=401)

    user = getUser(username)
    if (user == None):
        raise ServiceError('Forbidden', status_code=403)
    if (userkey != user['userkey']):
        raise ServiceError('Unauthorized', status_code=401)
    return user

# API

@app.route('/users/create', methods = ['POST'])
def register():
    try:
        if (request.is_json):
            user = request.get_json()
            username = user.get('username')
            userkey = user.get('password')
            if (username == None or userkey == None):
                return 'Invalid request', 400
            if (not addUser(username, userkey)):
                return 'Username is already registered.', 409
            return jsonify(dict(username=username)), 201
        else:
            return 'Invalid request', 400
    except Exception as e:
        raise ServiceError('Unknown server error', status_code=500) from e

@app.route('/users/auth')
def authorize():
    try:
        authorizeRequest(request)
        return jsonify(dict(authorized='OK')), 200
    except ServiceError as se:
        raise
    except Exception as e:
        raise ServiceError('Unknown server error', status_code=500) from e

@app.route('/syncs/progress/<document>')
def getProgress(document):
    try:
        user = authorizeRequest(request)
        position = getPosition(user['username'], document)
        return jsonify(position), 200
    except ServiceError as se:
        raise
    except Exception as e:
        raise ServiceError('Unknown server error', status_code=500) from e

@app.route('/syncs/progress', methods = ['PUT'])
def updateProgress():
    try:
        user = authorizeRequest(request)
        if (request.is_json):
            position = request.get_json()
            document = position.get('document')
            timestamp = updatePosition(user['username'], document, position)
            return jsonify(dict(document = document, timestamp = timestamp)), 200
        else:
            return 'Invalid request', 400
    except ServiceError as se:
        raise
    except Exception as e:
        raise ServiceError('Unknown server error', status_code=500) from e

# Initialization

def main():
    parser = argparse.ArgumentParser(description="KOReader Sync Server")
    parser.add_argument("-d", "--database", type = str, default='users.json', help = "JSON Database file")
    parser.add_argument("-t", "--host", type = str, default="0.0.0.0", help = "Server host")
    parser.add_argument("-p", "--port", type = int, default=8081, help = "Server port")
    parser.add_argument("-c", "--certificate", type = str, help = "SSL Certificate file")
    parser.add_argument("-k", "--key", type = str, help = "SSL Private key file")
    parser.add_argument("-l", "--logfile", type = str, default='koreader-server.log', help = "Log file")
    parser.add_argument("-v", "--verbose", action='store_true', help = "Run server in debug mode")
    args = parser.parse_args()

    global USERSDB

    USERSDB = args.database
    handler = RotatingFileHandler(args.logfile, maxBytes=100000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(handler) # HTTP log goes here
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    context = None
    if (args.certificate and args.key):
        context = (args.certificate, args.key)
    app.run(debug=args.verbose,host=args.host, port=args.port, ssl_context=context)

main()
