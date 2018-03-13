"""
Tests for profile services
"""
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.profile_service import ProfileService
from ovs.utils.genders import Gender
from ovs.tests.unittests.base_test import OVSBaseTestCase


class TestProfileService(OVSBaseTestCase):
    """
    Tests for profile services
    """

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        test_user_info = ('test@gmail.com', 'Bob', 'Smith', 'RESIDENT')
        UserService.create_user(*test_user_info)
        self.test_user = UserService.get_user_by_email('test@gmail.com').first()
        self.test_resident = ResidentService.get_resident_by_id(self.test_user.id).first()

    def test_update_profile(self):
        """ Tests that profiles can be updated """
        profile = self.test_resident.profile
        self.assertEqual(profile.preferred_name, "Bob")
        self.assertEqual(profile.phone_number, None)
        self.assertEqual(profile.preferred_email, 'test@gmail.com')
        self.assertEqual(profile.race, None)
        self.assertEqual(profile.gender, None)
        self.assertIsNotNone(profile.picture_id)

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
        self.assertIsNotNone(profile.picture_id)
