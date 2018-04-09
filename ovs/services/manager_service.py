""" Services related to managers """
from sqlalchemy.orm import aliased

from ovs import db
from ovs.models.package_model import Package
from ovs.models.resident_model import Resident
from ovs.models.user_model import User


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
        return db.session.query(Resident, User).join(User, Resident.user_id == User.id).all()

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Returns the Resident identified by user_id
        """
        return db.session.query(Resident).filter(Resident.user_id == user_id).first()

    @staticmethod
    def get_all_packages_recipients_checkers():
        """
        Join based on user_id
        :return: Lists of residents, users tuples
        :rtype: [(Resident(...), User(...)), ...]
        """
        user_1 = aliased(User)
        user_2 = aliased(User)
        return db.session.query(Package, user_1, user_2) \
            .join(user_1, Package.recipient_id == user_1.id) \
            .join(user_2, Package.checked_by_id == user_2.id).all()
