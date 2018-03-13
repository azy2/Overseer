""" Tests for manager services """
import datetime
from unittest import TestCase

from ovs import app
from ovs.models.profile_model import Profile
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.user_model import User
from ovs.services.manager_service import ManagerService
from ovs.services.package_service import PackageService
from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService


class TestManagerService(TestCase):
    """ Tests for manager services """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        self.tearDown()

    def tearDown(self):
        """ Runs after every tests and clears relevant tables """
        self.db.query(Profile).delete()
        self.db.query(User).delete()
        self.db.query(Resident).delete()
        self.db.query(Room).delete()
        self.db.commit()

    def test_update_resident_room_number(self):
        """ Tests update_resident_room_number """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        RoomService.create_room('1', 'Good', 'Single')
        ManagerService.update_resident_room_number(test_user.id,
                                                   '1')  # <-- Not actually changing the room number... !!!
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
        checked_at = datetime.datetime.now().replace(second=0, microsecond=0)
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
