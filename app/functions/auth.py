import os
import re
import time
import jwt

from app.functions.error import AccessError, InputError
from app.models import Accountdata, Session, User, db

SECRET = os.environ.get('SECRET')

def login(email, password):
    """
    Checks if login credentials are valid

    Raises issue if variables given are invalid:
        - Invalid email or password

    Parameters
    ----------
    'email' - (String)
    'password' - (String)

    Returns
    -------
    Is valid (Token)
    """

    curr_user = User.query.filter(
        User.email == email, User.password == password).first()

    if curr_user is None:
        raise InputError(description="Invalid email or password")

    return True


def logout():
    """docstring"""
    return


def register(email, password):
    """
    Creates new user. Valid password is min 8 char, contains at least 1 upper case and 1 digit

    Raises issue if variables given are invalid:
        - Invalid email or password
        - Email already registered

    Parameters
    ----------
    'email' - (String)
    'password' - (String)

    Returns
    -------
    None
    """

    # Check if email already registed
    registered_user = User.query.filter(User.email == email).first()

    if registered_user is not None:
        raise InputError(description="Email already registered with account")

    # Check valid inputs
    if not validate_email(email):
        raise InputError(description="Email is invalid")

    if not validate_password(password):
        raise InputError(description="Password is invalid")

    # Create new user
    new_user = User(email = email, password = password)
    new_user_data = Accountdata(
        businessName = None,
        contactName = None,
        electronicMail = email,

        supplierID = None,
        street = None,
        city = None,
        postcode = None,
        country = None,
        currency = None
    )
    db.session.add(new_user)
    db.session.add(new_user_data)
    db.session.commit()

def generate_token(email):
    """
    Generates new session and returns token.

    Parameters
    ----------
    'email' - (String)

    Returns
    -------
    {
        'token' : (String)
    }
    """

    user = User.query.filter(User.email == email).first()

    new_session = Session(user = user, time = time.time())

    new_session = Session(user = user, time = time.time())

    db.session.add(new_session)
    db.session.commit()

    token = jwt.encode(
        {'email' : user.email, 'session_id' : new_session.id},
        SECRET,
        algorithm='HS256'
    )

    return {'token' : token}


def remove():
    """docstring"""
    return

def validate_email(email):
    """Docstring"""
    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    return re.fullmatch(email_regex,email)

def validate_password(password):
    """docstring"""
    if len(password) < 8:
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    return True

def validate_token(token):
    """
    validates session and token
    returns user id from token.

    Raises issue if variables given are invalid:
        - token

    Parameters
    ----------
    'token' - string

    Returns
    -------
    userID - integer
    """
    decoded_token = jwt.decode(token,
    SECRET,
    algorithms=['HS256'])

    session_id = decoded_token['session_id']

    # return userid
    session = Session.query.filter(Session.id == session_id).first()
    return session.userId