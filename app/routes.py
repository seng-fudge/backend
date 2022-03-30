import json
from os import execv
from flask import current_app as app, request
from app.functions import apis, auth, user
from app.functions.error import InputError

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("Backend Online")


#################### /auth ####################
@app.route("/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json()
    # log a user into their session
    auth.login(data['email'], data['password'])

    return json.dumps(auth.generate_token(data['email']))

@app.route("/auth/logout", methods=["POST"])
def auth_logout():
    # log a user out of their session (also disconect all api sessions)
    auth.logout()

@app.route("/auth/register", methods=["POST"])
def auth_register():
    data = request.get_json()
    #register a user account
    auth.register(data['email'], data['password'])

    return json.dumps(auth.generate_token(data['email']))

@app.route("/auth/remove", methods=["DELETE"])
def auth_remove():
    #delete user account
    auth.remove()

###############################################

#################### /apis ####################
@app.route("/apis/connect", methods=["POST"])
def apis_connect():
    # connect all apis (associated with session)
    apis.connect()

@app.route("/apis/disconnect", methods=["POST"])
def apis_disconnect():
    # disconnect all apis (associated with session)
    apis.disconnect()

###############################################

#################### /user ####################
@app.route("/user/data", methods=["GET","POST"])
def user_data():
    token = request.headers["token"]
    user_id = auth.validate_token(token)

    if request.method == "POST":
        # update user data
        users_data = request.get_json()
        try:
            user.update_data(user_id, users_data)
        except KeyError as missing_data:
            raise InputError from missing_data
        return {}
    if request.method == "GET":
        # Get user data
        data = user.get_data(user_id)
        return data

    return {}
###############################################
