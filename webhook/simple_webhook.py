from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def index():
    if request.method == 'POST':
        print(request.json)
        return '', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run()
