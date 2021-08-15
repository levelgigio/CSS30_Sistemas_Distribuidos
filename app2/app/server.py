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


@app.route("/")
def home():
    return "Server is running"


@app.route("/get_rides")
def get_ride():
    return_list = []
    offered_rides = server.get_offered_rides()
    for ride in offered_rides:
        return_list.append(ride.get_ride_json())
    print("rides in server", return_list)
    return json.dumps(return_list)


@app.route("/offer_or_want_ride", methods=["POST"])
def offer_ride():
    ride_json = json.loads(request.data)
    print(ride_json)
    id = None
    if ride_json["offered"] == 1:
        id = server.add_offered_ride(ride_json)
    else:
        id = server.add_wanted_ride(ride_json)
    return f"Created ride with id {id}"


@app.route("/cancel_ride", methods=["POST"])
def cancel_ride():
    id = request.data
    server.cancel_ride(id)
    return "ok"


@app.route("/stream/<client_id>")
def stream(client_id):
    def eventStream():
        while True:
            client_rides = []
            for ride in server.get_wanted_rides():
                if ride.get_user() == client_id:
                    client_rides.append(ride)
                    print("cliente tem corridas que ele quer")

            response_offered = []

            for ride in client_rides:
                for r in server.get_offered_rides():
                    if (
                        ride.get_location() == r.get_location()
                        and ride.get_date() == r.get_date()
                        and ride.get_passengers() == r.get_passengers()
                        and ride.get_is_offered() == 0
                    ):
                        print("alguem tem a corrida que o cliente quer")
                        response_offered.append(
                            f"Motorista {r.get_user()} tem uma carona de {r.get_location()[0]} para {r.get_location()[1]} dia {r.get_date()} com {r.get_passengers()} passageiros (id {r.get_id()})."
                        )
            # if len(response_offered):
            #     print("\n".join(response_offered))
            #     yield construct_message("message", "---".join(response))

            # ------------------------

            client_rides = []
            for ride in server.get_offered_rides():
                if ride.get_user() == client_id:
                    client_rides.append(ride)
                    print("cliente ofereceu corridas")

            response_wanted = []

            for ride in client_rides:
                for r in server.get_wanted_rides():
                    if (
                        ride.get_location() == r.get_location()
                        and ride.get_date() == r.get_date()
                        and ride.get_passengers() == r.get_passengers()
                        and ride.get_is_offered() == 1
                    ):
                        print("alguem quer a corrida que usuario ofereceu")
                        response_wanted.append(
                            f"Passageiro {r.get_user()} quer uma carona de {r.get_location()[0]} para {r.get_location()[1]} dia {r.get_date()} com {r.get_passengers()} passageiros (id {r.get_id()})."
                        )
            response = []
            response.extend(response_wanted)
            response.extend(response_offered)
            if len(response):

                print("\n".join(response))
                yield construct_message("message", "---".join(response))

            sleep(1)

    return Response(eventStream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="localhost", port=5000)

# execute with -> python server.py
# see logs on "localhost:5000/stream"
