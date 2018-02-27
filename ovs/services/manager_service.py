""" Services related to managers """
from ovs import app
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
from ovs.services.resident_service import ResidentService
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
    def update_resident_room_number(user_id, room_number):
        """ Changes the room_number of Resident identified by user_id """
        db.query(Resident).filter(Resident.user_id == user_id).update({Resident.room_number: room_number})
        db.commit()
        return ResidentService.get_resident_by_id(user_id).first()
