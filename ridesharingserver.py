import Pyro5.api
from ride import Ride


@Pyro5.api.expose
@Pyro5.api.behavior(instance_mode="single")
class RideSharingServer(object):
    def __init__(self):
        self.users = []
        self.rides = []
        # self.offered_rides = []

    def get_offered_rides(self):
        return [ride.get_ride_json() for ride in self.rides if ride.get_is_offered()]

    def sign_up(self, username, phone, public_key):
        self.users.append(
            {"username": username, "phone": phone, "public_key": public_key}
        )
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

    def add_offered_ride(self, ride_json):
        offered_ride = Ride(
            user_uri=ride_json["user"],
            from_=ride_json["location"][0],
            to=ride_json["location"][1],
            date=ride_json["date"],
            passengers=ride_json["passengers"],
            offered=1,
        )
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

    def add_wanted_ride(self, ride_json):
        wanted_ride = Ride(
            user_uri=ride_json["user"],
            from_=ride_json["location"][0],
            to=ride_json["location"][1],
            date=ride_json["date"],
            passengers=ride_json["passengers"],
            offered=0,
        )
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
