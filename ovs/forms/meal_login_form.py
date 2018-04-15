""" Form with data required to login for a meal"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, ValidationError
from wtforms.validators import DataRequired

from ovs import db
from ovs.models.meal_plan_model import MealPlan

class MealLoginForm(FlaskForm):
    """ Form with data required to login for a meal"""
    pin = IntegerField('PIN', validators=[])

    def validate_pin(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided pin existsself.
        This is to thwart malicious input.
        """
        if db.session.query(MealPlan).filter(MealPlan.pin == field.data).count() == 0:
            raise ValidationError('Invalid Pin')


