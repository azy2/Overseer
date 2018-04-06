""" Services related to managers """
from sqlalchemy import exc
from sqlalchemy.orm import aliased

from flask import current_app
from ovs.models.package_model import Package
from ovs.models.resident_model import Resident
from ovs.models.user_model import User
from ovs.services.resident_service import ResidentService
from ovs.services.room_service import RoomService

db = current_app.extensions['database'].instance()


class ManagerService:
    """ Services related to managers """

    def __init__(self):
        pass

    @staticmethod
    def get_all_residents():
        """
        Join based on user_id
        :return: Lists of residents, users tuples
        :rtype: [(Resident(...), User(...)), ...]
        """
        return db.query(Resident, User).join(User, Resident.user_id == User.id).all()

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Returns the Resident identified by user_id
        """
        return db.query(Resident).filter(Resident.user_id == user_id).first()

    @staticmethod
    def update_resident_room_number(user_id, room_number):
        """ Changes the room_number of Resident identified by user_id """
        room = RoomService.get_room_by_number(room_number).first()
        if room is None:
            return None
        # Todo: Catch specific exceptions for join and update
        try:
            db.query(Resident).filter(Resident.user_id == user_id).update({Resident.room_number: room_number})
            db.commit()
        except exc.SQLAlchemyError:
            db.rollback()
            return None
        return ResidentService.get_resident_by_id(user_id).first()

    @staticmethod
    def get_all_packages_recipients_checkers():
        """
        Join based on user_id
        :return: Lists of residents, users tuples
        :rtype: [(Resident(...), User(...)), ...]
        """
        user_1 = aliased(User)
        user_2 = aliased(User)
        return db.query(Package, user_1, user_2) \
            .join(user_1, Package.recipient_id == user_1.id) \
            .join(user_2, Package.checked_by_id == user_2.id).all()
