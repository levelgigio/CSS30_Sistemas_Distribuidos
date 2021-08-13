from ride import Ride
from user import User


class RideSharingServer():
    def __init__(self):
        self.users = []
        self.rides = []
        self.current_id = 1000

    def get_offered_rides(self):
        if len(self.rides):
            return [ride.get_ride_json() for ride in self.rides if ride.get_is_offered()]
        else:
            return []

    def get_users(self):
        return self.users

    def sign_up(self, uri, username, phone):
        user = User(uri, username, phone)
        self.users.append(user)
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
        # self.get_user_object(user_uri).notify_rides(possible_rides)

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
                "Motorista {0} tem uma carona de {5} para {1} dia {2} com {3} passageiros (id {4})".format(
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
                "Cliente {0} quer uma carona de {5} para {1} dia {2} para {3} passageiros (id {4})".format(
                    self.get_user_object(ride.get_user()).get_name(),
                    ride.get_location()[1],
                    ride.get_date(),
                    ride.get_passengers(),
                    ride.get_id(),
                    ride.get_location()[0],
                )
            )

    

    def add_offered_ride(self, ride_json):
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
        # self.print_ride(offered_ride.get_ride_json())
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
                    # self.get_user_object(passenger_uri).notify_rides(
                    #     [offered_ride.get_ride_json()]
                    # )

                    # driver_uri = offered_ride.get_user()
                    # self.get_user_object(driver_uri).notify_rides(
                    #     [ride.get_ride_json()]
                    # )
                except:
                    pass

        return offered_ride.get_id()

    def add_wanted_ride(self, ride_json):
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
                    # self.get_user_object(driver_uri).notify_rides(
                    #     [wanted_ride.get_ride_json()]
                    # )

                    # passenger_uri = wanted_ride.get_user()
                    # self.get_user_object(passenger_uri).notify_rides(
                    #     [ride.get_ride_json()]
                    # )
                except:
                    pass

        return wanted_ride.get_id()

    def cancel_ride(self, ride_id):
        try:
            self.rides.remove(
                next(ride for ride in self.rides if ride.get_id() == int(ride_id))
            )
            print("Corrida {0} cancelada".format(ride_id))
            return 1
        except:
            print("Corrida {0} nao existe e nao pode ser cancelada".format(ride_id))
            return 0