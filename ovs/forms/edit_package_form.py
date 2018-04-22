""" Form with data required to edit a package """
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

from ovs import db
from ovs.models.package_model import Package
from ovs.models.resident_model import Resident
from ovs.models.user_model import User



class EditPackageForm(FlaskForm):
    """ Form with data required to edit a package """
    package_id = HiddenField('Package ID', validators=[DataRequired()])
    recipient_email = StringField('Package Recipient', validators=[DataRequired()])
    description = StringField('Package Description', validators=[Length(min=0, max=2047), DataRequired()])
    update_button = SubmitField('Update')
    deliver_button = SubmitField('Deliver')

    def validate_recipient_id(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided user_id exists.
        This is to thwart malicious input.

        Args:
            form: The EditPackageForm that was submitted.
            field: The recipient_id field.

        Raises:
            ValidationError: If recipient_id does not correspond to an existing resident.
        """
        if db.session.query(Resident).filter(Resident.user_id == field.data).count() == 0:
            raise ValidationError('Resident does not exist')

    def validate_package_id(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided package_id exists.
        This is to thwart malicious input.

        Args:
            form: The EditPackageForm that was submitted.
            field: The package_id field.

        Raises:
            ValidationError: If package_id not correspond to an existing package.
        """
        if db.session.query(Package).filter(Package.id == field.data).count() == 0:
            raise ValidationError('Package does not exist')

    def validate_recipient_email(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided resident email exists.
        This is to thwart malicious input.

        Args:
            form: The EditPackageForm that was submitted.
            field: The recipient_email field.

        Raises:
            ValidationError: If package_id not correspond to an existing package.
        """
        user = User.query.filter_by(email=field.data).first()
        if user is None or user.resident is None:
            raise ValidationError('Resident does not exist. Please verify resident email.')
