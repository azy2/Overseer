"""
Tests for profile services
"""
from unittest import TestCase
from ovs import app
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.profile_service import ProfileService
from ovs.models.user_model import User
from ovs.utils.genders import Gender


class TestProfileService(TestCase):
    """
    Tests for profile services
    """
    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        self.tearDown()
        test_user_info = ('test@gmail.com', 'Bob', 'Smith', 'RESIDENT')
        UserService.create_user(*test_user_info)
        self.test_user = UserService.get_user_by_email('test@gmail.com').first()
        self.test_resident = ResidentService.get_resident_by_id(self.test_user.id).first()

    def tearDown(self):
        """ Runs after every tests and clears relevant tables """
        self.db.query(User).delete()
        self.db.commit()

    def test_update_profile(self):
        """ Tests update_profile """
        profile = self.test_resident.profile
        self.assertEqual(profile.preferred_name, "Bob")
        self.assertEqual(profile.phone_number, None)
        self.assertEqual(profile.preferred_email, 'test@gmail.com')
        self.assertEqual(profile.race, None)
        self.assertEqual(profile.gender, None)
        self.assertEqual(profile.picture_path, None)

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
        self.assertEqual(profile.picture_path, None)
