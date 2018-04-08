"""
DB and utility functions for Residents
"""
from sqlalchemy import exc

from flask import current_app

from ovs.models.user_model import User
from ovs.models.profile_model import Profile
from ovs.models.resident_model import Resident
from ovs.services.profile_picture_service import ProfilePictureService
from ovs.services.meal_service import MealService
from ovs.utils import genders


db = current_app.extensions['database'].instance()

class ResidentService:
    """ DB and utility functions for Residents """

    def __init__(self):
        pass

    @staticmethod
    def create_resident(new_user, room_number='None'):
        """
        Adds a User to the Resident table
        """
        new_resident = Resident(new_user.id, room_number)
        new_resident_profile = Profile(new_user.id)
        new_resident_profile.preferred_name = new_user.first_name
        new_resident_profile.preferred_email = new_user.email
        new_resident_profile.gender = genders.UNSPECIFIED
        ResidentService.set_default_picture(new_resident_profile.picture_id)

        db.add(new_resident)
        db.add(new_resident_profile)
        db.commit()

        return new_resident

    @staticmethod
    def edit_resident(user_id, email, first_name, last_name, room_number):
        """
        Edits an existing resident
        """
        from ovs.services.user_service import UserService
        success = UserService.edit_user(user_id, email, first_name, last_name)
        if success:
            success = ResidentService.update_resident_room_number(user_id, room_number) is not None
        return success

    @staticmethod
    def delete_resident(user_id):
        """
        Deletes an existing resident
        """
        from ovs.services.profile_service import ProfileService
        resident = ResidentService.get_resident_by_id(user_id).first()
        if resident is None:
            return False
        success = ProfileService.delete_profile(user_id)
        if success:
            db.delete(resident)
        return success


    @staticmethod
    def set_default_picture(picture_id):
        """
        Sets default picture for new residents
        """
        default_picture_path = current_app.config['BLOB']['default_picture_path']
        with open(default_picture_path, 'rb') as default_image:
            file_contents = default_image.read()
            file_bytes = bytearray(file_contents)
        ProfilePictureService.create_profile_picture(picture_id, file_bytes)

    @staticmethod
    def get_resident_by_email(email):
        """
        Gets a user by their email
        :param email: The email of the user
        :return: The db entry of that user
        """
        user_resident = db.query(User, Resident).join(Resident, User.id == Resident.user_id).filter(User.email == email)
        if user_resident is None:
            return None
        return user_resident.first()[1]

    @staticmethod
    def get_resident_by_id(user_id):
        """
        Returns the resident given by user_id
        """
        return db.query(Resident).filter(Resident.user_id == user_id)

    @staticmethod
    def update_resident_room_number(user_id, room_number):
        """ Changes the room_number of Resident identified by user_id """
        from ovs.services.room_service import RoomService
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
    def get_resident_by_pin(pin):
        """
        Returns the resident given pin
        """
        return db.query(Resident).filter(Resident.mealplan_pin == pin).first()

    @staticmethod
    def set_resident_pin(user_id, new_pin):
        """
        Returns the resident given by user_id
        """
        try:
            db.query(Resident).filter(Resident.user_id == user_id).update({Resident.mealplan_pin: new_pin})
            db.commit()
        except exc.SQLAlchemyError:
            db.rollback()
            return False
        return True

    @staticmethod
    def create_meal_plan_for_resident_by_email(meal_plan, plan_type, email):  # pylint: disable=unused-argument
        """
        Adds a new meal plan to the DB
        :param email: User to link to, TODO:implement
        :param pin: The plan's pin
        :param meal_plan: The plan's maximum credit count
        :param plan_type: The plan's reset period
        :return: True for success, False for failure
        """
        # Verify resident exists
        resident = ResidentService.get_resident_by_email(email)
        if resident is None:
            return None

        # Create mealplan
        meal_plan = MealService.create_meal_plan(meal_plan, plan_type)
        try:
            resident.mealplan_pin = meal_plan.pin
            db.commit()
        except exc.SQLAlchemyError:
            db.rollback()
            return None

        return meal_plan
