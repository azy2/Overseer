"""
Defines a User as represented in the database
"""

from flask import jsonify
from flask_bcrypt import Bcrypt, bcrypt
from sqlalchemy import Integer, Enum, Column, CHAR, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ovs import db

SALT_ROUNDS = 12

bcrypt_app = Bcrypt()


class User(db.Model):
    """
    Defines a User as represented in the database.
    Args:
        email (str): The user's email.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        password (str): The user's initial password.
        role (Enum): The user's role. Must be one of 'RESIDENT', 'RESIDENT_ADVISOR',
                     'STAFF', 'OFFICE_MANAGER', 'BUILDING_MANAGER', or 'ADMIN'

    Returns:
        User: A User Model object.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(CHAR(60), nullable=False)
    role = Column(Enum('RESIDENT', 'RESIDENT_ADVISOR', 'STAFF',
                       'OFFICE_MANAGER', 'BUILDING_MANAGER', 'ADMIN'),
                  nullable=False)
    profile = relationship('Profile', uselist=False, back_populates='user',
                           cascade='all, delete, delete-orphan')
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    resident = relationship('Resident', uselist=False, cascade='delete, delete-orphan')

    def __init__(self, email, first_name, last_name, password, role):
        if password is None:
            password = bcrypt.gensalt()
        password_hash = current_app.extensions['bcrypt'].generate_password_hash(password)
        super(User, self).__init__(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password_hash,
            role=role)

    def __repr__(self):
        """
        Allows User to be printed.
        Returns:
            str: A string representation of this User.
        """
        return 'User([id={id}, email={email}, first_name={first_name}, last_name={last_name}, role={role}, ' \
               'created={created}, updated={updated}])'.format(**self.__dict__)

    def has_password(self, password):
        """
        Checks if inputted password matches the one stored in DB
        Args:
            password: The typed in password

        Returns:
            bool: True if `password` matches the one in the database, False otherwise.
        """
        return bcrypt_app.check_password_hash(self.password, password)

    def json(self):
        """
        Returns a JSON representation of this User
        Returns:
            A JSON representation of this User.
        """
        return jsonify(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            role=self.role,
            created=self.created,
            updated=self.updated
        )

    def update(self, email, first_name, last_name):
        """
        Updates user with new information
        Args:
            email: The new email address.
            first_name: The new first_name.
            last_name: The new last_name.
        """
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def is_authenticated(self):  # pylint: disable=no-self-use
        """
        Checks if a user is authenticated. Always returns True as required by Flask.
        Returns:
            True
        """
        return True

    def is_active(self):  # pylint: disable=no-self-use
        """
        Checks if this user account is active. Always returns True as required by Flask.
        Returns:
            True
        """
        return True

    def is_anonymous(self):  # pylint: disable=no-self-use
        """
        Checks if this user is anonymous. Always returns False as required by Flask.
        Returns:
            False
        """
        return False

    def get_id(self):
        """
        Retrieve this users id in the database as a string.
        Returns:
            str: The user's id.
        """
        return str(self.id)

    def update_password(self, new_password):
        """
        Updates the password of the user.

        Args:
            new_password: The newpassword to hash and set as the user pass.

        Returns:
            The updated model.
        """
        self.password = bcrypt_app.generate_password_hash(new_password)
        return self
