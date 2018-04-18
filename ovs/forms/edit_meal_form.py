""" Form with data required to edit a meal"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, ValidationError, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange

from ovs import db
from ovs.models.meal_plan_model import MealPlan

class EditMealForm(FlaskForm):
    """ Form with data required to edit a meal"""
    pin = HiddenField('PIN', validators=[DataRequired()])
    credit = IntegerField('Credit', validators=[NumberRange(min=0)])
    meal_plan = IntegerField('Meal Plan', validators=[NumberRange(min=1)])
    plan_type = SelectField('Plan Type', choices=[('WEEKLY', 'Weekly'),
                                                  ('SEMESTERLY', 'Semesterly'),
                                                  ('LIFETIME', 'Lifetime')])
    update_button = SubmitField('Update')
    delete_button = SubmitField('Delete')

    def validate_pin(form, field):  # pylint: disable=no-self-argument, no-self-use
        """
        Validates that the provided pin exists
        This is to thwart malicious input.
        """
        if db.session.query(MealPlan).filter(MealPlan.pin == field.data).count() == 0:
            raise ValidationError("Pin doesn't exist.")
