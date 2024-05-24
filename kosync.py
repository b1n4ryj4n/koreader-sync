# -*- coding: utf-8 -*-
import time
import uuid
from distutils.util import strtobool
from os import getenv
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from tinydb import Query, TinyDB

app = FastAPI(openapi_url=None, redoc_url=None)
db = TinyDB("data/db.json")
users = db.table("users")
documents = db.table("documents")
load_dotenv()

class KosyncUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class KosyncDocument(BaseModel):
    document: Optional[str] = None
    progress: Optional[str] = None
    percentage: Optional[float] = None
    device: Optional[str] = None
    device_id: Optional[str] = None


@app.post("/users/create")
def register(kosync_user: KosyncUser):
	# Check whether new registrations are allowed on this server based on the OPEN_REGISTRATIONS environment variable.
	# By default registrations are enabled.
	registrations_allowed = bool(strtobool(getenv("OPEN_REGISTRATIONS", "True")))
	if registrations_allowed:
		# check if username or password is missing
		if kosync_user.username is None or kosync_user.password is None:
			return JSONResponse(status_code=400, content={"message": f"Invalid request"})
		# check if user already exists
		QUser = Query()
		if users.contains(QUser.username == kosync_user.username):
			return JSONResponse(status_code=409, content="Username is already registered.")
		# register new user
		if users.insert({'username': kosync_user.username, 'password': kosync_user.password}):
			return JSONResponse(status_code=201, content={"username": kosync_user.username})
		# if something went wrong
		return JSONResponse(status_code=500, content="Unknown server error")
	else:
		return JSONResponse(status_code=403, content="This server is currently not accepting new registrations.")


@app.get("/users/auth")
def authorize(x_auth_user: Optional[str] = Header(None), x_auth_key: Optional[str] = Header(None)):
    # check if username or password is missing
    if x_auth_user is None or x_auth_key is None:
        return JSONResponse(status_code=401, content={"message": f"Unauthorized"})
    # check if username is in database
    QUser = Query()
    # check username and password combination
    if users.contains(QUser.username == x_auth_user):
        if users.contains((QUser.username == x_auth_user) & (QUser.password == x_auth_key)):
            return JSONResponse(status_code=200, content={"authorized": f"OK"})
        else:
            return JSONResponse(status_code=401, content={"message": f"Unauthorized"})
    return JSONResponse(status_code=403, content={"message": f"Forbidden"})


@app.put("/syncs/progress")
def update_progress(kosync_document: KosyncDocument, x_auth_user: Optional[str] = Header(None),
                    x_auth_key: Optional[str] = Header(None)):
    # check if username or password is missing
    if x_auth_user is None or x_auth_key is None:
        return JSONResponse(status_code=401, content={"message": f"Unauthorized"})
    QUser = Query()
    QDocument = Query()
    # check if username is in database
    if not users.contains(QUser.username == x_auth_user):
        return JSONResponse(status_code=403, content={"message": f"Forbidden"})
    # check username and password combination before put data in database
    if users.contains((QUser.username == x_auth_user) & (QUser.password == x_auth_key)):
        # add new document progress
        timestamp = int(time.time())
        if kosync_document.document is None or kosync_document.progress is None or kosync_document.percentage is None \
                or kosync_document.device is None or kosync_document.device_id is None:
            return JSONResponse(status_code=500, content="Unknown server error")
        else:
            if documents.upsert({'username': x_auth_user, 'document': kosync_document.document,
                                 'progress': kosync_document.progress, 'percentage': kosync_document.percentage,
                                 'device': kosync_document.device, 'device_id': kosync_document.device_id,
                                 'timestamp': timestamp}, (QDocument.username == x_auth_user) &
                                                          (QDocument.document == kosync_document.document)):
                return JSONResponse(status_code=200,
                                    content={"document": kosync_document.document, "timestamp": timestamp})
    else:
        return JSONResponse(status_code=401, content={"message": f"Unauthorized"})


@app.get("/syncs/progress/{document}")
def get_progress(document: Optional[str] = None, x_auth_user: Optional[str] = Header(None),
                 x_auth_key: Optional[str] = Header(None)):
    # check if username or password is missing
    if x_auth_user is None or x_auth_key is None:
        return JSONResponse(status_code=401, content={"message": f"Unauthorized"})
    # check if document parameter exists
    if document is None:
        return JSONResponse(status_code=500, content="Unknown server error")

    QUser = Query()
    QDocument = Query()

    # check if username is in database
    if not users.contains(QUser.username == x_auth_user):
        return JSONResponse(status_code=403, content={"message": f"Forbidden"})

    # check username and password combination before get progress data
    if users.contains((QUser.username == x_auth_user) & (QUser.password == x_auth_key)):
        # get document progress if user has the document
        result = documents.get((QDocument.username == x_auth_user) & (QDocument.document == document))
        if result:
            rrdi = bool(strtobool(getenv("RECEIVE_RANDOM_DEVICE_ID", "False")))
            if rrdi == False:
                device_id = result["device_id"]
            else:
                device_id = uuid.uuid1()
                device_id = str(device_id.hex).upper()
            return JSONResponse(status_code=200,
                                content={'username': x_auth_user, 'document': result["document"],
                                         'progress': result["progress"], 'percentage': result["percentage"],
                                         'device': result["device"], 'device_id': device_id,
                                         'timestamp': result["timestamp"]})
    else:
        return JSONResponse(status_code=401, content={"message": f"Unauthorized"})

@app.get("/healthstatus")
def get_healthstatus():
    return JSONResponse(status_code=200, content={"message": f"healthy"})
