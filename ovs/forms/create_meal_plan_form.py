""" Form with data required to create a meal plan """
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length


class CreateMealPlanForm(FlaskForm):
    """ Form with data required to register a resident """
    email = StringField('User Email Address', validators=[Length(min=6, max=35), DataRequired()])
    meal_plan = IntegerField('Meal Plan', validators=[DataRequired()])
    plan_type = SelectField('Plan Type', choices=[('WEEKLY', 'Weekly'),
                                                  ('SEMESTERLY', 'Semesterly'),
                                                  ('LIFETIME', 'Lifetime')])
