""" Data generation class """
from flask import current_app

from ovs.services import UserService
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.room_model import Room
from ovs.models.profile_model import Profile
from ovs.models.meal_plan_model import MealPlan
from ovs.utils import roles

db = current_app.extensions['database'].instance()
class DataGen:
    """ Data generation class """
    @staticmethod
    def create_user(user_role):
        """ Creates a default user if it doesn't exist """
        user = UserService.get_user_by_email(
            current_app.config[user_role]['email']).one_or_none()
        if not user:
            user = UserService.create_user(current_app.config[user_role]['email'],
                                           current_app.config[user_role]['first_name'],
                                           current_app.config[user_role]['last_name'],
                                           user_role,
                                           current_app.config[user_role]['password'])

        current_app.config['DEFAULT_IDS'].add(user.id)

    @staticmethod
    def create_defaults():
        """ Populate the database with defaults """
        current_app.config['DEFAULT_IDS'] = set()
        DataGen.create_user(roles.ADMIN)
        if current_app.config['TESTING'] or current_app.config['DEVELOPMENT']:
            for user_role in [roles.RESIDENT, roles.RESIDENT_ADVISOR, roles.STAFF,
                              roles.OFFICE_MANAGER, roles.BUILDING_MANAGER]:
                DataGen.create_user(user_role)
        db.commit()

    @staticmethod
    def clear_db():
        """ Empty the DB for tests """
        db.query(Profile).delete()
        db.query(User).delete()
        db.query(Resident).delete()
        db.query(Room).delete()
        db.query(MealPlan).delete()
        db.commit()

    @staticmethod
    def clear_db_except_defaults():
        """ Empty the DB except for the default users """
        db.query(Profile).filter(Profile.user_id not in current_app.config['DEFAULT_IDS']).delete()
        db.query(User).filter(User.id not in current_app.config['DEFAULT_IDS']).delete()
        db.query(Resident).filter(Resident.user_id not in current_app.config['DEFAULT_IDS']).delete()
        db.query(Room).delete()
        db.query(MealPlan).delete()
