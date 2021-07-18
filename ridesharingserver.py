from __future__ import print_function
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

    def add_offered_ride(self, ride):
        self.offered_rides.append(ride)
        for wanted_ride in self.wanted_rides:
            if (
                wanted_ride.get_location() == ride.get_location()
                and wanted_ride.get_date() == ride.get_date()
                and wanted_ride.get_passengers() == ride.get_passengers()
            ):
                wanted_ride.get_user().notify_has_ride(ride)

    def add_wanted_ride(self, ride):
        self.wanted_rides.append(ride)
        for offered_ride in self.offered_rides:
            if (
                offered_ride.get_location() == ride.get_location()
                and offered_ride.get_date() == ride.get_date()
                and offered_ride.get_passengers() == ride.get_passengers()
            ):
                offered_ride.get_user().notify_has_ride(ride)

    def test(self):
        print("Hi I am avalialble")

    def test_clients(self):
        for user in self.users:
            try:
                user_object = Pyro5.api.Proxy(user)
                print(user_object.get_name())
                user_object.test_client()
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
