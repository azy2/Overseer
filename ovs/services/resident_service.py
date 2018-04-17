"""
DB and utility functions for Residents
"""
from ovs import db
from ovs.models.profile_model import Profile
from ovs.models.resident_model import Resident
from ovs.models.user_model import User
from ovs.utils import genders


class ResidentService:
    """ DB and utility functions for Residents """

    def __init__(self):
        pass

    @staticmethod
    def create_resident(new_user, room_number='None'):
        """
        Adds a resident to the Resident table.

        Args:
            new_user: A User db model.
            room_number: Room number.

        Returns:
            The Resident db model that was just created.
        """
        from ovs.services.profile_service import ProfileService

        new_resident = Resident(new_user.id)
        new_resident.room_number = room_number
        db.session.add(new_resident)
        db.session.flush()

        new_resident_profile = Profile(new_user.id)
        new_resident_profile.preferred_name = new_user.first_name
        new_resident_profile.preferred_email = new_user.email
        new_resident_profile.gender = genders.UNSPECIFIED
        ProfileService.set_default_picture(new_resident_profile.picture_id)
        db.session.add(new_resident_profile)
        db.session.flush()

        return new_resident

    @staticmethod
    def edit_resident(user_id, email, first_name, last_name, room_number):
        """
        Edits an existing resident identified by user_id.

        Args:
            user_id: Unique user id.
            email: New email.
            first_name: New first name.
            last_name: New last name.
            room_number: New room number.
        """
        from ovs.services.user_service import UserService
        from ovs.services.room_service import RoomService
        UserService.edit_user(user_id, email, first_name, last_name)
        RoomService.add_resident_to_room(email, room_number)

    @staticmethod
    def delete_resident(user_id):
        """
        Deletes an existing resident identified by user_id.

        Args:
            user_id: Unique user id.
        """
        from ovs.services.profile_picture_service import ProfilePictureService
        from ovs.services import UserService
        user = UserService.get_user_by_id(user_id)
        resident = ResidentService.get_resident_by_id(user_id)
        picture_id = resident.profile.picture_id
        # The profile gets deleted by cascade
        db.session.delete(user)
        db.session.delete(resident)
        db.session.flush()
        ProfilePictureService.delete_profile_picture(picture_id)

    @staticmethod
    def get_resident_by_email(email):
        """
        Fetch resident identified by email.

        Args:
            email: A email address.

        Returns:
            A Resident db model.
        """
        return Resident.query.join(User, User.id == Resident.user_id).filter(User.email == email).first()

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Fetch resident identified by user id.

        Args:
            user_id: Unique user id.

        Returns:
            A Resident db model.
        """
        return Resident.query.filter_by(user_id=user_id).first()

    @staticmethod
    def resident_exists(user_id):
        """
        Check if resident identified user id exists.

        Args:
            user_id: Unique user id.

        Returns:
            If the residents exists.
        """
        return ResidentService.get_resident_by_id(user_id) is not None

    @staticmethod
    def get_resident_by_pin(pin):
        """
        Fetch resident identified by pin.

        Args:
            pin: Unique meal plan pin.

        Returns:
            A Resident db model.
        """
        return Resident.query.filter_by(mealplan_pin=pin).first()

    @staticmethod
    def set_resident_pin(user_id, new_pin):
        """
        Set a meal pin for a resident identified by user id.

        Args:
            user_id: The resident's unique user id.
            new_pin: The new meal pin to be assigned to the resident.
        """
        Resident.query\
                .filter_by(user_id=user_id)\
                .update({Resident.mealplan_pin: new_pin})
        db.session.flush()

    @staticmethod
    def get_all_residents_users():
        """
        Fetch all related residents and users in db.

        Returns:
            A list of (Resident, User) db model tuples.
        """
        return db.session.query(Resident, User).join(User, Resident.user_id == User.id).all()
