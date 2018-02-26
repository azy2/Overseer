"""
Tests for manager services
"""
from unittest import TestCase
from ovs import app
from ovs.services.user_service import UserService
from ovs.services.manager_service import ManagerService
from ovs.services.room_service import RoomService
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room


class TestManagerService(TestCase):
    """
    Tests for manager services
    """
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
        """ Tests create_user """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        RoomService.create_room('1', 'Good', 'Single')
        ManagerService.update_resident_room_number(test_user.id, '1')
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
