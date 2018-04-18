""" Utility classes for doing secure cryptography """
from uuid import uuid4


class Crypto:
    """ Utility methods for doing secure cryptography """

    def __init__(self):
        pass

    @staticmethod
    def generate_password():
        """
        Get a default password

        Returns:
            Generate a random password
        """
        return uuid4().hex
