import json
from flask import current_app as app, request

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("Backend Online")


#################### /auth ####################
@app.route("/auth/login", methods=["POST"])
def auth_login():
    # log a user into their session (connect all their api sessions)
    return

@app.route("/auth/logout", methods=["POST"])
def auth_logout():
    # log a user out of their session (also disconect all api sessions)
    return

@app.route("/auth/register", methods=["POST"])
def auth_register():
    #register a user account
    return

@app.route("/auth/remove", methods=["DELETE"])
def auth_remove():
    #delete user account
    return

###############################################

#################### /apis ####################
@app.route("/apis/connect", methods=["POST"])
def apis_connect():
    # connect all apis (associated with a user)
    return
@app.route("/apis/disconnect", methods=["POST"])
def apis_disconnect():
    # disconnect all apis (associated with a user)
    return
@app.route("/apis/renew", methods=["POST"])
def apis_renew():
    # disconnect all apis, and renew tokens (associated with a user)
    return
###############################################

#################### /user ####################
@app.route("/user/data", methods=["POST", "GET"])
def user_data():
    if request.method == "POST":
        # update user data
        return
    if request.method == "GET":
        # Get user data
        return
    
###############################################