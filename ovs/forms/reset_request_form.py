""" Form with data required to login."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email
from ovs.forms.validators import EmailRegistered


class ResetRequestForm(FlaskForm):
    """ Form with data required to login."""
    email = StringField('Email', validators=[DataRequired(), Email(), EmailRegistered(check=True)])
