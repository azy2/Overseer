from flask import jsonify
import sqlalchemy as sa
from ovs import app
import bcrypt

SALT_ROUNDS = 12

class User(app.BaseModel):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(255), nullable=False, unique=True)
    password = sa.Column(sa.CHAR(60), nullable=False)
    role = sa.Column(sa.Enum('RESIDENT', 'RESIDENT_ADVISOR', 'STAFF', 'OFFICE_MANAGER', 'BUILDING_MANAGER', 'ADMIN'), nullable=False)
    created = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    updated = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, email, password, role):
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(SALT_ROUNDS))
        super(User, self).__init__(email=email, password=password, role=role)

    def __repr__(self):
        return "User([id='%s', email='%s', role='%s', created='%s', updated='%s'])" % \
            (self.id, self.email, self.role, self.created, self.updated)

    def has_password(self, password):
        return self.password == bcrypt.hashpw(password, self.password)

    def json(self):
        return jsonify(
            id = self.id,
            email = self.email,
            role = self.role,
            created = self.created,
            updated = self.updated
        )
