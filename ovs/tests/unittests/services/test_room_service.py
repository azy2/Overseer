"""
Tests for room services
"""
from ovs.models.room_model import Room
from ovs.services.room_service import RoomService
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.tests.unittests.base_test import OVSBaseTestCase

from ovs.datagen import DataGen


class TestRoomService(OVSBaseTestCase):
    """
    Tests for room services
    """
    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        DataGen.create_default_room()
        self.create_test_room()

    def create_test_room(self):
        """ Creates a room for use in testing  """

        self.test_room_info = ('5', 'Good', 'Single')
        self.test_room = RoomService.create_room(*self.test_room_info)

    def test_create_room(self):
        """ Tests that rooms can be created """
        room = self.db.session.query(Room).filter(Room.id == self.test_room.id).first()
        self.assertEqual((room.number, room.status, room.type), self.test_room_info)

    def test_get_room_by_id(self):
        """ Tests that get_room_by_id returns the correct room """
        room = RoomService.get_room_by_id(self.test_room.id)
        self.assertEqual((room.number, room.status, room.type), self.test_room_info)

    def test_invalid_get_room_by_id(self):
        """ Tests that get_room_by_id returns None for an invalid room id """
        room = RoomService.get_room_by_id(5)
        self.assertIsNone(room)

    def test_get_room_by_number(self):
        """ Tests that get_room_by_number returns the correct room """
        room = RoomService.get_room_by_number(self.test_room.number)
        self.assertEqual((room.number, room.status, room.type), self.test_room_info)

    def test_invalid_get_room_by_number(self):
        """ Tests that get_room_by_number returns None for an invalid room number """
        room = RoomService.get_room_by_number('429')
        self.assertIsNone(room)

    def test_add_resident_to_room(self):
        """ Tests that residents can be added to a room """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        test_user = UserService.create_user(*test_user_info)
        resident = ResidentService.get_resident_by_id(test_user.id)
        old_room = RoomService.get_room_by_number('None')

        self.assertTrue(resident in old_room.occupants)
        RoomService.add_resident_to_room(test_user.email, self.test_room.number)

        self.assertEqual(resident.room_number, self.test_room.number)
        self.assertTrue(resident in self.test_room.occupants)
        self.assertFalse(resident in old_room.occupants)

    def test_invalid_add_resident_to_room(self):
        """ Tests that non-resident users cannot be added to a room """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        test_user = UserService.create_user(*test_user_info)

        RoomService.add_resident_to_room(test_user.email, self.test_room.number)

        resident = ResidentService.get_resident_by_id(test_user.id)

        self.assertIsNone(resident)
        self.assertFalse(resident in self.test_room.occupants)

    def test_get_all_rooms(self):
        """ Tests getting all rooms with 2 entries """
        self.assertEqual(len(RoomService.get_all_rooms()), 2)

    def test_get_all_rooms_multiple(self):
        """ Tests getting all rooms with 3 entries"""
        RoomService.create_room('6', 'Bad', 'Double')
        self.assertEqual(len(RoomService.get_all_rooms()), 3)

    def test_delete_room(self):
        """ Tests that rooms can be deleted """
        expected = self.db.session.query(Room).count() - 1

        # check if deletion successful
        self.assertTrue(RoomService.delete_room(self.test_room.id))

        self.assertEqual(self.db.session.query(Room).count(), expected)

    def test_delete_room_invalid(self):
        """ Tests that a nonexistant room cannot be deleted """
        expected = self.db.session.query(Room).count()

        # check if deletion successful
        self.assertTrue(RoomService.delete_room(self.test_room.id + 1))

        self.assertEqual(self.db.session.query(Room).count(), expected)

    def test_edit_room(self):
        """ Tests that rooms can be edited"""
        self.assertTrue(RoomService.edit_room(
            self.test_room.id, '6', 'Bad', 'Double'))
        self.assertEqual((self.test_room.number, self.test_room.status, self.test_room.type),
                         self.test_room_info)

    def test_edit_room_invalid(self):
        self.assertFalse(RoomService.edit_room(
            self.test_room.id+3, '6', 'Bad', 'Double'))
        self.assertIsNone(RoomService.get_room_by_number('6'))
