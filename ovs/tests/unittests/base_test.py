"""
The base test case that all other test cases should inherit from
"""
from flask_testing import LiveServerTestCase
from flask import current_app
from ovs import create_app


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
        with current_app.app_context():
            from ovs.datagen import DataGen
            DataGen.clear_db()
            self.db = current_app.extensions['database'].instance()

    def tearDown(self):
        """
        Runs after every tests and clears relevant tables. Subclasses should
        override this if they require additional teardown code to be run
        """
        with current_app.app_context():
            from ovs.datagen import DataGen
            DataGen.clear_db()
