import os

from datetime import datetime, timedelta
from flask import Flask, abort, jsonify, request

"""
Notes: Knowi's Webhook only takes HTTPS calls. To run this locally, consider using NGROK and in your Knowi account, 
pass in your NGROK HTTPS URL (i.e. https://949eas4a.ngrok.io/auth, https://949eas4a.ngrok.io/webhook)


Two step call which first validates the /auth endpoint for the WEBHOOK_VERIFY_TOKEN and AUTH_HEADER value 
before processing data sent to /webhook

"""

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
