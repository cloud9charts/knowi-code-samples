from datetime import datetime, timedelta
import os

from flask import Flask, abort, jsonify, request

WEBHOOK_VERIFY_TOKEN = os.environ.get('WEBHOOK_VERIFY_TOKEN')
AUTH_HEADER = os.environ.get('AUTH_HEADER')
CLIENT_AUTH_TIMEOUT = 24  # in Hours

app = Flask(__name__)

authorizedClients = {}


@app.route('/auth', methods=['POST'])
def auth():
    """
    Send a POST request to localhost:5000/auth with specified header and webhook token to authenticate request before
    /webhook content is is called
    """
    if request.method == 'POST':
        headers = request.headers.get('x-api-key')
        verify_token = request.args.get('verifyToken')

        if verify_token != WEBHOOK_VERIFY_TOKEN or headers != AUTH_HEADER:
            return jsonify({'status': 'bad token'}), 401
        else:
            authorizedClients[request.remote_addr] = datetime.now()
            return jsonify({'status': 'success'}), 200


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Sends content after authentication to localhost:5000/webhook
    """
    if request.method == 'POST':
        client = request.remote_addr
        if client in authorizedClients:
            if datetime.now() - authorizedClients.get(client) > timedelta(hours=CLIENT_AUTH_TIMEOUT):
                authorizedClients.pop(client)
                return jsonify({'status': 'authorisation timeout'}), 401
            else:
                print(request.json)
                return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'not authorised'}), 401

    else:
        abort(400)


if __name__ == '__main__':
    app.run()

"""
# https://ogma-dev.github.io/posts/simple-flask-webhook/
- need to use NGROK since knowi only takes HTTPS requests


url to invoke: https://9449ef4a.ngrok.io/webhook
auth url: https://9449ef4a.ngrok.io/auth?verifyToken=knowi
auth header: x-api-key: 5d9606972ed4db16bdb2d620
"""
