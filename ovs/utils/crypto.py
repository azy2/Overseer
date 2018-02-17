from uuid import uuid4

class Crypto:
    @staticmethod
    def generate_password():
        return uuid4().hex
