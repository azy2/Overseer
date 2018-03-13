""" Data generation class """
from ovs import app
from ovs.services import UserService
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.profile_model import Profile
from ovs.models.meal_plan_model import MealPlan
from ovs.utils import roles

db = app.database.instance()
class DataGen:
    """ Data generation class """
    @staticmethod
    def create_superuser():
        """ Add the superuser to the database """
        UserService.create_user(app.config['SUPERUSER']['email'],
                                app.config['SUPERUSER']['first_name'],
                                app.config['SUPERUSER']['last_name'],
                                roles.ADMIN,
                                app.config['SUPERUSER']['password'])

    @staticmethod
    def create_default_resident():
        """ Add the default resident to the database """
        UserService.create_user(app.config['RESIDENT']['email'],
                                app.config['RESIDENT']['first_name'],
                                app.config['RESIDENT']['last_name'],
                                roles.RESIDENT,
                                app.config['RESIDENT']['password'])

    @staticmethod
    def create_defaults():
        """ Populate the database with defaults """
        super_user = UserService.get_user_by_email(
            app.config['SUPERUSER']['email']).one_or_none()
        if not super_user:
            DataGen.create_superuser()

        default_resident = UserService.get_user_by_email(
            app.config['RESIDENT']['email']).one_or_none()
        if not default_resident:
            DataGen.create_default_resident()

    @staticmethod
    def clear_db():
        """ Empty the DB for tests """
        db.query(Profile).delete()
        db.query(User).delete()
        db.query(Resident).delete()
        db.query(Room).delete()
        db.query(MealPlan).delete()
        db.commit()
