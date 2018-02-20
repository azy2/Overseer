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
        """ Runs before every test and clears the user table """
        self.db = app.database.instance()
        self.tearDown()

    def tearDown(self):
        """ Runs after every tests and clears the user table """
        self.db.query(User).delete()

    def test_create_user(self):
        """ Tests create_user """
        test_user = {'email': 'test@gmail.com', 'first_name': 'Bob',
                     'last_name': 'Ross', 'role': 'ADMIN'}
        UserService.create_user(**test_user)
        user_list = self.db.query(User).filter(User.email == test_user['email']).all()
        self.assertEqual(len(user_list), 1)
        user = user_list[0]
        self.assertEqual((user.email, user.first_name, user.last_name, user.role), tuple(test_user.values()))
        self.assertIsNotNone(user.password)
