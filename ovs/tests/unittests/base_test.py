"""
The base test case that all other test cases should inherit from
"""
from flask_testing import LiveServerTestCase
from mock import patch
from ovs import create_app
from ovs import db
from ovs.datagen import DataGen


def mock_generate_password_hash(self, password, rounds=None): # pylint: disable=unused-argument
    """ Mocks password hashing during tests. """
    return password

def mock_check_password_hash(self, pw_hash, password): # pylint: disable=unused-argument
    """ Mocks a password compare during tests """
    return pw_hash == password

class OVSBaseTestCase(LiveServerTestCase):
    """
    The base test case that all other test cases should inherit from
    """

    def create_app(self):
        app = create_app()
        app.config['LIVESERVER_PORT'] = 0
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        DataGen.clear_db()
        self.db = db
        DataGen.create_default_room()
        self.hash_patch = patch('flask_bcrypt.Bcrypt.generate_password_hash',
                                new=mock_generate_password_hash)
        self.addCleanup(self.hash_patch.stop)
        self.hash_patch.start()
        self.check_hash_patch = patch('flask_bcrypt.Bcrypt.check_password_hash',
                                      new=mock_check_password_hash)
        self.addCleanup(self.check_hash_patch.stop)
        self.check_hash_patch.start()

    def tearDown(self):
        """
        Runs after every tests and clears relevant tables. Subclasses should
        override this if they require additional teardown code to be run
        """
        DataGen.clear_db()
