class User:
    def __init__(self, uri=None, username=None, phone=None, public_key=None):
        self.__uri = uri
        self.__username = username
        self.__phone = phone
        self.__public_key = public_key

    def get_uri(self):
        return self.__uri

    def get_username(self):
        return self.__username

    def get_phone(self):
        return self.__phone

    def get_public_key(self):
        return self.__public_key
