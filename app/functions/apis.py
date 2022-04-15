import os
import json
import requests

from flask import session
from app.models import Session, User, Token, db
from app.functions.error import InputError, ServiceUnavailableError


def render_cors_forward(xml):
    resp = requests.post(
        "https://www.invoicerendering.com/einvoices?renderType=html",
        files={'xml': xml})

    if resp.status_code != 200:
        raise InputError(description=resp.json)

    return resp.text

def render_get_pdf(xml):
    resp = requests.post(
        "https://www.invoicerendering.com/einvoices?renderType=pdf",
        files={'xml': xml})
    if resp.status_code != 200:
        raise ServiceUnavailableError(
            description="Something went wront with the PDF renderer, email was not sent"
            )
    return resp.content

def send_email_pdf(session_id, xml_string, pdf_bytestream):
    token = get_current_token(session_id)

    resp = requests.post(
        "https://fudge2021.herokuapp.com/invoice/extract_and_send/pdf",
        files = {'file': bytes(xml_string, 'UTF-8'), "pdf": pdf_bytestream },
        headers = {"token": token.send_token}
    )
    return resp

def connect(session_id):
    """
    Connects user to token for session

    Raises issue if api servers are not working

    Parameters
    ----------
    'session_id' - int

    Returns
    -------
    {"send_token": (String)}
    """

    send_token = start_send_session()
    cleanup_tokens(session_id)

    new_token = Token(sessionId=session_id, send_token=send_token)
    db.session.add(new_token)
    db.session.commit()

    return {"send_token": send_token}


def disconnect(session_id):
    """
    Disconnects session tokens

    Parameters
    ----------
    'session_id' - int

    Returns
    -------
    None
    """
    token = Token.query.filter(Token.sessionId == session_id).first()

    if token is not None:
        end_send_session(token.send_token)
        cleanup_tokens(session_id)

    return {}


####### helpers #######

def start_send_session():
    ''''Gets token for send api'''
    resp = requests.post("https://fudge2021.herokuapp.com/session/start", json={
                         'username': os.environ.get("SENDUSERNAME"),
                         'password': os.environ.get("SENDPASSWORD")})

    if resp.status_code != 200:
        raise ServiceUnavailableError(
            description="Cannot reach send email API, please try again later.")

    return json.loads(resp.text)['token']


def end_send_session(token):
    ''''Logsout token for send api'''
    requests.post("https://fudge2021.herokuapp.com/session/end", json={
        'token': token})


def cleanup_tokens(session_id):
    '''Logout and remove all tokens linked to session'''
    old_tokens = Token.query.filter(Token.sessionId == session_id).all()
    for token in old_tokens:
        db.session.delete(token)

def get_current_token(session_id):
    token = Token.query.filter(Token.sessionId == session_id).first()
    return token
