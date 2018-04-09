""" Tests for package services """
from datetime import datetime

from ovs.tests.unittests.base_test import OVSBaseTestCase
from ovs.services.user_service import UserService
from ovs.services.package_service import PackageService
from ovs.models.package_model import Package


class TestPackageServce(OVSBaseTestCase):
    """ Tests for package services"""

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        self.create_test_users()

    def create_test_users(self):
        """ Creates two RESIDENT accounts and one ADMIN account for use in testing """
        self.test_resident_1 = UserService.create_user('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        self.test_resident_2 = UserService.create_user('test2@gmail.com', 'Joe', 'Smith', 'RESIDENT')
        self.test_admin = UserService.create_user('test3@gmail.com', 'Jim', 'White', 'ADMIN')

    def test_update_package(self):
        """ Tests that packages can be updated """
        checked_at = datetime.now().replace(second=0, microsecond=0)
        package_description = "Fragile"
        test_package = PackageService.create_package(self.test_resident_1.id, self.test_admin.id,
                                                     checked_at, package_description)
        new_package_description = "NOT Fragile"
        PackageService.update_package(test_package.id, self.test_resident_2.email, new_package_description)
        updated_test_package = self.db.session.query(Package).filter(Package.id == test_package.id).first()

        self.assertEqual(updated_test_package.recipient_id, self.test_resident_2.id)
        self.assertEqual(updated_test_package.description, new_package_description)
