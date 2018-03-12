"""
Defines a User as represented in the database
"""
import bcrypt
import sqlalchemy as sa
from flask import jsonify

from ovs import app

SALT_ROUNDS = 12


class User(app.BaseModel):
    """
    Defines a User as represented in the database. Along with some utility functions.
    """
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(255), nullable=False, unique=True)
    first_name = sa.Column(sa.String(255), nullable=False)
    last_name = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.CHAR(60), nullable=False)
    role = sa.Column(sa.Enum('RESIDENT', 'RESIDENT_ADVISOR', 'STAFF',
                             'OFFICE_MANAGER', 'BUILDING_MANAGER', 'ADMIN'),
                     nullable=False)
    created = sa.Column(
        sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    updated = sa.Column(sa.DateTime, server_default=sa.text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, email, first_name, last_name, password, role):
        password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt(SALT_ROUNDS))
        super(User, self).__init__(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role)

    def __repr__(self):
        return "User([id='%s', email='%s', first_name='%s', last_name='%s', " + \
            "role='%s', created='%s', updated='%s'])" % \
            (self.id, self.email, self.first_name, self.last_name,
             self.role, self.created, self.updated)

    def has_password(self, password):
        """ Checks if inputted password matches the one stored in DB """
        return self.password.encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), self.password.encode('utf-8'))

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
