import Pyro5.api
from ride import Ride


@Pyro5.api.expose
@Pyro5.api.behavior(instance_mode="single")
class RideSharingServer(object):
    def __init__(self):
        self.users = []
        self.wanted_rides = []
        self.offered_rides = []

    def get_offered_rides(self):
        return self.offered_rides

    def add_user(self, user):
        self.users.append(user)
        print("Created user {0}.".format(user))

    def get_user_object(self, user_uri):
        return Pyro5.api.Proxy(user_uri)

    def add_offered_ride(self, ride_json):
        ride = Ride(
            user_uri=ride_json["user"],
            from_=ride_json["location"][0],
            to=ride_json["location"][1],
            date=ride_json["date"],
            passengers=ride_json["passengers"],
        )
        print(ride.get_ride_json())
        self.offered_rides.append(ride)
        for wanted_ride in self.wanted_rides:
            if (
                wanted_ride.get_location() == ride.get_location()
                and wanted_ride.get_date() == ride.get_date()
                and wanted_ride.get_passengers() == ride.get_passengers()
            ):
                try:
                    passenger_uri = wanted_ride.get_user()
                    self.get_user_object(passenger_uri).notify_offer_ride(
                        ride.get_ride_json()
                    )

                    driver_uri = ride.get_user()
                    self.get_user_object(driver_uri).notify_want_ride(
                        wanted_ride.get_ride_json()
                    )
                except:
                    pass

    def add_wanted_ride(self, ride_json):
        ride = Ride(
            user_uri=ride_json["user"],
            from_=ride_json["location"][0],
            to=ride_json["location"][1],
            date=ride_json["date"],
            passengers=ride_json["passengers"],
        )
        self.wanted_rides.append(ride)
        for offered_ride in self.offered_rides:
            if (
                offered_ride.get_location() == ride.get_location()
                and offered_ride.get_date() == ride.get_date()
                and offered_ride.get_passengers() == ride.get_passengers()
            ):
                try:
                    driver_uri = offered_ride.get_user()
                    self.get_user_object(driver_uri).notify_want_ride(
                        ride.get_ride_json()
                    )

                    passenger_uri = ride.get_user()
                    self.get_user_object(passenger_uri).notify_offer_ride(
                        offered_ride.get_ride_json()
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
