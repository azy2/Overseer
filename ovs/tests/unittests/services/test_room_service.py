"""
Tests for room services
"""
from unittest import TestCase
from ovs import app
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.room_service import RoomService
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.profile_model import Profile


class TestRoomService(TestCase):
    """
    Tests for room services
    """
    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        self.tearDown()
        self.create_test_room()

    def tearDown(self):
        """ Runs after every tests and clears relevant tables """
        self.db.query(Profile).delete()
        self.db.query(User).delete()
        self.db.query(Resident).delete()
        self.db.query(Room).delete()
        self.db.commit()

    def create_test_room(self):
        """ Creates a room for use in testing  """
        self.test_room_info = ('5', 'Good', 'Single')
        self.test_room = RoomService.create_room(*self.test_room_info)

    def test_create_room(self):
        """ Tests that rooms can be created """
        room = self.db.query(Room).filter(Room.id == self.test_room.id).first()
        self.assertEqual((room.number, room.status, room.type), self.test_room_info)

    def test_get_room_by_id(self):
        """ Tests that get_room_by_id returns the correct room """
        room = RoomService.get_room_by_id(self.test_room.id).first()
        self.assertEqual((room.number, room.status, room.type), self.test_room_info)

    def test_invalid_get_room_by_id(self):
        """ Tests that get_room_by_id returns None for an invalid room id """
        room = RoomService.get_room_by_id(5).first()
        self.assertIsNone(room)

    def test_get_room_by_number(self):
        """ Tests that get_room_by_number returns the correct room """
        room = RoomService.get_room_by_number(self.test_room.number).first()
        self.assertEqual((room.number, room.status, room.type), self.test_room_info)

    def test_invalid_get_room_by_number(self):
        """ Tests that get_room_by_number returns None for an invalid room number """
        room = RoomService.get_room_by_number(429).first()
        self.assertIsNone(room)

    def test_add_resident_to_room(self):
        """ Tests that residents can be added to a room """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        RoomService.add_resident_to_room(test_user.email, self.test_room.number)

        resident = ResidentService.get_resident_by_id(test_user.id).first()
        self.assertEqual(resident.room_number, self.test_room.number)

    def test_invalid_add_resident_to_room(self):
        """ Tests that non-resident users cannot be added to a room """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        test_user = UserService.create_user(*test_user_info)

        RoomService.add_resident_to_room(test_user.email, self.test_room.number)
        resident = ResidentService.get_resident_by_id(test_user.id).first()
        self.assertIsNone(resident)
