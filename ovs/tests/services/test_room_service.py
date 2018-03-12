"""
Tests for room services
"""
from unittest import TestCase

from ovs import app
from ovs.models.profile_model import Profile
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.user_model import User
from ovs.services.resident_service import ResidentService
from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService


class TestRoomService(TestCase):
    """
    Tests for room services
    """

    @classmethod
    def setUpClass(cls):
        """ Sets the app config to TESTING mode """
        app.config['TESTING'] = True

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

    def test_create_room(self):
        """ Tests create_room """
        test_room_info = ('5', 'Good', 'Single')
        orig_room = RoomService.create_room(*test_room_info)
        room = self.db.query(Room).filter(Room.id == orig_room.id).first()
        self.assertEqual((room.number, room.status,
                          room.type), test_room_info)

    def test_get_room_by_id(self):
        """ Tests get_room_by_id """
        test_room_info = ('5', 'Good', 'Single')
        orig_room = RoomService.create_room(*test_room_info)
        room = RoomService.get_room_by_id(orig_room.id).first()
        self.assertEqual((room.number, room.status,
                          room.type), test_room_info)

    def test_get_room_by_id_null(self):
        """ Tests get_room_by_id """
        room = RoomService.get_room_by_id(5).first()
        self.assertIsNone(room)

    def test_get_room_by_number(self):
        """ Tests get_room_by_number """
        test_room_info = ('5', 'Good', 'Single')
        RoomService.create_room(*test_room_info)
        room = RoomService.get_room_by_number(test_room_info[0]).first()
        self.assertEqual((room.number, room.status,
                          room.type), test_room_info)

    def test_get_room_by_number_null(self):
        """ Tests get_room_by_number """
        room = RoomService.get_room_by_number(5).first()
        self.assertIsNone(room)

    def test_add_resident_to_room(self):
        """ Tests add_resident_to_room """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        test_room_info = ('5', 'Good', 'Single')
        RoomService.create_room(*test_room_info)
        RoomService.add_resident_to_room(test_user_info[0], test_room_info[0])
        resident = ResidentService.get_resident_by_id(test_user.id).first()
        self.assertEqual(resident.room_number, test_room_info[0])

    def test_add_resident_to_room_fail(self):
        """ Tests add_resident_to_room """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        test_user = UserService.create_user(*test_user_info)
        test_room_info = ('5', 'Good', 'Single')
        RoomService.create_room(*test_room_info)
        RoomService.add_resident_to_room(test_user_info[0], test_room_info[0])
        resident = ResidentService.get_resident_by_id(test_user.id).first()
        self.assertIsNone(resident)
