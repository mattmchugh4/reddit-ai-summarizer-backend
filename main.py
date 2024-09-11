from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# Import the synchronous wrapper function
from handle_query import start_query
from web_search import perform_search

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(
    app, cors_allowed_origins="*", engineio_logger=True, logger=True, ping_timeout=120
)


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


@socketio.on("search")
def run_search(data):
    search_query = data.get("searchQuery")

    def emit_search_result(result):
        socketio.emit("search_result", {"result": result})

    perform_search(search_query, emit_search_result)


@socketio.on("searchUrl")
def handle_request_data(data):
    input_url = data.get("inputUrl")

    def emit_processed_data(processed_data):
        socketio.emit("comment-data", processed_data)

    def emit_status_message(status_message):
        socketio.emit("status-message", status_message)

    start_query(input_url, emit_processed_data, emit_status_message)


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on("data")
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ", str(data))
    emit("data", {"data": data, "id": request.sid}, broadcast=True)


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001)

    # app.run(debug=True, port=5000)
