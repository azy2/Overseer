"""
Tests for user services
"""
from ovs import app
from ovs.services.user_service import UserService
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.tests.unittests.base_test import OVSBaseTestCase

db = app.database.instance()

class TestUserService(OVSBaseTestCase):
    """
    Tests for user services
    """
    def setUp(self):
        """ Runs before every test and clears relevant tables """
        super().setUp()
        self.create_test_user()

    def create_test_user(self):
        """ Creates a test user """
        self.test_user_info = ('test@gmail.com', 'Bob', 'Ross', 'ADMIN')
        self.test_user = UserService.create_user(*self.test_user_info)

    def test_create_user(self):
        """ Tests that users can be created """
        user_list = self.db.query(User).filter(User.email == self.test_user_info[0]).all()
        self.assertEqual(len(user_list), 1)

        user = user_list[0]
        self.assertEqual((user.email, user.first_name, user.last_name, user.role), self.test_user_info)
        self.assertIsNotNone(user.password)

    def test_get_user_by_email(self):
        """ Tests get_user_by_email successfully finds a user """
        user_list = UserService.get_user_by_email(self.test_user_info[0]).all()
        self.assertEqual(len(user_list), 1)

        user = user_list[0]
        self.assertEqual((user.email, user.first_name, user.last_name, user.role), self.test_user_info)
        self.assertIsNotNone(user.password)

    def test_invalid_get_user_by_email(self):
        """ Tests get_user_by_email does not find anyone with an invalid email """
        user = UserService.get_user_by_email("dummy@gmail.com").first()
        self.assertIsNone(user)

    def test_edit_user(self): #cases : bad user, overwrite, same email, normal
        """ Tests editing a user when everything works"""
        self.assertTrue(UserService.edit_user(self.test_user.id, 'test2@gmail.com', 'John', 'Smith'))
        self.assertEqual(self.test_user.email, 'test2@gmail.com')
        self.assertEqual(self.test_user.first_name, 'John')
        self.assertEqual(self.test_user.last_name, 'Smith')

    def test_user_same_email(self):
        """ Tests editing a user when everything works. Duplicate email is okay, since it is the one! """
        self.assertTrue(UserService.edit_user(self.test_user.id, 'test@gmail.com', 'John', 'Smith'))
        self.assertEqual(self.test_user.email, 'test@gmail.com')
        self.assertEqual(self.test_user.first_name, 'John')
        self.assertEqual(self.test_user.last_name, 'Smith')

    def test_edit_user_bad_id(self):
        """ Tests editing a nonexistant user"""
        self.assertFalse(UserService.edit_user(self.test_user.id+3, 'test2@gmail.com', 'John', 'Smith')) #random id
        self.assertIsNone(UserService.get_user_by_email('test2@gmail.com').first())

    def test_edit_user_duplicate_email(self):
        """ Tests edit resident to an existing email """
        UserService.create_user('test2@gmail.com', '', '', 'ADMIN')
        self.assertFalse(UserService.edit_user(self.test_user.id, 'test2@gmail.com', 'John', 'Smith'))
        self.assertEqual(self.test_user.email, self.test_user_info[0])
        self.assertEqual(self.test_user.first_name, self.test_user_info[1])
        self.assertEqual(self.test_user.last_name, self.test_user_info[2])

    def test_delete_user(self):
        """ Tests that a user can be deleted """
        expected = db.query(User).count()-1
        self.assertTrue(UserService.delete_user(self.test_user.id)) #deletion successful
        self.assertEqual(db.query(User).count(), expected)

    def test_delete_user_null(self):
        """ Tests that nothing breaks when deleting a nonexistant resident """
        expected = db.query(User).count()
        self.assertFalse(UserService.delete_user(self.test_user.id + 3)) #This random id is NOT the resident
        self.assertEqual(db.query(User).count(), expected)

    def test_delete_user_resident(self):
        """ Tests that deleting a user deletes their resident info """
        resident = UserService.create_user('test2@gmail.com', 'John', 'Smith', 'RESIDENT')
        expected_user = db.query(User).count() - 1
        expected_resident = db.query(Resident).count()-1
        self.assertTrue(UserService.delete_user(resident.id))
        self.assertEqual(db.query(User).count(), expected_user)
        self.assertEqual(db.query(Resident).count(), expected_resident)
