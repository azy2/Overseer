""" Tests for manager services """
import datetime

from ovs.services.user_service import UserService
from ovs.services.manager_service import ManagerService
from ovs.services.package_service import PackageService
from ovs.tests.unittests.base_test import OVSBaseTestCase


class TestManagerService(OVSBaseTestCase):
    """ Tests for manager services """

    def setUp(self):
        """ Runs before every test """
        super().setUp()
        self.create_test_users()

    def create_test_users(self):
        """ Creates two RESIDENT accounts and one ADMIN account for use in testing """
        self.test_resident_1 = UserService.create_user('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        self.test_resident_2 = UserService.create_user('test2@gmail.com', 'Joe', 'Smith', 'RESIDENT')
        self.test_admin = UserService.create_user('test3@gmail.com', 'Jim', 'White', 'ADMIN')

    def test_get_all_residents_users(self):
        """ Tests that get_all_residents_users returns the correct number of residents"""
        residents = ManagerService.get_all_residents_users()
        self.assertEqual(len(residents), 2)

    def test_get_all_packages_recipients_checkers(self):
        """ Tests get_all_packages_recipients_checkers are expected checkers """
        checked_at = datetime.datetime.now().replace(second=0, microsecond=0)
        package_description = 'Fragile'
        PackageService.create_package(self.test_resident_1.id, self.test_admin.id, checked_at, package_description)
        packages_recipients_checkers = ManagerService.get_all_packages_recipients_checkers()

        self.assertEqual(len(packages_recipients_checkers), 1)
        self.assertEqual(packages_recipients_checkers[0][0].description, package_description)
        self.assertEqual(packages_recipients_checkers[0][0].checked_at, checked_at)
        self.assertEqual(packages_recipients_checkers[0][1].email, self.test_resident_1.email)
        self.assertEqual(packages_recipients_checkers[0][1].role, self.test_resident_1.role)
        self.assertEqual(packages_recipients_checkers[0][2].email, self.test_admin.email)
        self.assertEqual(packages_recipients_checkers[0][2].role, self.test_admin.role)
