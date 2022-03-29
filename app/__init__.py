from json import dumps
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


startTime = datetime.now()

db = SQLAlchemy()


def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.register_error_handler(Exception, default_handler)

    CORS(app)

    db.init_app(app)

    with app.app_context():
        from app import routes #pylint:ignore

        db.create_all()  # Create sql tables for our data models

        return app

def default_handler(err):
    """Handle errors"""
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response
