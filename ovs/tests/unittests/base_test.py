"""
The base test case that all other test cases should inherit from
"""
from flask_testing import TestCase
from mock import patch
from ovs import create_app
from ovs import db
from ovs.datagen import DataGen


class MockBcrypt(object):
    """ Mock the Bcrypt object to avoid expensive security stuff during testing. """
    def __init__(self, app=None): # pylint: disable=unused-argument
        """
        Does nothing.
        Args:
            app: Unused.
        """
        pass

    def init_app(self, app): # pylint: disable=unused-argument
        """
        Does nothing.
        Args:
            app: Unused.
        """
        pass

    def generate_password_hash(self, password, rounds=None): # pylint: disable=unused-argument, no-self-use
        """
        Mock generate_password_hash to speed up tests.
        Args:
            password: The password to not hash.
            rounds: The number of rounds Bcrypt would have applied a hash.

        Returns:
            password
        """
        return password

    def check_password_hash(self, pw_hash, password): # pylint: disable=unused-argument, no-self-use
        """
        Since we aren't hashing passwords logging in is as simple as comparing plaintext.
        Args:
            pw_hash: The password the user typed in.
            password: The password the account has.

        Returns:
            bool: True if they are the same.
        """
        return pw_hash == password

bcrypt_mock = MockBcrypt()

class OVSBaseTestCase(TestCase):
    """
    The base test case that all other test cases should inherit from
    """

    def create_app(self):
        """
        Creates a Flask app for use during each test.
        Returns:
            Flask: a unique flask app for this test.
        """
        app = create_app('config/config-testing.json')
        return app

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        DataGen.clear_db()
        self.db = db
        DataGen.create_default_room()
        self.bcrypt_patch = patch('ovs.models.user_model.Bcrypt',
                                  new=bcrypt_mock)
        self.addCleanup(self.bcrypt_patch.stop)
        self.bcrypt_patch.start()

    def tearDown(self):
        """
        Runs after every tests and clears relevant tables. Subclasses should
        override this if they require additional teardown code to be run
        """
        DataGen.clear_db()
