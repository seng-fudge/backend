from flask import session
import requests
import os
import json
from app.models import Session, User, Token, db
from app.functions.error import AccessError, ServiceUnavailableError


def connect(session_id):
    """Gets all required tokens for a user"""

    send_token = start_send_session()
    cleanup_tokens(session_id)

    new_token = Token(sessionId=session_id, send_token=send_token)
    db.session.add(new_token)
    db.session.commit()

    return {"send_token": send_token}


def disconnect(session_id):
    """Disconnects all tokens for a user"""
    token = Token.query.filter(Token.sessionId == session_id).first()

    if token is not None:
        end_send_session(token.send_token)
        cleanup_tokens(session_id)

    return {}


####### helpers #######

def start_send_session():
    resp = requests.post("https://fudge2021.herokuapp.com/session/start", json={
                         'username': os.environ.get("SENDUSERNAME"), 'password': os.environ.get("SENDPASSWORD")})

    if resp.status_code != 200:
        raise ServiceUnavailableError(
            description="Cannot reach send email API, please try again later.")

    return json.loads(resp.text)['token']


def end_send_session(token):
    requests.post("https://fudge2021.herokuapp.com/session/end", json={
                         'token': token})


def cleanup_tokens(session_id):
    old_tokens = Token.query.filter(Token.sessionId == session_id).all()
    for token in old_tokens:
        db.session.delete(token)
