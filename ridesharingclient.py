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
        self.my_rides = []

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
            print("Nenhuma corrida encontrada")

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
        ride = Ride(self.uri, from_, to, date, passengers, 1)
        ride_id = self.get_server().add_offered_ride(ride.get_ride_json())
        self.my_rides.append(ride_id)
        print(
            "A corrida oferecida de {0} para {1} para o dia {2} com {3} passageiros tem o id de {4}".format(
                from_, to, date, passengers, ride_id
            )
        )

    def request_ride(self, from_, to, date, passengers):
        ride = Ride(self.uri, from_, to, date, passengers, 0)
        ride_id = self.get_server().add_wanted_ride(ride.get_ride_json())
        self.my_rides.append(ride_id)
        print(
            "A corrida requisitada de {0} para {1} para o dia {2} com {3} passageiros tem o id de {4}".format(
                from_, to, date, passengers, ride_id
            )
        )

    def cancel_ride(self, ride_id):
        self.get_server().cancel_ride(ride_id)


user = RideSharingClient()
print("Crie sua conta")
name = input("Qual seu nome? ")
phone = input("Qual seu telefone? ")
user.create_account(name, phone)
user.sign_up()

while True:
    print("O que voce quer fazer?")
    print("o - para oferecer uma corrida")
    print("r - para requisitar uma corrida")
    print("b - para buscar uma corrida")
    print("c - para cancelar uma corrida")
    command = input("Entre com o comando: ")
    if command == 'o':
        from_ = input("Partindo de: ")
        to = input("Para: ")
        date = input("Na data de (use o formato DD/MM/YYYY: ")
        passengers = input("Para quantos passageiros? ")
        user.offer_ride(from_, to, date, passengers)

    elif command == 'r':
        from_ = input("Partindo de: ")
        to = input("Para: ")
        date = input("Na data de (use o formato DD/MM/YYYY: ")
        passengers = input("Para quantos passageiros? ")
        user.request_ride(from_, to, date, passengers)
    
    elif command == 'b':
        from_ = input("Partindo de: ")
        to = input("Para: ")
        date = input("Na data de (use o formato DD/MM/YYYY: ")
        passengers = input("Para quantos passageiros? ")
        user.check_if_ride_exists(from_, to, date, passengers)
    
    elif command == 'c':
        ride_id = input("Id da corrida a ser cancelada: ")
        user.cancel_ride(ride_id)

    else:
        print("Comando invalido")