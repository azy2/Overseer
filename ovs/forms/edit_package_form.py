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
    recipient_id = HiddenField('Recipient ID', validators=[DataRequired()])
    recipient_email = StringField('Package Recipient', validators=[DataRequired()])
    description = StringField('Package Description', validators=[Length(min=0, max=2047), DataRequired()])
    update_button = SubmitField('Update')
    check_button = SubmitField('Check')

    def validate_recipient_id(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided user_id exists.
        This is to thwart malicious input.
        """
        if db.session.query(Resident).filter(Resident.user_id == field.data).count() == 0:
            raise ValidationError('Resident does not exist')


    def validate_package_id(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided package_id exists.
        This is to thwart malicious input.
        """
        if db.session.query(Package).filter(Package.id == field.data).count() == 0:
            raise ValidationError('Package does not exist')


    def validate_recipient_email(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided resident email exists.
        This is to thwart malicious input.
        """
        if db.session.query(User).filter(User.email == field.data).count() == 0:
            raise ValidationError('Resident does not exist. Please verify resident email.')
