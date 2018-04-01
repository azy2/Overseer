""" DB and utility functions for Users """
from sqlalchemy import exc

from ovs import app
from ovs.models.user_model import User
from ovs.services.mail_service import MailService
from ovs.services.meal_service import MealService
from ovs.services.resident_service import ResidentService
from ovs.utils import crypto
from ovs.mail import templates

db = app.database.instance()


class UserService:
    """ DB and utility functions for Users """

    def __init__(self):
        pass

    @staticmethod
    def create_user(email, first_name, last_name, role, password=None):
        """
        Adds a new user to the DB and generates a random password
        for them if none is provided
        :param email: The User's email
        :param first_name: The User's first name
        :param last_name: The User's last name
        :param role: The User's role. See `ovs.utils.roles`
        :param password: The User's password. If none is provided a
        random one will be generated
        :return: The newly created User
        """
        if password is None:
            password = crypto.generate_password()
        new_user = User(email, first_name, last_name, password, role)
        try:
            db.add(new_user)
            db.commit()
        except exc.IntegrityError:
            db.rollback()
            return None
        if role == 'RESIDENT':
            ResidentService.create_resident(new_user)

        UserService.send_setup_email(email, first_name, last_name, role, password)

        return new_user

    @staticmethod
    def edit_user(user_id, email, first_name, last_name):
        """
        Edits user with user_id with new information
        """
        print(user_id)
        user = UserService.get_user_by_id(user_id).first()
        if user is None: #Error : bad user_id
            return False

        email_user = UserService.get_user_by_email(email).first()
        if email_user is None or email_user == user: #We don't want to overwrite somebody else
            user.update(email, first_name, last_name)
            return True
        return False

    @staticmethod
    def send_setup_email(email, first_name, last_name, role, password):
        """
        Sends setup email to a provided user
        """
        user_info_substitution = {
            "first_name": first_name,
            "last_name": last_name,
            "role": role,
            "password": password
        }
        MailService.send_email(email, 'User Account Creation',
                               templates['user_creation_email'],
                               substitutions=user_info_substitution)

    @staticmethod
    def get_user_by_email(email):
        """
        Gets a user by their email
        :param email: The email of the user
        :return: The db entry of that user
        """
        return db.query(User).filter(User.email == email)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Gets a user by their id
        """
        return db.query(User).filter(User.id == user_id)

    @staticmethod
    def create_meal_plan_for_user_by_email(pin, meal_plan, plan_type, email):  # pylint: disable=unused-argument
        """
        Adds a new meal plan to the DB
        :param email: User to link to, TODO:implement
        :param pin: The plan's pin
        :param meal_plan: The plan's maximum credit count
        :param plan_type: The plan's reset period
        :return: True for success, False for failure
        """
        valid = MealService.create_meal_plan(pin, meal_plan, plan_type)
        return valid
