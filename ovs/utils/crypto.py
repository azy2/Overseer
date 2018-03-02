""" Utility classes for doing secure cryptography """
from uuid import uuid4

class Crypto:
    """ Utility methods for doing secure cryptography """
    @staticmethod
    def generate_password():
        """ Generate a random password """
        return uuid4().hex
