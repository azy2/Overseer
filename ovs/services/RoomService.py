from ovs import app
from ovs.models.RoomModel import Room
from ovs.models.ResidentModel import Resident
from ovs.services import UserService
db = app.database.instance()

class RoomService:
    @staticmethod
    def create_room(number, status, type):
        new_room = Room(number=number, status=status, type=type)
        db.add(new_room)
        db.commit()
        return new_room

    @staticmethod
    def get_room_by_id(id):
        return db.query(Room).filter(Room.id == id)

    @staticmethod
    def get_room_by_number(number):
        return db.query(Room).filter(Room.number == number)

    @staticmethod
    def add_resident_to_room(email, number):
        # TODO: change below code to pull from residents table once it is
        # implemented to mirror the users table automatically

        user = UserService.get_user_by_email(email).first()

        new_resident = Resident(user_id=user.id, room_number=number)
        db.add(new_resident)
        db.commit()
        return new_resident
