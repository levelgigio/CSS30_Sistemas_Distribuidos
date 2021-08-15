import Pyro5.api
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from ride import Ride
import threading
import os
from Crypto.Signature import pss


@Pyro5.api.expose
class RideSharingClient(object):
    def __init__(self):
        daemon = Pyro5.api.Daemon()  # make a Pyro daemon
        self.uri = daemon.register(self)  # register the greeting maker as a Pyro object
        threading.Thread(target=daemon.requestLoop).start()
        self.my_rides = []

    def create_account(self, name, phone):
        self.name = name
        self.phone = phone
        self.key_pair = self.generate_new_key_pair()

    def generate_new_key_pair(self):
        random_seed = Random.new().read
        keyPair = RSA.generate(1024, random_seed)
        return keyPair

    def get_uri(self):
        return self.uri

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_public_key(self):
        return self.key_pair.publickey()

    def get_info(self):
        return (self.uri, self.name, self.phone, self.public_key)

    def sign_up(self):
        publickey = self.get_public_key()
        publickey = publickey.export_key("PEM")
        self.get_server().sign_up(
            self.get_uri(), self.get_name(), self.get_phone(), publickey
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
            ride_id=ride_json["ride_id"],
        )
        if ride.get_is_offered():
            print(
                "Motorista {0} tem uma carona de {5} para {1} dia {2} com {3} passageiros (id {4}) \n".format(
                    self.get_user_object(ride.get_user()).get_name(),
                    ride.get_location()[1],
                    ride.get_date(),
                    ride.get_passengers(),
                    ride.get_id(),
                    ride.get_location()[0],
                )
            )
        else:
            print(
                "Cliente {0} quer uma carona de {5} para {1} dia {2} para {3} passageiros (id {4})\n".format(
                    self.get_user_object(ride.get_user()).get_name(),
                    ride.get_location()[1],
                    ride.get_date(),
                    ride.get_passengers(),
                    ride.get_id(),
                    ride.get_location()[0],
                )
            )

    def get_server(self):
        nameserver = Pyro5.api.locate_ns()
        uri = nameserver.lookup("sd.ridesharingapp")
        return Pyro5.api.Proxy(uri)

    def get_user_object(self, user_uri):
        return Pyro5.api.Proxy(user_uri)

    def offer_ride(self, from_, to, date, passengers):
        ride = Ride(self.uri, from_, to, date, passengers, 1)
        message = "offering ride"
        message = message.encode("utf-8")
        hash = SHA256.new(message)
        digital_sign = pss.new(self.key_pair).sign(hash)
        ride_id = self.get_server().add_offered_ride(
            ride.get_ride_json(), digital_sign, message
        )
        if ride_id != 0:
            ride.set_id(ride_id)
            self.my_rides.append(ride)
            print(
                "A corrida oferecida de {0} para {1} para o dia {2} com {3} passageiros tem o id de {4}".format(
                    from_, to, date, passengers, ride_id
                )
            )
        else:
            print("Não foi possível cadastrar a corrida a ser oferecida.")

    def request_ride(self, from_, to, date, passengers):
        ride = Ride(self.uri, from_, to, date, passengers, 0)
        message = "requesting ride"
        message = message.encode("utf-8")
        hash = SHA256.new(message)
        digital_sign = pss.new(self.key_pair).sign(hash)
        ride_id = self.get_server().add_wanted_ride(
            ride.get_ride_json(), digital_sign, message
        )
        if ride_id != 0:
            ride.set_id(ride_id)
            self.my_rides.append(ride)
            print(
                "A corrida requisitada de {0} para {1} para o dia {2} com {3} passageiros tem o id de {4} \n".format(
                    from_, to, date, passengers, ride_id
                )
            )
        else:
            print("Não foi possível cadastrar a corrida a ser requisitada.")

    def cancel_ride(self, ride_id):
        if self.get_server().cancel_ride(ride_id) == 1:
            self.my_rides.remove(
                next(ride for ride in self.my_rides if ride.get_id() == int(ride_id))
            )
            print("Corrida {0} cancelada".format(ride_id))
        else:
            print("Corrida {0} nao existe e nao pode ser cancelada".format(ride_id))

    def print_my_rides(self):
        if len(self.my_rides):
            for ride in self.my_rides:
                self.print_ride(ride.get_ride_json())
        else:
            print("Voce nao tem corridas")


user = RideSharingClient()
print("Crie sua conta")
name = input("Qual seu nome? ")
phone = input("Qual seu telefone? ")
user.create_account(name, phone)
user.sign_up()
os.system("cls" if os.name == "nt" else "clear")
print()
print("Usuario {} criado".format(name))

while True:
    print("O que voce quer fazer?")
    print("o - para oferecer uma corrida")
    print("r - para requisitar uma corrida")
    print("b - para buscar uma corrida")
    print("c - para cancelar uma corrida")
    print("m - minhas corridas")
    command = input("Entre com o comando: \n")
    if command == "o":
        from_ = input("Partindo de: ")
        to = input("Para: ")
        date = input("Na data de (use o formato DD/MM/YYYY): ")
        passengers = input("Para quantos passageiros? ")
        os.system("cls" if os.name == "nt" else "clear")
        print()
        user.offer_ride(from_, to, date, passengers)

    elif command == "r":
        from_ = input("Partindo de: ")
        to = input("Para: ")
        date = input("Na data de (use o formato DD/MM/YYYY):")
        passengers = input("Para quantos passageiros? ")
        os.system("cls" if os.name == "nt" else "clear")
        print()
        user.request_ride(from_, to, date, passengers)

    elif command == "b":
        from_ = input("Partindo de: ")
        to = input("Para: ")
        date = input("Na data de (use o formato DD/MM/YYYY): ")
        passengers = input("Para quantos passageiros? ")
        os.system("cls" if os.name == "nt" else "clear")
        print()
        user.check_if_ride_exists(from_, to, date, passengers)

    elif command == "c":
        ride_id = input("Id da corrida a ser cancelada: ")
        os.system("cls" if os.name == "nt" else "clear")
        print()
        user.cancel_ride(ride_id)

    elif command == "m":
        os.system("cls" if os.name == "nt" else "clear")
        print()
        user.print_my_rides()

    else:
        os.system("cls" if os.name == "nt" else "clear")
        print()
        print("Comando invalido")
