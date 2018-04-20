""" Form with data required to add a package """
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import Length, DataRequired

from ovs import db
from ovs.models.resident_model import Resident
from ovs.models.user_model import User


class AddPackageForm(FlaskForm):
    """ Form with data required to add a package """
    recipient_email = StringField('Recipient\'s Email Address',
                                  validators=[Length(min=6, max=35), DataRequired()])
    description = StringField('Package Description', validators=[Length(min=0, max=2047)])

    def validate_resident_email(form, field):  # pylint: disable=unused-argument, no-self-use, no-self-argument
        """
        Validates that the provided resident email exists.
        This is to thwart malicious input.

        Args:
            form: The AddPackageForm that was submitted.
            field: The resident_email field.

        Raises:
            ValidationError: If resident_email does not correspond to an existing account.
        """
        if db.session.query(Resident, User).join(User, Resident.user_id == User.id) \
                .filter(User.email == field.data).count() == 0:
            raise ValidationError('Resident does not exist. Please verify resident email.')
