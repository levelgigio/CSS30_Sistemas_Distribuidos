import Pyro5.api
from ride import Ride
from user import User
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pss
import base64

@Pyro5.api.expose
@Pyro5.api.behavior(instance_mode="single")
class RideSharingServer(object):
    def __init__(self):
        self.users = []
        self.rides = []
        self.current_id = 1000

    def get_offered_rides(self):
        return [ride.get_ride_json() for ride in self.rides if ride.get_is_offered()]

    def get_users(self):
        return self.users

    def sign_up(self, uri, username, phone, public_key):
        # print(public_key)
        # pub_key = RSA.import_key(public_key)
        # public_key = base64.b64decode(public_key["data"])
        user = User(uri, username, phone, public_key)
        self.users.append(user)
        # self.users.append(
        #     {"uri": uri, "username": username, "phone": phone, "public_key": public_key}
        # )
        print("Created user {}.".format(username))


    def check_if_ride_exists(self, user_uri, from_, to, date, passengers):
        possible_rides = [
            ride.get_ride_json()
            for ride in self.rides
            if (
                ride.get_location() == [from_, to]
                and ride.get_date() == date
                and ride.get_passengers() == passengers
            )
        ]
        self.get_user_object(user_uri).notify_rides(possible_rides)

    def get_user_object(self, user_uri):
        return Pyro5.api.Proxy(user_uri)

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
                "Motorista {0} tem uma carona para {1} dia {2} com {3} passageiros (id {4})".format(
                    self.get_user_object(ride.get_user()).get_name(),
                    ride.get_location()[1],
                    ride.get_date(),
                    ride.get_passengers(),
                    ride.get_id(),
                )
            )
        else:
            print(
                "Cliente {0} quer uma carona para {1} dia {2} para {3} passageiros (id {4})".format(
                    self.get_user_object(ride.get_user()).get_name(),
                    ride.get_location()[1],
                    ride.get_date(),
                    ride.get_passengers(),
                    ride.get_id(),
                )
            )

    def add_offered_ride(self, ride_json, digital_sign, message):

        message1 = message["data"]
        message1 = base64.b64decode(message1)
        receiver_hash = SHA256.new(message1)
        ride_uri = ride_json["user"]
        for user in self.users:
            if user.get_uri() == ride_json["user"]:
                pub_key = user.get_public_key()
                pub_key1 = pub_key["data"]
                pub_keya = base64.b64decode(pub_key1)
                pub_key2 = RSA.importKey(pub_keya)
                break

        # if (pub_key2 != RSA.RsaKey):
        verifier = pss.new(pub_key2)
        try:
            digital_sign1 = digital_sign["data"]
            digital_sign2 = base64.b64decode(digital_sign1)
            verifier.verify(receiver_hash, digital_sign2)
            print("The signature is authentic.")
        except (ValueError, TypeError):
            print("The signature is not authentic.")
            return 0

        offered_ride = Ride(
            user_uri=ride_json["user"],
            from_=ride_json["location"][0],
            to=ride_json["location"][1],
            date=ride_json["date"],
            passengers=ride_json["passengers"],
            offered=ride_json["offered"],
            ride_id=self.current_id,
        )
        self.current_id = self.current_id + 1
        self.print_ride(offered_ride.get_ride_json())
        self.rides.append(offered_ride)
        for ride in self.rides:
            if (
                ride.get_location() == offered_ride.get_location()
                and ride.get_date() == offered_ride.get_date()
                and ride.get_passengers() == offered_ride.get_passengers()
                and ride.get_is_offered() == 0
            ):
                try:
                    passenger_uri = ride.get_user()
                    self.get_user_object(passenger_uri).notify_rides(
                        [offered_ride.get_ride_json()]
                    )

                    driver_uri = offered_ride.get_user()
                    self.get_user_object(driver_uri).notify_rides(
                        [ride.get_ride_json()]
                    )
                except:
                    pass

        return offered_ride.get_id()

    def add_wanted_ride(self, ride_json, digital_sign, message):

        message1 = message["data"]
        message1 = base64.b64decode(message1)
        receiver_hash = SHA256.new(message1)
        ride_uri = ride_json["user"]
        for user in self.users:
            if user.get_uri() == ride_json["user"]:
                pub_key = user.get_public_key()
                pub_key1 = pub_key["data"]
                pub_keya = base64.b64decode(pub_key1)
                pub_key2 = RSA.importKey(pub_keya)
                break
        # if (pub_key != None):
        verifier = pss.new(pub_key2)
        try:
            digital_sign1 = digital_sign["data"]
            digital_sign2 = base64.b64decode(digital_sign1)
            verifier.verify(receiver_hash, digital_sign2)
            print("The signature is authentic.")
        except (ValueError, TypeError):
            print("The signature is not authentic.")
            return 0

        wanted_ride = Ride(
            user_uri=ride_json["user"],
            from_=ride_json["location"][0],
            to=ride_json["location"][1],
            date=ride_json["date"],
            passengers=ride_json["passengers"],
            offered=ride_json["offered"],
            ride_id=self.current_id,
        )
        self.current_id = self.current_id + 1
        self.print_ride(wanted_ride.get_ride_json())
        self.rides.append(wanted_ride)
        for ride in self.rides:
            if (
                ride.get_location() == wanted_ride.get_location()
                and ride.get_date() == wanted_ride.get_date()
                and ride.get_passengers() == wanted_ride.get_passengers()
                and ride.get_is_offered() == 1
            ):
                try:
                    driver_uri = ride.get_user()
                    self.get_user_object(driver_uri).notify_rides(
                        [wanted_ride.get_ride_json()]
                    )

                    passenger_uri = wanted_ride.get_user()
                    self.get_user_object(passenger_uri).notify_rides(
                        [ride.get_ride_json()]
                    )
                except:
                    pass

        return wanted_ride.get_id()

    def cancel_ride(self, ride_id):
        self.rides.remove(
            next(ride for ride in self.rides if ride.get_id() == int(ride_id))
        )
        print("Corrida {0} cancelada".format(ride_id))


def main():
    Pyro5.api.Daemon.serveSimple(
        {RideSharingServer: "sd.ridesharingapp"},
        ns=True,
        host="localhost",
        port=9091,
        verbose=True,
    )


if __name__ == "__main__":
    main()
