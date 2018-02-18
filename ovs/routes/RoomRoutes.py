from flask import Blueprint
from ovs.services import RoomService
rooms_bp = Blueprint('room', __name__,)


@rooms_bp.route('/')
def create_room():
    new_room = RoomService.create_room(112, 'FULL', 'DOUBLE')
    return new_room.json()
