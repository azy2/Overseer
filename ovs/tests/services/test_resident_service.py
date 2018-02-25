"""
Tests for manager services
"""
from unittest import TestCase
from ovs import app
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
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

    def test_create_resident(self):
        """ Tests create_resident """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        user = UserService.create_user(*test_user_info)
        resident = self.db.query(Resident).filter(Resident.user_id == user.id).first()
        self.assertIsNotNone(resident)

    def test_create_resident_null(self):
        """ Tests create_resident """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        user = UserService.create_user(*test_user_info)
        resident = self.db.query(Resident).filter(Resident.user_id == user.id).first()
        self.assertIsNone(resident)

    def test_get_resident_by_id(self):
        """ Tests get_resident_by_id """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        resident = ResidentService.get_resident_by_id(test_user.id).first()
        self.assertIsNotNone(resident)

    def test_get_resident_by_id_null(self):
        """ Tests get_resident_by_id """
        resident = ResidentService.get_resident_by_id(4).first()
        self.assertEqual(resident, None)
