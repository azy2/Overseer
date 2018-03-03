"""
Tests for meal plan services
"""
from unittest import TestCase
from datetime import datetime
from ovs import app
from ovs.services.meal_service import MealService
from ovs.models.meal_plan_model import MealPlan


class TestMealPlanService(TestCase):
    """
    Tests for meal plan services
    """
    def setUp(self):
        """ Runs before every test and clears relevant tables """
        self.db = app.database.instance()
        self.tearDown()

    def tearDown(self):
        """ Runs after every tests and clears relevant tables """
        self.db.query(MealPlan).delete()
        self.db.commit()

    def test_create_meal_plan(self):
        """ Tests create_meal_plan """
        test_meal_plan_info = (141414, 10, 'WEEKLY')
        MealService.create_meal_plan(*test_meal_plan_info)
        meal_list = self.db.query(MealPlan).filter(MealPlan.pin == test_meal_plan_info[0]).all()
        self.assertEqual(len(meal_list), 1)
        meal_plan = meal_list[0]
        self.assertEqual((meal_plan.pin, meal_plan.meal_plan,
                          meal_plan.plan_type), test_meal_plan_info)

    def test_create_meal_plan_duplicate(self):
        """ Tests create_meal_plan for duplicate pin"""
        test_meal_plan_info = (141414, 10, 'WEEKLY')
        self.assertTrue(MealService.create_meal_plan(*test_meal_plan_info))
        test_meal_plan_info2 = (141414, 14, 'WEEKLY')
        self.assertFalse(MealService.create_meal_plan(*test_meal_plan_info2))
        meal_list = self.db.query(MealPlan).filter(MealPlan.pin == test_meal_plan_info[0]).all()
        self.assertEqual(len(meal_list), 1)
        meal_plan = meal_list[0]
        self.assertEqual((meal_plan.pin, meal_plan.meal_plan,
                          meal_plan.plan_type), test_meal_plan_info)

    def test_get_meal_plan_by_pin(self):
        """ Tests get_meal_plan_by_pin """
        test_meal_plan_info = (141414, 10, 'WEEKLY')
        MealService.create_meal_plan(*test_meal_plan_info)
        meal_plan = MealService.get_meal_plan_by_pin(test_meal_plan_info[0])
        self.assertEqual((meal_plan.pin, meal_plan.meal_plan,
                          meal_plan.plan_type), test_meal_plan_info)

    def test_get_meal_plan_by_pin_0(self):
        """ Tests get_meal_plan_by_pin with bad parameter"""
        meal_plan = MealService.get_meal_plan_by_pin(9999999)
        self.assertEqual(meal_plan, None)

    def test_use_meal(self):
        """ Tests use_meal for new user """
        test_meal_plan_info = (141414, 10, 'WEEKLY')
        MealService.create_meal_plan(*test_meal_plan_info)
        self.assertTrue(MealService.use_meal(test_meal_plan_info[0]))
        meal_plan = MealService.get_meal_plan_by_pin(test_meal_plan_info[0])
        self.assertEqual(test_meal_plan_info[1]-1, meal_plan.credits)
        #Add 1 minute to the reset time to avoid any flaky tests right around the reset period
        self.assertTrue(datetime.now() < meal_plan.reset_date.replace(minute=1))

    def test_use_meal_no_credits(self):
        """ Tests use_meal with no credits available"""
        #Test currently flaky if reset_date is between the first call and last call to use_meal
        test_meal_plan_info = (141414, 10, 'WEEKLY')
        MealService.create_meal_plan(*test_meal_plan_info)
        for _ in range(test_meal_plan_info[1]):
            self.assertTrue(MealService.use_meal(test_meal_plan_info[0]))
        meal_plan = MealService.get_meal_plan_by_pin(test_meal_plan_info[0])
        self.assertEqual(0, meal_plan.credits)
        self.assertFalse(MealService.use_meal(test_meal_plan_info[0]))

    def test_use_meal_invalid_pin(self):
        """ Tests use_meal with no account exisiting """
        self.assertFalse(MealService.use_meal(9999999))
