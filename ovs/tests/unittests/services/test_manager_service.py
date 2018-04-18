"""
Tests for manager services
"""
from ovs.tests.unittests.base_test import OVSBaseTestCase
from ovs.services.manager_service import ManagerService
from ovs.services.user_service import UserService
from ovs.datagen import DataGen

class TestManagerService(OVSBaseTestCase):
    """
    Tests for manager services
    """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        DataGen.create_defaults()

    def test_get_all_managers(self):
        """ Tests that get_all_mangers returns the correct number of users """
        expected = 5

        self.assertEqual(len(ManagerService.get_all_managers()), expected)

    def test_get_admin_count(self):
        """ Tests that get_admin_count returns the correct number of users"""
        UserService.create_user('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        expected = 2

        self.assertEqual(ManagerService.get_admin_count(), expected)
