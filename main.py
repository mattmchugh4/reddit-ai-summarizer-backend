from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO

from app.sockets import register_socket_handlers
from app.start_query import start_query

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    # engineio_logger=True,
    # logger=True, # logging for debugging
    engineio_logger=True,
    logger=True,
    ping_timeout=120,
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
