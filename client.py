# This is the code that visits the warehouse.
from __future__ import print_function
import sys
import Pyro5.api
from Pyro5.compatibility import Pyro4

# if sys.version_info<(3,0):
#     input = raw_input

class RideSharingClient(object):
    def __init__(self, name, phone, public_key):
        self.name = name
        self.phone = phone
        self.public_key = public_key

    def info():
        return {self.public_key: {
            self.name, self.phone, 
        }}

    def sign_up(self, server):
        server.add_user(self.info())

    def get_clients(self, server):
        print(server.list_clients())


sys.excepthook = Pyro4.util.excepthook
# uri = input("Enter the uri of the warehouse: ").strip()
# warehouse = Pyro5.api.Proxy(uri)
server = Pyro5.api.Proxy("PYRONAME:sd.ridesharingapp")
giovanni = RideSharingClient("Giovanni", "41991810172", "a23456789x")
yoshio = RideSharingClient("Yoshio", "41991122445", "b2274889y")
giovanni.sign_up(server)
yoshio.sign_up(server)
yoshio.get_clients(server)