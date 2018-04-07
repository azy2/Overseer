"""
DB and utility functions for Meals
"""
from flask import current_app
from ovs.models.meal_plan_model import MealPlan

db = current_app.extensions['database'].instance()


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
    def use_meal(pin):
        """
        Uses a meal on the account with given pin
        :param pin: account to use
        :return: The updated account
        """
        user_plan = MealService.get_meal_plan_by_pin(pin)
        if user_plan is not None:
            has_meal = user_plan.update_meal_count()
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
