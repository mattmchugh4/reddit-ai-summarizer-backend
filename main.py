import logging

import eventlet

eventlet.monkey_patch()

import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO

from app.sockets import register_socket_handlers
from app.start_query import start_query

logger = logging.getLogger(__name__)

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
# Enable Socket.IO debugging only if LOG_LEVEL is "DEBUG"
SOCKETIO_DEBUG = LOG_LEVEL == "DEBUG"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise ValueError("No SECRET_KEY set for Flask application")

CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    # Change for debugging
    engineio_logger=SOCKETIO_DEBUG,
    logger=SOCKETIO_DEBUG,
    ping_timeout=120,
    async_mode="eventlet",  # Use Eventlet for async support
)


register_socket_handlers(socketio)


@app.errorhandler(ConnectionRefusedError)
def connection_refused_error_handler(error):
    logger.error("Connection refused: %s", error)
    return "", 500


# todo rename all of this
@app.route("/http-call", methods=["POST"])
def http_call():
    try:
        data = request.json.get("data")
        processed_data = start_query(data)
        return processed_data
    except ConnectionRefusedError as e:
        logger.error("Connection refused: %s", e)
        raise e


if __name__ == "__main__":
    socketio.run(app, debug=SOCKETIO_DEBUG, port=5001)
