import requests
import os
import json
from app.models import User, Token, db
from app.functions.error import AccessError, ServiceUnavailableError

def connect(user_id):
    """Gets all required tokens for a user"""
    #getuser
    user = User.query.filter(User.id == user_id).first()
    send_token = start_send_session()
    create_token = None
    cleanup_tokens(user)

    new_token = Token(user=user, send_token=send_token,
                      create_token=create_token)
    db.session.add(new_token)
    db.session.commit()

    return {"send_token": send_token, "create_token": create_token}

def disconnect(user_id):
    """Disconnects all tokens for a user"""
    token = None
    user = User.query.filter(User.id == user_id).first()
    if user != None:
        token = Token.query.filter(Token.user == user).first()
    else:
        raise AccessError(description="That user does not exist")

    if token != None:
        end_send_session(token.send_token)
        cleanup_tokens(user)

    return {}


####### helpers #######

def start_send_session():
    resp = requests.post("https://fudge2021.herokuapp.com/session/start", json={
                         'username': os.environ.get("SENDUSERNAME"), 'password': os.environ.get("SENDPASSWORD")})

    if resp.status_code != 200:
        raise ServiceUnavailableError(description= "Cannot reach send email API, please try again later.")

    return json.loads(resp.text)['token']

def end_send_session(token):
    resp = requests.post("https://fudge2021.herokuapp.com/session/end", json={
                         'token': token})

    if resp.status_code != 200:
        raise ServiceUnavailableError(description= "Cannot reach send email API, please try again later.")

    return json.loads(resp.text)['token']

def cleanup_tokens(user):
    old_tokens = Token.query.filter(Token.user == user).all()
    for token in old_tokens:
        db.session.delete(token)
