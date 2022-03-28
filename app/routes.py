import json
from flask import current_app as app, request
from app.functions import apis, auth, user

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("Backend Online")


#################### /auth ####################
@app.route("/auth/login", methods=["POST"])
def auth_login():
    # log a user into their session
    auth.login()
    return

@app.route("/auth/logout", methods=["POST"])
def auth_logout():
    # log a user out of their session (also disconect all api sessions)
    auth.logout
    return

@app.route("/auth/register", methods=["POST"])
def auth_register():
    #register a user account
    auth.register()
    return

@app.route("/auth/remove", methods=["DELETE"])
def auth_remove():
    #delete user account
    auth.remove()
    return

###############################################

#################### /apis ####################
@app.route("/apis/connect", methods=["POST"])
def apis_connect():
    # connect all apis (associated with session)
    apis.connect()
    return
@app.route("/apis/disconnect", methods=["POST"])
def apis_disconnect():
    # disconnect all apis (associated with session)
    apis.disconnect()
    return
###############################################

#################### /user ####################
@app.route("/user/data", methods=["POST", "GET"])
def user_data():
    if request.method == "POST":
        # update user data
        user.update_data()
        return
    if request.method == "GET":
        # Get user data
        user.get_data()
        return
    
###############################################