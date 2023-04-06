from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from handle_query import start_query


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api', methods=['POST'])
def api():
    # Get the request data
    data = request.get_json()

    # Do some processing with the data
    response = process_request(data)

    # Return the response
    return response


def process_request(data):
    # Process the request data here and return a response
    response_data = "Your request was processed successfully!"
    response = Response(response_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(port=5000)
