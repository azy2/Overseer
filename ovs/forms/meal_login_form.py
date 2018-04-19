""" Form with data required to login for a meal"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, ValidationError

from ovs import db
from ovs.models.meal_plan_model import MealPlan

class MealLoginForm(FlaskForm):
    """ Form with data required to login for a meal"""
    pin = IntegerField('PIN', validators=[])

    def validate_pin(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided pin exists.
        This is to thwart malicious input.

        Args:
            form: The MealLoginForm that was submitted.
            field: The pin field.

        Raises:
            ValidationError: If pin does not exist.
        """
        if db.session.query(MealPlan).filter(MealPlan.pin == field.data).count() == 0:
            raise ValidationError('Invalid Pin')
