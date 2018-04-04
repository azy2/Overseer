"""
Tests for resident services
"""
from ovs import app
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.room_service import RoomService
from ovs.models.resident_model import Resident
from ovs.tests.unittests.base_test import OVSBaseTestCase

db = app.database.instance()

class TestResidentService(OVSBaseTestCase):
    """
    Tests for resident services
    """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        self.create_test_resident()

    def create_test_resident(self):
        """ Creates a test resident for use in testing """
        self.test_resident_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        self.test_admin_info = ('test2@gmail.com', 'Bob', 'Ross', 'ADMIN')
        self.test_user = UserService.create_user(*self.test_resident_info)
        self.test_resident = ResidentService.get_resident_by_id(self.test_user.id).first()
        self.test_room = RoomService.create_room('1', 'Good', 'Single')

    def test_create_resident(self):
        """ Tests that residents can be created """
        resident = self.db.query(Resident).filter(Resident.user_id == self.test_user.id).first()
        self.assertIsNotNone(resident)

    def test_create_resident_null(self):
        """ Tests that non-resident user accounts cannot be found in Resident database """
        user = UserService.create_user(*self.test_admin_info)
        resident = self.db.query(Resident).filter(Resident.user_id == user.id).first()
        self.assertIsNone(resident)

    def test_get_resident_by_id(self):
        """ Tests that get_resident_by_id successfully finds a resident """
        resident = ResidentService.get_resident_by_id(self.test_user.id).first()
        self.assertIsNotNone(resident)
        self.assertEqual(resident.user_id, self.test_user.id)

    def test_invalid_get_resident_by_id(self):
        """ Tests that get_resident_by_id does not find a resident with a non-existent id """
        resident = ResidentService.get_resident_by_id(4).first()
        self.assertIsNone(resident)

    def test_update_resident_room_number(self):
        """ Tests that a resident's room number can be updated """
        ResidentService.update_resident_room_number(self.test_user.id, '1')
        self.assertEqual(self.test_resident.room_number, '1')

    def test_edit_resident(self): # cases - invalid email/id, invalid room, success
        """ Tests that a resident can be edited"""
        self.assertTrue(ResidentService.edit_resident(self.test_user.id, 'test2@gmail.com', 'Joe', 'Smith', '1'))
        self.assertEqual(self.test_user.email, 'test2@gmail.com') #further confirmation in test_edit_user
        self.assertEqual(self.test_resident.room_number, '1') #check that update_resident_room_number got called

    def test_edit_resident_bad_room(self):
        """ Tests that a bad room number will be rejected """
        self.assertFalse(ResidentService.edit_resident(self.test_user.id, 'test2@gmail.com', 'Joe', 'Smith', '2'))
        self.assertEqual(self.test_resident.room_number, 'None')

    def test_edit_resident_bad_email(self): # cases - invalid email/id, invalid room, success
        """ Tests that a duplicate email will cancel everything """
        UserService.create_user(*self.test_admin_info)
        self.assertFalse(ResidentService.edit_resident(self.test_user.id, 'test2@gmail.com', 'Joe', 'Smith', '1'))
        self.assertEqual(self.test_user.email, 'test@gmail.com') #User is not updated
        self.assertEqual(self.test_resident.room_number, 'None') #Room number is not updated

    def test_delete_resident(self):
        """ Tests that profiles can be deleted """
        expected = db.query(Resident).count()-1
        self.assertTrue(ResidentService.delete_resident(self.test_user.id)) #method returns success
        self.assertEqual(db.query(Resident).count(), expected)

    def test_delete_resident_null(self):
        """ Tests that nothing breaks when deleting a nonexistant resident """
        expected = db.query(Resident).count()
        self.assertFalse(ResidentService.delete_resident(self.test_user.id + 3)) #This random id is NOT the resident
        self.assertEqual(db.query(Resident).count(), expected)
