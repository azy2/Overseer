"""
Service routines and db access for the Auth layer
"""
import logging

from flask_login import LoginManager
from sqlalchemy.exc import SQLAlchemyError

from ovs import db
from ovs.models.user_model import User

LOGIN_MANAGER = LoginManager()


class AuthService:
    """Contains application methods relevant to the Authentication layer"""
    @staticmethod
    @LOGIN_MANAGER.user_loader
    def load_user(user_id):
        """
        Fetch a user by user id.

        Args:
            user_id: Unique user id.

        Returns:
            A User db model.
        """
        try:
            return db.session.query(User).get(int(user_id))
        except SQLAlchemyError:
            logging.exception('Faied to fetch user by user id.')

    @staticmethod
    def verify_auth(user, password):
        """
        Verify the password authenticates a given user.

        Args:
            user: A User model.
            password: Input password.

        Returns:
            If the user is authenticated.
        """
        return user.has_password(password)
