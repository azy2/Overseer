"""
Tests for resident services
"""
from ovs.tests.unittests.base_test import OVSBaseTestCase
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.room_service import RoomService
from ovs.services.manager_service import ManagerService
from ovs.models.resident_model import Resident


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
        self.test_admin = UserService.create_user(*self.test_admin_info)
        self.test_resident = ResidentService.get_resident_by_id(self.test_user.id)
        self.test_room = RoomService.create_room('1', 'Good', 'Single')

    def test_create_resident(self):
        """ Tests that residents can be created """
        resident = self.db.session.query(Resident).filter(
            Resident.user_id == self.test_user.id).first()
        self.assertIsNotNone(resident)

    def test_create_resident_null(self):
        """ Tests that non-resident user accounts cannot be found in Resident database """
        resident = self.db.session.query(Resident).filter(
            Resident.user_id == self.test_admin.id).first()
        self.assertIsNone(resident)

    def test_get_resident_by_id(self):
        """ Tests that get_resident_by_id successfully finds a resident """
        self.assertIsNotNone(self.test_resident)
        self.assertEqual(self.test_resident.user_id, self.test_user.id)

    def test_invalid_get_resident_by_id(self):
        """ Tests that get_resident_by_id does not find a resident with a non-existent id """
        resident = ResidentService.get_resident_by_id(4)
        self.assertIsNone(resident)

    def test_get_resident_by_email(self):
        """ Tests that get_resident_by_email successfully finds a resident """
        resident = ResidentService.get_resident_by_email(self.test_resident_info[0])
        self.assertIsNotNone(resident)

    def test_get_resident_by_email_invalid(self):
        """ Tests that get_resident_by_email returns none if an invalid email is provided """
        resident = ResidentService.get_resident_by_email('invalid@invalid.com')
        self.assertIsNone(resident)

    def test_update_resident_room_number(self):
        """ Tests that a resident's room number can be updated """
        ResidentService.update_resident_room_number(self.test_user.id, '1')
        self.assertEqual(self.test_resident.room_number, '1')

    def test_edit_resident(self):  # cases - invalid email/id, invalid room, success
        """ Tests that a resident can be edited"""
        self.assertTrue(ResidentService.edit_resident(
            self.test_user.id, 'test_edit@gmail.com', 'Joe', 'Smith', '1'))

        # further confirmation in test_edit_user
        self.assertEqual(self.test_user.email, 'test_edit@gmail.com')
        # check that update_resident_room_number got called
        self.assertEqual(self.test_resident.room_number, '1')

    def test_edit_resident_bad_room(self):
        """ Tests that a bad room number will be rejected """
        self.assertFalse(ResidentService.edit_resident(
            self.test_user.id, 'test_edit@gmail.com', 'Joe', 'Smith', '2'))
        self.assertEqual(self.test_resident.room_number, 'None')

    # cases - invalid email/id, invalid room, success
    def test_edit_resident_bad_email(self):
        """ Tests that a duplicate email will cancel everything """
        self.assertFalse(ResidentService.edit_resident(
            self.test_user.id, 'test2@gmail.com', 'Joe', 'Smith', '1'))

        # Check user is not updated
        self.assertEqual(self.test_user.email, 'test@gmail.com')
        # Check room number is not updated
        self.assertEqual(self.test_resident.room_number, 'None')

    def test_delete_resident(self):
        """ Tests that profiles can be deleted """
        expected = self.db.session.query(Resident).count() - 1

        # check if deletion successful
        self.assertTrue(ResidentService.delete_resident(self.test_user.id))

        self.assertEqual(len(ManagerService.get_all_residents_users()), expected)

    def test_delete_resident_null(self):
        """ Tests that nothing breaks when deleting a nonexistant resident """
        expected = self.db.session.query(Resident).count()

        # This id is NOT the resident
        self.assertFalse(
            ResidentService.delete_resident(self.test_user.id + 1))

        self.assertEqual(self.db.session.query(Resident).count(), expected)
