""" Form with data required to login."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class ResetRequestForm(FlaskForm):
    """ Form with data required to login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
