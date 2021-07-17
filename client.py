from __future__ import print_function
import sys
import Pyro5.api
from Pyro5.compatibility import Pyro4
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from ride import Ride

# if sys.version_info<(3,0):
#     input = raw_input

class RideSharingClient(object):
    def __init__(self, name, phone):
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

    def sign_up(self, server):
        server.add_user(Proxy(self))

    def offer_ride(self, server, from_, to, date, passengers):
        ride = Ride(self, from_, to, date, passengers)
        server.add_offered_ride(ride)

    def request_ride(self, server, from_, to, date, passengers):
        ride = Ride(self, from_, to, date, passengers)
        server.add_wanted_ride(ride)

    def notify_has_ride(self, ride):
        print("Usuario {0} tem uma carona para {1} dia {2} que voce quer".format(ride.get_user().get_name(), ride.get_location()[1], ride.get_date()))


sys.excepthook = Pyro4.util.excepthook
# uri = input("Enter the uri of the warehouse: ").strip()
# warehouse = Pyro5.api.Proxy(uri)
server = Pyro5.api.Proxy("PYRONAME:sd.ridesharingapp")
giovanni = RideSharingClient("Giovanni", "41991810172")
yoshio = RideSharingClient("Yoshio", "41998956698")
giovanni.sign_up(server)
yoshio.sign_up(server)

# yoshio.offer_ride(server, "curitiba", "barra mansa", "18/07/2021", 4)
# giovanni.request_ride(server, "barra mansa", "campo grande", "18/07/2021", 1)
# giovanni.request_ride(server, "curitiba", "barra mansa", "18/07/2021", 4)