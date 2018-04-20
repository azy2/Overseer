""" Test meal plan creation and usage. """
from selenium.webdriver.support.ui import Select
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestMealPlan(SeleniumBaseTestCase):
    """ Tests meal plan creation and usage. """

    def create_test_meal_plan(self):
        """ Creates a test meal plan for the default resident.

            Returns:
                string: the pin for the meal plan created
        """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()
        self.go_to_page_in_dropdown('Meal Plans', 'mealDropdown')

        # Make a Semesterly meal plan for the default resident
        email_text_field = self.browser.find_element_by_id('email')
        email_text_field.send_keys(self.default_resident_email)
        credits_text_field = self.browser.find_element_by_id('meal_plan')
        credits_text_field.send_keys('20')
        plan_type_selector = Select(self.browser.find_element_by_id('plan_type'))
        plan_type_selector.select_by_visible_text('Semesterly')
        register_button = self.browser.find_element_by_name('create_btn')
        register_button.click()

        # New meal plans get added to the bottom of the table, find last entry
        meal_plan_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = meal_plan_table.find_elements_by_tag_name('tr')[-1]
        row_entries = last_table_row.find_elements_by_tag_name('td')

        # Verify information in table matches information entered
        # Format is [PIN][Email][Current Credits][Meal Plan Credits][Plan Type]
        # All <input> tag fields have class named 'form-control'
        user_pin = row_entries[0].text.strip()
        user_email = row_entries[1].text.strip()
        num_credits = row_entries[2].find_element_by_class_name('form-control').get_attribute('value')
        meal_plan_credits = row_entries[3].find_element_by_class_name('form-control').get_attribute('value')
        plan_type_selector = Select(row_entries[4].find_element_by_class_name('form-control'))
        plan_type = plan_type_selector.first_selected_option.text

        self.assertEqual(user_email, self.default_resident_email)
        self.assertEqual(num_credits, '20')
        self.assertEqual(meal_plan_credits, '20')
        self.assertEqual(plan_type, 'Semesterly')

        # Return the user's pin for other meal plan tests to use
        return user_pin

    def test_create_meal_plan(self):
        """ Tests that custom meal plans can be created. """
        self.create_test_meal_plan()

    def test_use_meal_plan(self):
        """ Tests that meal plans can be used and credits go down, and up for an undo. """
        created_plan_pin = self.create_test_meal_plan()

        # Navigate to 'Meal login'
        self.go_to_page_in_dropdown('Meal login', 'mealDropdown')

        # Use meal plan
        pin_text_field = self.browser.find_element_by_id('pin')
        pin_text_field.send_keys(created_plan_pin)
        sign_in_button = self.browser.find_element_by_class_name('btn-primary')
        sign_in_button.click()

        # Verify credits went down
        self.go_to_page_in_dropdown('Meal Plans', 'mealDropdown')
        meal_plan_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = meal_plan_table.find_elements_by_tag_name('tr')[-1]
        row_entries = last_table_row.find_elements_by_tag_name('td')
        num_credits = row_entries[2].find_element_by_class_name('form-control').get_attribute('value')
        self.assertEqual(num_credits, '19')

        # Use Undo button and verify credits restored
        self.go_to_page_in_dropdown('Meal login', 'mealDropdown')
        undo_button = self.browser.find_element_by_class_name('btn-secondary')
        undo_button.click()

        self.go_to_page_in_dropdown('Meal Plans', 'mealDropdown')
        meal_plan_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = meal_plan_table.find_elements_by_tag_name('tr')[-1]
        row_entries = last_table_row.find_elements_by_tag_name('td')
        num_credits = row_entries[2].find_element_by_class_name('form-control').get_attribute('value')
        self.assertEqual(num_credits, '20')
