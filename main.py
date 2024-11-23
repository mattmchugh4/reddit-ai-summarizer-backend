import logging
import os

import eventlet

eventlet.monkey_patch()

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

from app.sockets import register_socket_handlers
from app.start_query import start_query
from app.web_search import perform_search

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
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


@app.route("/search", methods=["POST"])
def search_route():
    """
    Example usage:
    POST /search
    JSON Body: {"query": "python web scraping"}
    """
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' in JSON body"}), 400

    search_query = data["query"]
    try:
        results = perform_search(search_query)
        return jsonify({"results": results})
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return jsonify({"error": "Search failed"}), 500


if __name__ == "__main__":
    socketio.run(app, debug=SOCKETIO_DEBUG, port=5001)
