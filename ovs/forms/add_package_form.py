""" Form with data required to add a package """
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import Length, DataRequired
from flask import current_app

from ovs.models.resident_model import Resident
from ovs.models.user_model import User

db = current_app.extensions['database'].instance()


def validate_resident_email(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided resident email exists.
    This is to thwart malicious input.
    """
    if db.query(Resident, User).join(User, Resident.user_id == User.id).filter(User.email == field.data).count() == 0:
        raise ValidationError('Resident does not exist. Please verify resident email.')


class AddPackageForm(FlaskForm):
    """ Form with data required to add a package """
    recipient_email = StringField('Recipient\'s Email Address',
                                  validators=[Length(min=6, max=35), DataRequired(), validate_resident_email])
    description = StringField('Package Description', validators=[Length(min=0, max=2047)])
