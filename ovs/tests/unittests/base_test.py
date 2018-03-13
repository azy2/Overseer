"""
The base test case that all other test cases should inherit from
"""
from unittest import TestCase
from ovs import DataGen
from ovs import app


class OVSBaseTestCase(TestCase):
    """
    The base test case that all other test cases should inherit from
    """

    @classmethod
    def setUpClass(cls):
        """ Sets the app config to TESTING mode """
        app.config['TESTING'] = True

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        DataGen.clear_db()

    def tearDown(self):
        """
        Runs after every tests and clears relevant tables. Subclasses should
        override this if they require additional teardown code to be run
        """
        DataGen.clear_db()
