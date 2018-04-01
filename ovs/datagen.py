""" Data generation class """
from ovs import app
from ovs.services import UserService
from ovs.services import RoomService
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
    def create_user(user_role):
        """ Creates a default user if it doesn't exist """
        user = UserService.get_user_by_email(
            app.config[user_role]['email']).one_or_none()
        if not user:
            UserService.create_user(app.config[user_role]['email'],
                                    app.config[user_role]['first_name'],
                                    app.config[user_role]['last_name'],
                                    user_role,
                                    app.config[user_role]['password'])

    @staticmethod
    def create_default_room():
        room = RoomService.get_room_by_number('None').first()
        if room is None:
            RoomService.create_room('None', '', '')

    @staticmethod
    def create_defaults():
        """ Populate the database with defaults """
        DataGen.create_user(roles.ADMIN)
        DataGen.create_default_room()
        if app.config['TESTING'] or app.config['DEVELOPMENT']:
            for user_role in [roles.RESIDENT, roles.RESIDENT_ADVISOR, roles.STAFF,
                              roles.OFFICE_MANAGER, roles.BUILDING_MANAGER]:
                DataGen.create_user(user_role)


    @staticmethod
    def clear_db():
        """ Empty the DB for tests """
        db.query(Profile).delete()
        db.query(User).delete()
        db.query(Resident).delete()
        db.query(Room).delete()
        db.query(MealPlan).delete()
        db.commit()
