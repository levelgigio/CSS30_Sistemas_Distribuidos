from __future__ import print_function
import Pyro5.api

@Pyro5.api.expose
@Pyro5.api.behavior(instance_mode="single")
class RideSharingServer(object):
    def __init__(self):
        self.users = []
        self.wanted_rides = []
        self.offered_rides = []

    def list_clients(self):
        return self.users

    def get_offered_rides(self):
        return self.offered_rides
    
    def add_user(self, user):
        self.users.append(user)
        print("Created user {0}.".format(user))


def main():
    Pyro5.api.Daemon.serveSimple(
            {
                RideSharingServer: "sd.ridesharingapp"
            },
            ns=True, host="localhost", port=9090, verbose=True)

if __name__=="__main__":
    main()