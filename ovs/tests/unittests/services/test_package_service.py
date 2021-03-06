""" Tests for package services """
from datetime import datetime

from ovs.tests.unittests.base_test import OVSBaseTestCase
from ovs.services.user_service import UserService
from ovs.services.package_service import PackageService
from ovs.models.package_model import Package
from ovs.datagen import DataGen


class TestPackageService(OVSBaseTestCase):
    """ Tests for package services"""

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        self.create_test_users()

    def create_test_users(self):
        """ Creates two RESIDENT accounts and one ADMIN account for use in testing """
        DataGen.create_default_room()
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
        updated_test_package = Package.query.filter(Package.id == test_package.id).first()

        self.assertEqual(updated_test_package.recipient_id, self.test_resident_2.id)
        self.assertEqual(updated_test_package.description, new_package_description)

    def test_get_all_packages_recipients(self):
        """ Tests get_all_packages_recipients contains a package """
        checked_at = datetime.now().replace(second=0, microsecond=0)
        package_description = 'Fragile'
        PackageService.create_package(self.test_resident_1.id, self.test_admin.id, checked_at, package_description)
        packages_recipients = PackageService.get_all_packages_recipients()

        self.assertEqual(len(packages_recipients), 1)
        self.assertEqual(packages_recipients[0][0].description, package_description)
        self.assertEqual(packages_recipients[0][0].checked_at, checked_at)
        self.assertEqual(packages_recipients[0][1].email, self.test_resident_1.email)
        self.assertEqual(packages_recipients[0][1].role, self.test_resident_1.role)
