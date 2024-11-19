import eventlet

eventlet.monkey_patch()

import logging  # noqa: E402
import os  # noqa: E402

from dotenv import load_dotenv  # noqa: E402
from flask import Flask, request  # noqa: E402
from flask_cors import CORS  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402

from app.sockets import register_socket_handlers  # noqa: E402
from app.start_query import start_query  # noqa: E402

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise ValueError("No SECRET_KEY set for Flask application")

CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    # Change for debugging
    engineio_logger=True,
    logger=True,
    ping_timeout=120,
    async_mode="eventlet",  # Use Eventlet for async support
)


register_socket_handlers(socketio)


@app.errorhandler(ConnectionRefusedError)
def connection_refused_error_handler(error):
    print("Connection refused:", error)
    return "", 500


@app.route("/http-call", methods=["POST"])
def http_call():
    try:
        data = request.json.get("data")
        processed_data = start_query(data)
        return processed_data
    except ConnectionRefusedError as e:
        print("Connection refused:", e)
        raise e


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001)

    # app.run(debug=True, port=5000)

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
