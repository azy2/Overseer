"""
The base test case that all other test cases should inherit from
"""
from flask_testing import LiveServerTestCase
from mock import patch
from ovs import create_app
from ovs import db
from ovs.datagen import DataGen


class MockBcrypt(object):
    """ Mock the Bcrypt object to avoid expensive security stuff during testing. """
    def __init__(self, app=None): # pylint: disable=unused-argument
        """ mock __init__ """
        pass

    def init_app(self, app): # pylint: disable=unused-argument
        """ mock init_app """
        pass

    def generate_password_hash(self, password, rounds=None): # pylint: disable=unused-argument, no-self-use
        """ mock generate_password_hash """
        return password

    def check_password_hash(self, pw_hash, password): # pylint: disable=unused-argument, no-self-use
        """ mock check_password_hash """
        return pw_hash == password

bcrypt_mock = MockBcrypt()

class OVSBaseTestCase(LiveServerTestCase):
    """
    The base test case that all other test cases should inherit from
    """

    def create_app(self):
        app = create_app('config/config-testing.json')
        app.config['LIVESERVER_PORT'] = 0
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
