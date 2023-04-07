from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, emit
from flask_cors import CORS

from handle_query import start_query


app = Flask(__name__)
# app.config['SECRET_KEY'] = '870c84b187e85d1350d36e0f5cfeffab26a9255e5bf5c3e3'
# CORS(app, resources={r"/*": {"origins": "*"}})
# socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/http-call", methods=['POST'])
def http_call():

    data = request.json.get('data')

    processed_data = start_query(data)

    return processed_data




# @socketio.on("connect")
# def connected():
#     # This function is executed when a new client connects to the server via Socket.IO
#     # It prints the client's session ID and a message indicating that the client has connected.
#     print(request.sid)
#     print("client has connected")
#     # Send a message to the client with their session ID
#     emit("connect", {"data": f"id: {request.sid} is connected"})

# # Event listener for receiving data from a client via Socket.IO


# @socketio.on('data')
# def handle_message(data):
#     # This function is executed when the server receives a message from a client via Socket.IO
#     # It prints the message received from the client and broadcasts the message to all connected clients,
#     # along with the sender's session ID.
#     print("data from the front end: ", str(data))
#     emit("data", {'data': data, 'id': request.sid}, broadcast=True)

# # Event listener for a client disconnecting from the server via Socket.IO


# @socketio.on("disconnect")
# def disconnected():
#     # This function is executed when a client disconnects from the server via Socket.IO
#     # It prints a message indicating that the user has disconnected and broadcasts a message
#     # to all connected clients informing them of the disconnection.
#     print("user disconnected")
#     emit("disconnect", f"user {request.sid} disconnected", broadcast=True)



if __name__ == '__main__':
    app.run(debug=True, port=5001)

    # socketio.run(app, debug=True, port=5001)
