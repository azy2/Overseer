"""
Tests for resident services
"""
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.profile_model import Profile
from ovs.tests.unittests.base_test import OVSBaseTestCase

class TestResidentService(OVSBaseTestCase):
    """
    Tests for resident services
    """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        self.create_test_resident()

    def get_tables_used_in_tests(self):
        """
        Subclass test cases should override this to return what database objects
        correspond to tables they will need cleared before running
        """
        return [Profile, User, Resident, Room]

    def create_test_resident(self):
        """ Creates a test resident for use in testing """
        self.test_resident_info = ('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        self.test_resident = UserService.create_user(*self.test_resident_info)

    def test_create_resident(self):
        """ Tests that residents can be created """
        resident = self.db.query(Resident).filter(Resident.user_id == self.test_resident.id).first()
        self.assertIsNotNone(resident)

    def test_create_resident_null(self):
        """ Tests that non-resident user accounts cannot be found in Resident database """
        test_user_info = ('test2@gmail.com', 'Bob', 'Ross', 'ADMIN')
        user = UserService.create_user(*test_user_info)
        resident = self.db.query(Resident).filter(Resident.user_id == user.id).first()
        self.assertIsNone(resident)

    def test_get_resident_by_id(self):
        """ Tests that get_resident_by_id successfully finds a resident """
        resident = ResidentService.get_resident_by_id(self.test_resident.id).first()
        self.assertIsNotNone(resident)
        self.assertEqual(resident.user_id, self.test_resident.id)

    def test_invalid_get_resident_by_id(self):
        """ Tests that get_resident_by_id does not find a resident with a non-existent id """
        resident = ResidentService.get_resident_by_id(4).first()
        self.assertIsNone(resident)
