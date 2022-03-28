from os import getcwd, environ
import os

PORT = 5000

url = f"http://localhost:{PORT}/"

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    if 'SECRET_KEY' in environ:
        SECRET_KEY = environ.get('SECRET_KEY')

    # Database setup for later

    # Import environ if not on server where enviorment variables already saved
    if "ON_SERVER" not in os.environ:
        import enviro # pylint: disable=import-error

    # Gets uri for databse from eviro if on heroku, otherwise uses local sqlite
    if "DATABASE_URL" in os.environ:
        db_start = os.environ.get("DATABASE_URL")
        split_db = db_start.split(":")
        split_db[0] += "ql"
        SQLALCHEMY_DATABASE_URI = ":".join(split_db)
    else:

        # Remove local db if currenlty exists
        directory = getcwd()
        db_path = directory + "\\app\\log.db"
        if os.path.exists(db_path):
            os.remove(db_path)


        SQLALCHEMY_DATABASE_URI = "sqlite:///log.db"

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
