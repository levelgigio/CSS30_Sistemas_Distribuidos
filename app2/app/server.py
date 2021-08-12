from flask import Flask, Response
from time import sleep
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def construct_message(event, data):
    return f"event: {event}\ndata: {data}\n\n"


@app.route('/')
def home():
    return 'hello bacanos'


@app.route('/stream')
def stream():
    def eventStream():
        n = 0
        while True:
            yield construct_message('message', n)
            n += 1
            sleep(1)
    return Response(eventStream(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(host='localhost', port=5000)

#execute with -> python server.py
#see logs on "localhost:5000/stream"