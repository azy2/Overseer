""" Tests for package services """
from datetime import datetime
from unittest import TestCase

from ovs import app
from ovs.models.package_model import Package
from ovs.models.profile_model import Profile
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.user_model import User
from ovs.services.user_service import UserService
from ovs.services.package_service import PackageService
class TestPackageServce(TestCase):
    """ Tests for package services"""

    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        self.tearDown()

    def tearDown(self):
        """ Runs after every tests and clears relevant tables """
        self.db.query(Profile).delete()
        self.db.query(User).delete()
        self.db.query(Resident).delete()
        self.db.query(Room).delete()
        self.db.commit()

    def test_update_package(self):
        """ Tests update_package """
        # update_package(package_id, recipient_email, description)
        user_1 = UserService.create_user('test@gmail.com', 'Bob', 'Ross', 'RESIDENT')
        user_2 = UserService.create_user('test2@gmail.com', 'Joe', 'Smith', 'RESIDENT')
        user_3 = UserService.create_user('test3@gmail.com', 'Jim', 'White', 'ADMIN')
        checked_at = datetime.now().replace(second=0, microsecond=0)
        package_description = "Fragile"
        package_1 = PackageService.create_package(user_1.id, user_3.id, checked_at, package_description)
        new_package_description = "NOT Fragile"
        PackageService.update_package(package_1.id, user_2.email, new_package_description)
        updated_package_1 = self.db.query(Package).filter(Package.id == package_1.id).first()

        self.assertEqual(updated_package_1.recipient_id, user_2.id)
        self.assertEqual(updated_package_1.description, new_package_description)
