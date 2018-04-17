""" DB and utility functions for Users """
import logging

from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.mail import templates
from ovs.models.user_model import User
from ovs.services.mail_service import MailService
from ovs.services.resident_service import ResidentService
from ovs.utils import crypto


class UserService:
    """ DB and utility functions for Users """

    def __init__(self):
        pass

    @staticmethod
    def create_user(email, first_name, last_name, role, password=None):
        """
        Add a user entry to db.

        Args:
            email: The user's email address.
            first_name: The user's first name.
            last_name: The user's last name.
            role: The user's role.
            password: The user's password. If None a random one is generated.

        Returns:
            A User db model.
        """
        if password is None:
            password = crypto.generate_password()
        new_user = User(email, first_name, last_name, password, role)
        db.session.add(new_user)

        if role == 'RESIDENT':
            ResidentService.create_resident(new_user)

        UserService.send_setup_email(
            email, first_name, last_name, role, password)
        return new_user

    @staticmethod
    def edit_user(user_id, email, first_name, last_name):
        """
        Edits user identified by user id.

        Args:
            user_id: Unique user id.
            email: The user's email.
            first_name: The user's first_name.
            last_name: The user's last_name.

        Returns:
            If user was updated sucessfuly.
        """
        user = UserService.get_user_by_id(user_id)
        email_user = UserService.get_user_by_email(email)
        # Make user email is not associated with other existing users.
        user.update(email, first_name, last_name)

    @staticmethod
    def delete_user(user_id):
        """
        Deletes an existing user identified by user id.

        Args:
            user_id: Unique user id.

        Returns if the user was sucessfuly deleted.
        """
        user = UserService.get_user_by_id(user_id)
        if user.role == 'RESIDENT':
            ResidentService.delete_resident(user_id)

        db.session.delete(user)

    @staticmethod
    def send_setup_email(email, first_name, last_name, role, password):
        """
        Sends a setup email to the email address associated with a user.

        Args:
            email: The user's email address.
            first_name: The user's first name.
            last_name: The user's last name.
            role: The user's role.
            password: The user's password.
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
        Fetch a user identified by email.

        Args:
            user_id: The user's email address.

        Returns:
            A User db model.
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch a user identified by user id.

        Args:
            user_id: Unique user id.

        Returns:
            A User db model.
        """
        return User.query.filter_by(id=user_id).first()
