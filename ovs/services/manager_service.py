""" Services related to managers """
from sqlalchemy.orm import aliased
from ovs import app
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.models.package_model import Package
from ovs.services.user_service import UserService
from ovs.services.resident_service import ResidentService
from ovs.services.package_service import PackageService
db = app.database.instance()


class ManagerService:
    """ Services related to managers """

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
        db.query(Resident).filter(Resident.user_id == user_id).update({Resident.room_number: room_number})
        db.commit()
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

    @staticmethod
    def update_package(package_id, recipient_email, description):
        """ Changes the receiver and description of Package identified by package_id """
        recipient_id = UserService.get_user_by_email(recipient_email).first().id
        db.query(Package) \
          .filter(Package.id == package_id) \
          .update({Package.recipient_id: recipient_id, Package.description: description})
        db.commit()
        return PackageService.get_package_by_id(package_id).first()
