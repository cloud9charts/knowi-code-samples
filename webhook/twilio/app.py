from flask import Flask, abort, jsonify, request
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

ACCOUNT_SID = 'TWILIO_ACCOUNT_SID'
AUTH_TOKEN = 'TWILIO_AUTH_TOKEN'
FROM = '+1234567890'
TO = '+1234567890'

# instantiate Flask app¬ server and Twilio client
app = Flask(__name__)
client = Client(ACCOUNT_SID, AUTH_TOKEN)


@app.route('/sms', methods=['POST'])
def sms():
    if request.method == 'POST':
        try:
            knowiAlert = request.json
            smsMessage = client.messages.create(to=TO, from_=FROM, body=str(knowiAlert))
            print('SMS SUCCESSFULLY SENT: \n', knowiAlert)
            return jsonify(200)

        except TwilioRestException as e:
            print('ISSUE/ERROR WITH SMS: \n', e, )
            return abort(400)


@app.route('/ping', methods=['GET'])
def healthCheck():
    return jsonify({"response": "pong!", "status": 200})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
