from flask import Flask, Response, request
from time import sleep
from flask_cors import CORS
from ridesharingserver import RideSharingServer
import json

server = RideSharingServer()

app = Flask(__name__)
CORS(app)


def construct_message(event, data):
    return f"event: {event}\ndata: {data}\n\n"


@app.route('/')
def home():
    return 'hello bacanos'

@app.route('/get_rides')
def get_ride():
    offered_rides = server.get_offered_rides()
    print('rides in server', offered_rides)
    return json.dumps(offered_rides)

@app.route('/offer_or_want_ride', methods=['POST'])
def offer_ride():
    ride_json = json.loads(request.data)
    print(ride_json)
    if ride_json['offered'] == 1:
        server.add_offered_ride(ride_json)
    else:
        server.add_wanted_ride(ride_json)
    return "ok"

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