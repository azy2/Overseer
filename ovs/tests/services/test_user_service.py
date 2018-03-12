"""
Tests for user services
"""
from unittest import TestCase
from ovs import app
from ovs.services.user_service import UserService
from ovs.models.user_model import User


class TestUserService(TestCase):
    """
    Tests for user services
    """
    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        self.tearDown()

    def tearDown(self):
        """ Runs after every tests and clears relevant tables """
        self.db.query(User).delete()
        self.db.commit()

    def test_create_user(self):
        """ Tests create_user """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        UserService.create_user(*test_user_info)
        user_list = self.db.query(User).filter(User.email == test_user_info[0]).all()
        self.assertEqual(len(user_list), 1)
        user = user_list[0]
        self.assertEqual((user.email, user.first_name,
                          user.last_name, user.role), test_user_info)
        self.assertIsNotNone(user.password)

    def test_get_user_by_email(self):
        """ Tests get_user_by_email """
        test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        UserService.create_user(*test_user_info)
        user_list = UserService.get_user_by_email(test_user_info[0]).all()
        self.assertEqual(len(user_list), 1)
        user = user_list[0]
        self.assertEqual((user.email, user.first_name,
                          user.last_name, user.role), test_user_info)
        self.assertIsNotNone(user.password)

    def test_get_user_by_email_0(self):
        """ Tests get_user_by_email with bad parameter"""
        user_list = UserService.get_user_by_email("dummy@gmail.com").all()
        self.assertEqual(len(user_list), 0)
