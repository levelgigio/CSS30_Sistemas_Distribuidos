import Pyro5.api
from Pyro5.compatibility import Pyro4
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from ride import Ride
import threading

@Pyro5.api.expose
class RideSharingClient(object):
    def __init__(self):
        self.name = None
        self.phone = None
        self.key_pair = None
        self.uri = None
    
    def create_account(self, name, phone):
        self.name = name
        self.phone = phone
        self.key_pair = self.generate_new_key_pair()

    def set_uri(self, uri):
        self.uri = uri

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

    @Pyro5.api.expose
    def get_info(self):
        return (self.name, self.phone, self.public_key)

    def sign_up(self, server):
        server.add_user(self.uri)

    def offer_ride(self, server, from_, to, date, passengers):
        ride = Ride(self, from_, to, date, passengers)
        server.add_offered_ride(ride)

    def request_ride(self, server, from_, to, date, passengers):
        ride = Ride(self, from_, to, date, passengers)
        server.add_wanted_ride(ride)

    def notify_has_ride(self, ride):
        print(
            "Usuario {0} tem uma carona para {1} dia {2} que voce quer".format(
                ride.get_user().get_name(), ride.get_location()[1], ride.get_date()
            )
        )

    # def test_server_availability(self, server):
    #     server.test()

    # def test_client(self):
    #     print(self.name)



user = RideSharingClient()
daemon = Pyro5.api.Daemon()  # make a Pyro daemon
uri = daemon.register(user)  # register the greeting maker as a Pyro object
threading.Thread(target=daemon.requestLoop).start()
user.set_uri(uri)
user.create_account("Giovanni", "Forastieri")
server = Pyro5.api.Proxy("PYRONAME:sd.ridesharingapp")
print(user.get_name())
user.sign_up(server)
server.test_clients()

