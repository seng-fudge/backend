import signal
import config
from app import init_app


def graceful_exit(*args):
    """add things here to close/disconnect/remove/delete on exit"""
    exit(0)

app = init_app()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, graceful_exit)
    app.run(port = config.PORT, debug = True)
