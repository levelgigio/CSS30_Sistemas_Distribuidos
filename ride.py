class Ride:
    def __init__(self, user_uri=None, from_=None, to=None, date=None, passengers=None):
        self.__user_uri = user_uri
        self.__from = from_
        self.__to = to
        self.__date = date
        self.__passengers = passengers

    def get_location(self):
        return [self.__from, self.__to]

    def get_date(self):
        return self.__date

    def get_passengers(self):
        return self.__passengers

    def get_user(self):
        return self.__user_uri

    def get_ride_json(self):
        return {
            "location": self.get_location(),
            "date": self.get_date(),
            "passengers": self.get_passengers(),
            "user": self.get_user(),
        }

    # def create_ride_from_json(self, ride_json):
    #     return Ride(
    #         ride_json["user"],
    #         ride_json["location"][0],
    #         ride_json["location"][1],
    #         ride_json["date"],
    #         ride_json["passengers"],
    #     )
