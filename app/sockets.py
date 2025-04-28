import logging

from flask import request
from flask_socketio import emit

from app.start_query import start_query
from app.web_search import perform_search

logger = logging.getLogger(__name__)


def register_socket_handlers(socketio):
    # Create new namespace instance
    namespace = "/api/reddit-summarizer/ws/"

    @socketio.on("search", namespace=namespace)
    def run_search(data):
        search_query = data.get("searchQuery")

        perform_search(
            search_query, lambda result: emit("search_result", {"result": result})
        )

    @socketio.on("searchUrlAndQuestion", namespace=namespace)
    def handle_request_data(data):
        input_url = data.get("inputUrl")
        user_question = data.get("userQuestion")

        start_query(
            input_url,
            user_question,
            lambda processed_data: emit("comment-data", processed_data),
            lambda status_message: emit("status-message", status_message),
            lambda stream_chunk: emit("stream-response", stream_chunk),
            lambda post_data: emit("post-data", post_data),
        )

    @socketio.on("connect", namespace=namespace)
    def handle_connect():
        """Event listener when client connects to the server"""
        logger.info(f"Client connected: {request.sid}")
        emit("connected", {"data": f"id: {request.sid} is connected"})

    @socketio.on("data", namespace=namespace)
    def handle_message(data):
        """Event listener when client types a message"""
        emit("data", {"data": data, "id": request.sid}, broadcast=True)

    @socketio.on("disconnect", namespace=namespace)
    def handle_disconnect():
        """Event listener when client disconnects to the server"""
        logger.info(f"Client disconnected: {request.sid}")
        emit("disconnected", f"user {request.sid} disconnected", broadcast=True)
