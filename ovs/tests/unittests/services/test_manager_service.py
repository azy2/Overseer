""" Tests for manager services """
import datetime
from ovs.services.user_service import UserService
from ovs.services.manager_service import ManagerService
from ovs.services.room_service import RoomService
from ovs.services.package_service import PackageService
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.profile_model import Profile
from ovs.models.package_model import Package
from ovs.tests.unittests.base_test import OVSBaseTestCase


class TestManagerService(OVSBaseTestCase):
    """ Tests for manager services """

    def setUp(self):
        """ Runs before every test """
        super().setUp()
        self.create_test_users()

    def get_tables_used_in_tests(self):
        """
        Subclass test cases should override this to return what database objects
        correspond to tables they will need cleared before running
        """
        return [Profile, User, Resident, Room]

    def create_test_users(self):
        """ Creates two RESIDENT accounts and one ADMIN account for use in testing """
        self.test_resident_1 = UserService.create_user('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        self.test_resident_2 = UserService.create_user('test2@gmail.com', 'Joe', 'Smith', 'RESIDENT')
        self.test_admin = UserService.create_user('test3@gmail.com', 'Jim', 'White', 'ADMIN')

    def test_update_resident_room_number(self):
        """ Tests that a resident's room number can be updated """
        RoomService.create_room('1', 'Good', 'Single')

        ManagerService.update_resident_room_number(self.test_resident_1.id, '1')
        resident = self.db.query(Resident).filter(Resident.user_id == self.test_resident_1.id).first()
        self.assertEqual(resident.room_number, '1')

    def test_get_all_residents(self):
        """ Tests that get_all_residents returns the correct number of residents"""
        residents = ManagerService.get_all_residents()
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

    def test_update_package(self):
        """ Tests that packages can be updated """
        # update_package(package_id, recipient_email, description)
        checked_at = datetime.datetime.now().replace(second=0, microsecond=0)
        package_description = "Fragile"
        test_package = PackageService.create_package(self.test_resident_1.id, self.test_admin.id,
                                                     checked_at, package_description)
        new_package_description = "NOT Fragile"
        ManagerService.update_package(test_package.id, self.test_resident_2.email, new_package_description)
        updated_test_package = self.db.query(Package).filter(Package.id == test_package.id).first()

        self.assertEqual(updated_test_package.recipient_id, self.test_resident_2.id)
        self.assertEqual(updated_test_package.description, new_package_description)
