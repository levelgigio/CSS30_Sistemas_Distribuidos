from ride import Ride
from user import User


class RideSharingServer:
    def __init__(self):
        self.users = []
        self.rides = []
        self.current_id = 1000

    def get_offered_rides(self):
        if len(self.rides):
            return [ride for ride in self.rides if ride.get_is_offered()]
        else:
            return []

    def get_wanted_rides(self):
        if len(self.rides):
            return [ride for ride in self.rides if not ride.get_is_offered()]
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

    def get_rides(self):
        return self.rides

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
        self.rides.append(offered_ride)
        
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
        self.rides.append(wanted_ride)

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
