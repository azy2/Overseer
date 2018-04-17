""" Form with data required to login for a meal"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, ValidationError
from wtforms.validators import DataRequired

from ovs import db
from ovs.models.meal_plan_model import MealPlan


class AddMealForm(FlaskForm):
    """ Form with data required to login for a meal"""
    pin = IntegerField('PIN', validators=[DataRequired()])
    number = IntegerField('Number', validators=[DataRequired()])

    def validate_meal_pin(form, field):  # pylint: disable=unused-argument, no-self-use
        """
        Validates that the provided pin exists.
        This is to thwart malicious input.

        Args:
            form: The AddMealForm that was submitted.
            field: The meal_pin field.

        Raises:
            ValidationError: If meal_pin does not exist.
        """
        if db.session.query(MealPlan).filter(MealPlan.pin == field.data).count() == 0:
            raise ValidationError("Pin doesn't exist.")
