""" Test meal plan creation and usage. """
from ovs.tests.selenium.table_test import TableTest, PlainTextElement, InputTextElement, SelectTextElement

class TestMealPlan(TableTest):
    """ Tests meal plan creation and usage. """

    def setUp(self):
        super().setUp()
        # Current form has [User Email][Credits][Plan Type Selector]
        self.form_text_field_types.append(InputTextElement())
        self.form_text_field_types.append(InputTextElement())
        self.form_text_field_types.append(SelectTextElement())

        # Current table has [User Pin][Email][Current Credits][Credits][Plan Type]
        self.table_text_field_types.append(PlainTextElement())
        self.table_text_field_types.append(PlainTextElement())
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(SelectTextElement())

    def navigate_to_table_page(self):
        self.go_to_page_in_dropdown('Meal Plans', 'mealDropdown')

    def test_add_meal_plan(self):
        """ Tests that meal plans can be added for a default resident.

            Returns:
                string: the pin for the meal plan created
        """
        # Meal plan page has a non-standard table without a one-to-one form correspondence
        # Need to modify the table field types so the test knows where to look for added data
        default_test_table_fields = self.table_text_field_types
        self.table_text_field_types = [None, PlainTextElement(), None, \
                                       InputTextElement(), SelectTextElement()]
        self.add_table_test(self.default_resident_email, '20', 'Semesterly')
        self.table_text_field_types = default_test_table_fields

        # Need to verify second credits table field and return the pin
        # So other tests can use the created plan
        last_row = self.get_last_table_row()

        current_credits = self.table_text_field_types[2].get_text(last_row[2])
        self.assertEqual(current_credits, '20')
        user_pin = self.table_text_field_types[0].get_text(last_row[0])
        return user_pin

    def test_update_delete_meal_plan(self):
        """ Tests that added meal plans can be updated and deleted. """
        self.test_add_meal_plan()

        # Only care about the fields that can be edited for this test
        default_test_table_fields = self.table_text_field_types
        self.table_text_field_types = [None, None, InputTextElement(), \
                                       InputTextElement(), SelectTextElement()]
        self.update_delete_table_test('15', '25', 'Lifetime')
        self.table_text_field_types = default_test_table_fields

    def test_use_meal_plan(self):
        """ Tests that meal plans can be used and credits go down, and up for an undo. """
        created_plan_pin = self.test_add_meal_plan()

        # Navigate to 'Meal login'
        self.go_to_page_in_dropdown('Meal login', 'mealDropdown')

        # Use meal plan
        pin_text_field = self.browser.find_element_by_id('pin')
        pin_text_field.send_keys(created_plan_pin)
        sign_in_button = self.browser.find_element_by_class_name('btn-primary')
        sign_in_button.click()

        # Verify credits went down
        self.navigate_to_table_page()
        last_row = self.get_last_table_row()
        num_credits = self.table_text_field_types[2].get_text(last_row[2])
        self.assertEqual(num_credits, '19')

        # Use Undo button and verify credits restored
        self.go_to_page_in_dropdown('Meal login', 'mealDropdown')
        undo_button = self.browser.find_element_by_class_name('btn-secondary')
        undo_button.click()

        self.navigate_to_table_page()
        last_row = self.get_last_table_row()
        num_credits = self.table_text_field_types[2].get_text(last_row[2])
        self.assertEqual(num_credits, '20')
