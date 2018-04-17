""" Data generation class """
from flask import current_app

from ovs import db
from ovs.services import RoomService, UserService
from ovs.utils import roles


class DataGen:
    """ Data generation class """
    @staticmethod
    def create_user(user_role):
        """
        Creates a default user if it doesn't exist.

        Args:
            user_role: The role of the default user to create.
                       current_app.config['USERS'][user_role] must exist.
        """
        default_user = current_app.config['USERS'][user_role]
        user = UserService.get_user_by_email(default_user['email'])
        if not user:
            UserService.create_user(default_user['email'],
                                    default_user['first_name'],
                                    default_user['last_name'],
                                    user_role,
                                    default_user['password'])

    @staticmethod
    def create_default_room():
        """ Creates default room if it doesn't exist """
        room = RoomService.get_room_by_number('None')
        if room is None:
            RoomService.create_room('None', '', '')

    @staticmethod
    def create_defaults():
        """ Populate the database with defaults """
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
        import ovs.models  # pylint: disable=unused-variable
        db.drop_all()
        db.create_all()
        db.session.commit()
