
from ovs import app
from ovs.models.user_model import User
from ovs.models.resident_model import Resident
db = app.database.instance()


class ManagerService:

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
        return db.query(Resident).filter(Resident.user_id == user_id).first()

    @staticmethod
    def update_resident_room_number(user_id, room_number):
        resident = ManagerService.get_resident_by_id(user_id)
        resident.room_number = room_number
        db.commit()
        return resident

    # TODO get a resident by email, etc...
