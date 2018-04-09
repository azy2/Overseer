""" Data generation class """
from flask import current_app

from ovs import db
from ovs.services import UserService
from ovs.services import RoomService
from ovs.utils import roles

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

        if user is not None:
            current_app.config['DEFAULT_IDS'].add(user.id)

    @staticmethod
    def create_default_room():
        """ Creates default room if it doesn't exist """
        room = RoomService.get_room_by_number('None').first()
        if room is None:
            RoomService.create_room('None', '', '')

    @staticmethod
    def create_defaults():
        """ Populate the database with defaults """
        current_app.config['DEFAULT_IDS'] = set()
        DataGen.create_user(roles.ADMIN)
        DataGen.create_default_room()
        if current_app.config['TESTING'] or current_app.config['DEVELOPMENT']:
            for user_role in [roles.RESIDENT, roles.RESIDENT_ADVISOR, roles.STAFF,
                              roles.OFFICE_MANAGER, roles.BUILDING_MANAGER]:
                DataGen.create_user(user_role)
        db.session.commit()


    @staticmethod
    def clear_db():
        """ Empty the DB for tests """
        import ovs.models # pylint: disable=unused-variable
        db.drop_all()
        db.create_all()
