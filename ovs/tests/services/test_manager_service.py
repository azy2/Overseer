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


class TestUserService(TestCase):
    """
    Tests for manager services
    """
    def setUp(self):
        """ Runs before every test and clears the user table """
        self.db = app.database.instance()
        self.tearDown()

    def tearDown(self):
        """ Runs after every tests and clears the user table """
        self.db.query(User).delete()
        self.db.query(Resident).delete()
        self.db.query(Room).delete()
        self.db.commit()

    def test_get_resident_by_id(self):
        """ Tests get_resident_by_id """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        resident = ManagerService.get_resident_by_id(test_user.id)
        self.assertIsNotNone(resident)

    def test_get_resident_by_id_null(self):
        """ Tests get_resident_by_id """
        resident = ManagerService.get_resident_by_id(4)
        self.assertEqual(resident, None)


    def test_update_resident_room_number(self):
        """ Tests update_resident_room_number """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        RoomService.create_room('1', 'Good', 'Single')
        ManagerService.update_resident_room_number(test_user.id, '1')
        resident = self.db.query(Resident).filter(Resident.user_id == test_user.id).first()
        self.assertEqual(resident.room_number, '1')
