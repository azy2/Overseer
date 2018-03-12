""" Form with data required to edit a package """
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length
from ovs.models.resident_model import Resident
from ovs.models.package_model import Package
from ovs.models.user_model import User
from ovs import app
db = app.database.instance()


def validate_user_id(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided user_id exists.
    This is to thwart malicious input.
    """
    if db.query(Resident).filter(Resident.user_id == field.data).count() == 0:
        raise ValidationError('Resident does not exist')

def validate_package_id(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided package_id exists.
    This is to thwart malicious input.
    """
    if db.query(Package).filter(Package.id == field.data).count() == 0:
        raise ValidationError('Package does not exist')

def validate_resident_email(form, field):  # pylint: disable=unused-argument
    """
    Validates that the provided resident email exists.
    This is to thwart malicious input.
    """
    if db.query(Resident, User).join(User, Resident.user_id == User.id).filter(User.email == field.data).count() == 0:
        raise ValidationError('Resident does not exist. Please verify resident email.')

class EditPackageForm(FlaskForm):
    """ Form with data required to edit a package """
    package_id = StringField('Package ID', validators=[DataRequired(), validate_package_id]) # (hidden)
    recipient_id = StringField('Recipient ID', validators=[DataRequired(), validate_user_id]) # (hidden)
    recipient_email = StringField('Package Recipient', validators=[DataRequired(),
                                                                   validate_resident_email]) # (editable)
    checked_by = StringField('Checked By')
    checked_at = StringField('Checked At')
    is_signed = StringField('Is Signed')
    signed_at = StringField('Signed At')
    description = StringField('Package Description', validators=[Length(min=0, max=2047), DataRequired()]) # (editable)
