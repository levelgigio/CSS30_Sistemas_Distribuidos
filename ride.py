class Ride:
    def __init__(self, user, from_, to, date, passengers):
        self.__user = user
        self.__from = from_
        self.__to = to
        self.__date = date
        self.__passengers = passengers

    def get_location():
        return {self.__from, self.__to}

    def get_date():
        return {self.__date}

    def get_passagers():
        return {self.__passengers}

    def get_user():
        return self.__user
