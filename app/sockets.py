from flask import request
from flask_socketio import emit

from app.start_query import start_query
from app.web_search import perform_search


def register_socket_handlers(socketio):

    @socketio.on("search")
    def run_search(data):
        search_query = data.get("searchQuery")

        perform_search(
            search_query, lambda result: emit("search_result", {"result": result})
        )

    @socketio.on("searchUrl")
    def handle_request_data(data):
        input_url = data.get("inputUrl")

        start_query(
            input_url,
            lambda processed_data: emit("comment-data", processed_data),
            lambda status_message: emit("status-message", status_message),
        )

    @socketio.on("connect")
    def connected():
        """Event listener when client connects to the server"""
        emit("connect", {"data": f"id: {request.sid} is connected"})

    @socketio.on("data")
    def handle_message(data):
        """Event listener when client types a message"""
        emit("data", {"data": data, "id": request.sid}, broadcast=True)

    @socketio.on("disconnect")
    def disconnected():
        """Event listener when client disconnects to the server"""
        emit("disconnect", f"user {request.sid} disconnected", broadcast=True)