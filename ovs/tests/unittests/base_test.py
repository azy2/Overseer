"""
The base test case that all other test cases should inherit from
"""
from unittest import TestCase
from ovs import app


class OVSBaseTestCase(TestCase):
    """
    The base test case that all other test cases should inherit from
    """
    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        self.clear_relevant_database_tables()

    def tearDown(self):
        """
        Runs after every tests and clears relevant tables. Subclasses should
        override this if they require additional teardown code to be run
        """
        self.clear_relevant_database_tables()

    def clear_relevant_database_tables(self):
        """ Clears the database tables relevant for the current test case """
        tables_to_clear = self.get_tables_used_in_tests()
        if tables_to_clear is None:
            return

        # Clear database tables
        for database_object in iter(tables_to_clear):
            self.db.query(database_object).delete()

        self.db.commit()

    # pylint: disable=no-self-use
    def get_tables_used_in_tests(self):
        """
        Subclass test cases should override this to return what database objects
        correspond to tables they will need cleared before running
        """
        return None
