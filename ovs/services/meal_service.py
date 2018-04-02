"""
DB and utility functions for Meals
"""
from datetime import datetime

from ovs import app
from ovs.models.meal_plan_model import MealPlan

db = app.database.instance()


class MealService:
    """ DB and utility functions for Meals """

    def __init__(self):
        pass

    @staticmethod
    def create_meal_plan(pin, meal_plan, plan_type):
        """
        Adds a new meal plan to the DB
        :param pin: The plan's pin
        :param meal_plan: The plan's maximum credit count
        :param plan_type: The plan's reset period
        :return: True for success, False for failure
        """
        if MealService.get_meal_plan_by_pin(pin) is not None:
            return False
        new_plan = MealPlan(pin, meal_plan, plan_type)
        db.add(new_plan)
        db.commit()
        return True

    @staticmethod
    def add_meals(pin, number):
        """
        Add numbers of meal credits
        :param pin: The plan's pin
        :type pin: int
        :param number: Number of credits
        :type number: int
        :return: validity of adding
        :rtype: bool
        """
        meal_plan = MealService.get_meal_plan_by_pin(pin)
        if meal_plan is None:
            return False
        meal_plan.credits += number
        db.commit()
        return True

    @staticmethod
    def update_meal_count(meal_plan):
        """
        Reset meal plan credits if past reset data
        Decrement meal plan credits if available
        Commit changes to DB
        :param meal_plan: 
        :type meal_plan: 
        :return: whether a credit was available
        :rtype: bool
        """
        if meal_plan.reset_date is None or datetime.utcnow() > meal_plan.reset_date:
            meal_plan.reset_date = meal_plan.get_next_reset_date()
            meal_plan.credits = meal_plan.meal_plan
        was_updated = False
        if meal_plan.credits > 0:
            meal_plan.credits -= 1
            was_updated = True
        db.commit()
        return was_updated

    @staticmethod
    def use_meal(pin):
        """
        Uses a meal on the account with given pin
        :param pin: account to use
        :return: The updated account
        """
        user_plan = MealService.get_meal_plan_by_pin(pin)
        if user_plan is not None:
            has_meal = MealService.update_meal_count(user_plan)
            if has_meal:
                MealService.log_meal_use(pin)
            return has_meal
        return False

    @staticmethod
    def get_meal_plan_by_pin(pin):
        """
        Gets the account with given pin
        :param pin: account to use
        :return: The account
        """
        return db.query(MealPlan).filter(MealPlan.pin == pin).first()

    @staticmethod
    def log_meal_use(pin):
        """
        Logs a meal use on the given account
        :param pin: account to use
        :return: TBD
        """
        pass
