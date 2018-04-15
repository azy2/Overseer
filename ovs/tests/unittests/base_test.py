"""
The base test case that all other test cases should inherit from
"""
from flask_testing import LiveServerTestCase
from ovs import create_app
from ovs import db
from ovs.datagen import DataGen


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

    def tearDown(self):
        """
        Runs after every tests and clears relevant tables. Subclasses should
        override this if they require additional teardown code to be run
        """
        DataGen.clear_db()
