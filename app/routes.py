from crypt import methods
import json
from os import execv
from flask import current_app as app, request, session
from app.functions import apis, auth, user
from app.functions.error import InputError, AccessError, ServiceUnavailableError


@app.route("/", methods=["GET"])
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
    token = request.headers["token"]
    # log a user out of their session (also disconect all api sessions)
    auth.logout(token)
    return {}


@app.route("/auth/register", methods=["POST"])
def auth_register():
    data = request.get_json()
    # register a user account
    auth.register(data['email'], data['password'])

    return json.dumps(auth.generate_token(data['email']))


@app.route("/auth/remove", methods=["DELETE"])
def auth_remove():

    token = request.headers["token"]
    user_id, _ = auth.validate_token(token)

    # delete user account
    auth.remove(user_id)

    return json.dumps({})

###############################################

#################### /apis ####################


@app.route("/apis/connect", methods=["POST"])
def apis_connect():
    token = request.headers["token"]
    _, session_id = auth.validate_token(token)
    # connect all apis (associated with session)
    response = apis.connect(session_id)
    return json.dumps(response)


@app.route("/apis/disconnect", methods=["POST"])
def apis_disconnect():
    token = request.headers["token"]
    _, session_id = auth.validate_token(token)
    # disconnect all apis (associated with session)
    apis.disconnect(session_id)
    return {}


@app.route("/apis/render_forward", methods=["POST"])
def apis_render_forward():
    token = request.headers["token"]
    auth.validate_token(token)

    data = request.get_json()

    return apis.render_cors_forward(data['xml'])


@app.route("/apis/email_pdf", methods = ['POST'])
def email_as_pdf():
    token = request.headers["token"]
    _, session_id = auth.validate_token(token)

    data = request.get_json()
    pdf_bytestream = apis.render_get_pdf(data['xml'])
    resp = apis.send_email_pdf(session_id, data['xml'], pdf_bytestream)

    if resp.status_code != 200:
        raise ServiceUnavailableError(
            description= "something wrong with the send email API, email was not sent")

    return {}


###############################################

#################### /user ####################


@app.route("/user/data", methods=["GET", "POST"])
def user_data():
    token = request.headers["token"]
    user_id, _ = auth.validate_token(token)

    if request.method == "POST":
        # update user data
        users_data = request.get_json()
        try:
            user.update_data(user_id, users_data)
        except KeyError as missing_data:
            raise InputError(
                description="Json form incomplete") from missing_data
        return {}
    if request.method == "GET":
        # Get user data
        return user.get_data(user_id)

    return {}
###############################################
