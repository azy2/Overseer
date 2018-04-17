"""
Tests for profile services
"""
from ovs.tests.unittests.base_test import OVSBaseTestCase
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.profile_service import ProfileService
from ovs.models.profile_model import Profile
from ovs.utils.genders import Gender
from ovs.datagen import DataGen


class TestProfileService(OVSBaseTestCase):
    """
    Tests for profile services
    """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        DataGen.create_default_room()
        test_user_info = ('test@gmail.com', 'Bob', 'Smith', 'RESIDENT')
        UserService.create_user(*test_user_info)
        self.test_user = UserService.get_user_by_email('test@gmail.com')
        self.test_resident = ResidentService.get_resident_by_id(self.test_user.id)

    def test_update_profile(self):
        """ Tests that profiles can be updated """
        profile = self.test_resident.profile
        self.assertEqual(profile.preferred_name, "Bob")
        self.assertEqual(profile.phone_number, None)
        self.assertEqual(profile.preferred_email, 'test@gmail.com')
        self.assertEqual(profile.race, None)
        self.assertEqual(profile.gender, 'Unspecified')

        ProfileService.update_profile(self.test_user.id,
                                      preferred_name='Jenny',
                                      phone_number='867-5309',
                                      preferred_email='test_new@gmail.com',
                                      race='Black',
                                      gender=Gender.FEMALE)

        self.assertEqual(profile.preferred_name, "Jenny")
        self.assertEqual(profile.phone_number, "867-5309")
        self.assertEqual(profile.preferred_email, 'test_new@gmail.com')
        self.assertEqual(profile.race, 'Black')
        self.assertEqual(profile.gender, Gender.FEMALE)

    def test_delete_profile(self):
        """ Tests that profiles can be deleted """
        expected = self.db.session.query(Profile).count() - 1

        # check if deletion successful
        self.assertTrue(ProfileService.delete_profile(self.test_user.id))

        self.assertEqual(len(ProfileService.get_all_profiles()), expected)

    def test_delete_profile_null(self):
        """ Tests that nothing breaks when deleting a nonexistant profile """
        expected = self.db.session.query(Profile).count()

        # This id is NOT the resident
        self.assertFalse(ProfileService.delete_profile(self.test_user.id + 1))

        self.assertEqual(self.db.session.query(Profile).count(), expected)

    def test_get_all_profiles(self):
        """ Tests that get_all_profiles returns the correct number of profiles """
        expected = self.db.session.query(Profile).count()

        self.assertEqual(len(ProfileService.get_all_profiles()), expected)
