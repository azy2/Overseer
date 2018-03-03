""" Tests for manager services """
from unittest import TestCase
import datetime
from ovs import app
from ovs.services.user_service import UserService
from ovs.services.manager_service import ManagerService
from ovs.services.room_service import RoomService
from ovs.services.package_service import PackageService
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.package_model import Package


class TestManagerService(TestCase):
    """ Tests for manager services """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        self.tearDown()

    def tearDown(self):
        """ Runs after every tests and clears relevant tables """
        self.db.query(User).delete()
        self.db.query(Resident).delete()
        self.db.query(Room).delete()
        self.db.commit()

    def test_update_resident_room_number(self):
        """ Tests update_resident_room_number """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        RoomService.create_room('1', 'Good', 'Single')
        ManagerService.update_resident_room_number(test_user.id, '1') # <-- Not actually changing the room number... !!!
        resident = self.db.query(Resident).filter(Resident.user_id == test_user.id).first()
        self.assertEqual(resident.room_number, '1')

    def test_get_all_residents(self):
        """ Tests get_all_residents """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        UserService.create_user(*test_user_info)
        test_user_info = ('test2@gmail.com', 'Joe', 'Smith', 'RESIDENT')
        UserService.create_user(*test_user_info)
        test_user_info = ('test3@gmail.com', 'Jim', 'White', 'ADMIN')
        UserService.create_user(*test_user_info)
        residents = ManagerService.get_all_residents()
        self.assertEqual(len(residents), 2)

    def test_get_all_packages_recipients_checkers(self):
        """ Tests get_all_packages_recipients_checkers """
        user_1 = UserService.create_user('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        user_2 = UserService.create_user('test2@gmail.com', 'Jim', 'White', 'ADMIN')
        checked_at = datetime.datetime.now()
        package_description = "Fragile"
        PackageService.create_package(user_1.id, user_2.id, checked_at, package_description)
        packages_recipients_checkers = ManagerService.get_all_packages_recipients_checkers()

        self.assertEqual(len(packages_recipients_checkers), 1)
        self.assertEqual(packages_recipients_checkers[0][0].description, package_description)
        self.assertEqual(packages_recipients_checkers[0][0].checked_at, checked_at)
        self.assertEqual(packages_recipients_checkers[0][1].email, user_1.email)
        self.assertEqual(packages_recipients_checkers[0][1].role, user_1.role)
        self.assertEqual(packages_recipients_checkers[0][2].email, user_2.email)
        self.assertEqual(packages_recipients_checkers[0][2].role, user_2.role)

    def test_update_package(self):
        """ Tests update_package """
        # update_package(package_id, recipient_email, description)
        user_1 = UserService.create_user('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        user_2 = UserService.create_user('test2@gmail.com', 'Joe', 'Smith', 'RESIDENT')
        user_3 = UserService.create_user('test3@gmail.com', 'Jim', 'White', 'ADMIN')
        checked_at = datetime.datetime.now()
        package_description = "Fragile"
        package_1 = PackageService.create_package(user_1.id, user_3.id, checked_at, package_description)
        new_package_description = "NOT Fragile"
        ManagerService.update_package(package_1.id, user_2.email, new_package_description)
        updated_package_1 = self.db.query(Package).filter(Package.id == package_1.id).first()

        self.assertEqual(updated_package_1.recipient_id, user_2.id)
        self.assertEqual(updated_package_1.description, new_package_description)
