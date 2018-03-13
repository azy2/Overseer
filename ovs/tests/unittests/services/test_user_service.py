"""
Tests for user services
"""
from ovs.services.user_service import UserService
from ovs.models.user_model import User
from ovs.tests.unittests.base_test import OVSBaseTestCase

class TestUserService(OVSBaseTestCase):
    """
    Tests for user services
    """
    def get_tables_used_in_tests(self):
        """
        Subclass test cases should override this to return what database objects
        correspond to tables they will need cleared before running
        """
        return [User]

    def test_create_user(self):
        """ Tests that users can be created """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        UserService.create_user(*test_user_info)

        user_list = self.db.query(User).filter(User.email == test_user_info[0]).all()
        self.assertEqual(len(user_list), 1)

        user = user_list[0]
        self.assertEqual((user.email, user.first_name, user.last_name, user.role), test_user_info)
        self.assertIsNotNone(user.password)

    def test_get_user_by_email(self):
        """ Tests get_user_by_email successfully finds a user """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        UserService.create_user(*test_user_info)

        user_list = UserService.get_user_by_email(test_user_info[0]).all()
        self.assertEqual(len(user_list), 1)

        user = user_list[0]
        self.assertEqual((user.email, user.first_name, user.last_name, user.role), test_user_info)
        self.assertIsNotNone(user.password)

    def test_invalid_get_user_by_email(self):
        """ Tests get_user_by_email does not find anyone with an invalid email """
        user_list = UserService.get_user_by_email("dummy@gmail.com").all()
        self.assertEqual(len(user_list), 0)
