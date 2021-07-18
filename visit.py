# This is the code that visits the warehouse.
from __future__ import print_function
import sys
import Pyro5.api
from Pyro5.compatibility import Pyro4

# if sys.version_info<(3,0):
#     input = raw_input


class Person(object):
    def __init__(self, name):
        self.name = name

    def visit(self, warehouse):
        print("This is {0}.".format(self.name))
        self.deposit(warehouse)
        self.retrieve(warehouse)
        print("Thank you, come again!")

    def deposit(self, warehouse):
        print("The warehouse contains:", warehouse.list_contents())
        item = input("Type a thing you want to store (or empty): ").strip()
        if item:
            warehouse.store(self.name, item)

    def retrieve(self, warehouse):
        print("The warehouse contains:", warehouse.list_contents())
        item = input("Type something you want to take (or empty): ").strip()
        if item:
            warehouse.take(self.name, item)


sys.excepthook = Pyro4.util.excepthook
# uri = input("Enter the uri of the warehouse: ").strip()
# warehouse = Pyro5.api.Proxy(uri)
warehouse = Pyro5.api.Proxy("PYRONAME:example.warehouse")
janet = Person("Janet")
henry = Person("Henry")
janet.visit(warehouse)
henry.visit(warehouse)
