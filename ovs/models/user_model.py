"""
Defines a User as represented in the database
"""

from flask import jsonify
from flask_bcrypt import bcrypt
from sqlalchemy import Integer, Enum, Column, CHAR, String, text, DateTime

from ovs import app, bcrypt_app

SALT_ROUNDS = 12


class User(app.BaseModel):
    """
    Defines a User as represented in the database. Along with some utility functions.
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
    created = Column(
        DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(DateTime, server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, email, first_name, last_name, password, role):
        if password is None:
            password = bcrypt.gensalt()
        password_hash = bcrypt_app.generate_password_hash(password)
        super(User, self).__init__(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password_hash,
            role=role)

    def __repr__(self):
        return 'User([id={id}, email={email}, first_name={first_name}, last_name={last_name}, role={role}, ' \
               'created={created}, updated={updated}])'.format(**self.__dict__)

    def has_password(self, password):
        """ Checks if inputted password matches the one stored in DB """
        to_check = password.encode('utf-8')
        actual = self.password.encode('utf-8')

        return bcrypt_app.check_password_hash(actual, to_check)

    def json(self):
        """ Returns a JSON representation of this User """
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
        """
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def is_authenticated(self):  # pylint: disable=no-self-use
        """ Checks if a user is authenticated """
        return True

    def is_active(self):  # pylint: disable=no-self-use
        """ Checks if this user account is active """
        return True

    def is_anonymous(self):  # pylint: disable=no-self-use
        """ Checks if this user is anonymous """
        return False

    def get_id(self):
        """ :returns the user's unique id in the database """
        return str(self.id)
