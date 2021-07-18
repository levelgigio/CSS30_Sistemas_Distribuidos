import Pyro5.api
from Pyro5.compatibility import Pyro4
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from ride import Ride
import threading
import time


@Pyro5.api.expose
class RideSharingClient(object):
    def __init__(self):
        # self.name = None
        # self.phone = None
        # self.key_pair = None

        daemon = Pyro5.api.Daemon()  # make a Pyro daemon
        self.uri = daemon.register(self)  # register the greeting maker as a Pyro object
        threading.Thread(target=daemon.requestLoop).start()
        self.server_uri = "PYRONAME:sd.ridesharingapp"

    def create_account(self, name, phone):
        self.name = name
        self.phone = phone
        self.key_pair = self.generate_new_key_pair()

    def generate_new_key_pair(self):
        random_seed = Random.new().read
        keyPair = RSA.generate(1024, random_seed)
        return keyPair

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_public_key(self):
        return self.key_pair.publickey()

    def get_info(self):
        return (self.name, self.phone, self.public_key)

    def sign_up(self):
        self.get_server().sign_up(
            self.get_name(), self.get_phone(), self.get_public_key()
        )

    def check_if_ride_exists(self, from_, to, date, passengers):
        self.get_server().check_if_ride_exists(self.uri, from_, to, date, passengers)

    def notify_rides(self, rides):
        if len(rides):
            for ride in rides:
                self.print_ride(ride)
        else:
            print("No ride found")

    def print_ride(self, ride_json):
        ride = Ride(
            user_uri=ride_json["user"],
            from_=ride_json["location"][0],
            to=ride_json["location"][1],
            date=ride_json["date"],
            passengers=ride_json["passengers"],
            offered=ride_json["offered"],
        )
        if ride.get_is_offered():
            print(
                "Motorista {0} tem uma carona para {1} dia {2} com {3} passageiros".format(
                    self.get_user_object(ride.get_user()).get_name(),
                    ride.get_location()[1],
                    ride.get_date(),
                    ride.get_passengers(),
                )
            )
        else:
            print(
                "Cliente {0} quer uma carona para {1} dia {2} para {3} passageiros".format(
                    self.get_user_object(ride.get_user()).get_name(),
                    ride.get_location()[1],
                    ride.get_date(),
                    ride.get_passengers(),
                )
            )

    def get_server(self):
        return Pyro5.api.Proxy(self.server_uri)

    def get_user_object(self, user_uri):
        return Pyro5.api.Proxy(user_uri)

    def offer_ride(self, from_, to, date, passengers):
        ride = Ride(self.uri, from_, to, date, passengers)
        self.get_server().add_offered_ride(ride.get_ride_json())

    def request_ride(self, from_, to, date, passengers):
        ride = Ride(self.uri, from_, to, date, passengers)
        self.get_server().add_wanted_ride(ride.get_ride_json())

    # def test_server_availability(self, server):
    #     server.test()

    # def test_client(self):
    #     print(self.name)


# user = RideSharingClient()
# user.create_account("Yoshio Motorista", "4199999999")
# user.sign_up()
# user.offer_ride("curitiba", "barra mansa", "18/07/2021", 4)

user_2 = RideSharingClient()
user_2.create_account("Giovanni Passageiro", "2199219312")
user_2.sign_up()
user_2.request_ride("barra mansa", "campo grande", "18/07/2021", 1)
time.sleep(5)
user_2.request_ride("curitiba", "barra mansa", "18/07/2021", 4)

# user_3 = RideSharingClient()
# user_3.create_account("Ian Motorista", "2199219312")
# user_3.sign_up()
# user_3.offer_ride("porto velho", "campo grande", "18/07/2021", 1)
# time.sleep(5)
# user_3.offer_ride("barra mansa", "campo grande", "18/07/2021", 1)
