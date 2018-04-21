""" Tests functionality across routes. """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestCrossSystem(SeleniumBaseTestCase):
    """ Tests functionality across routes. """

    def test_preferred_name_meal_plan(self):
        """ Tests that updating a resident's preferred name updates it for meal plans. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Create a meal plan for the new resident
        self.go_to_page_in_dropdown('Meal Plans', 'mealDropdown')

        # Make a 20 credit Semesterly meal plan for the created resident
        email_text_field = self.browser.find_element_by_id('email')
        email_text_field.send_keys(self.default_resident_email)
        credits_text_field = self.browser.find_element_by_id('meal_plan')
        credits_text_field.send_keys('20')
        plan_type_selector = Select(self.browser.find_element_by_id('plan_type'))
        plan_type_selector.select_by_visible_text('Semesterly')
        register_button = self.browser.find_element_by_name('create_btn')
        register_button.click()

        # New meal plans get added to the bottom of the table, find last entry to get the pin
        meal_plan_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = meal_plan_table.find_elements_by_tag_name('tr')[-1]
        resident_pin = last_table_row.find_elements_by_tag_name('td')[0].text.strip()

        # Use the meal plan
        self.go_to_page_in_dropdown('Meal login', 'mealDropdown')
        pin_text_field = self.browser.find_element_by_id('pin')
        pin_text_field.send_keys(resident_pin)
        sign_in_button = self.browser.find_element_by_class_name('btn-primary')
        sign_in_button.click()

        # Verify that the new resident's name is used in the confirmation
        # This element is likely to change on the page, really should have an ID attached
        confirmation_holder = self.browser.find_elements_by_class_name('col-6')[1]
        self.assertIn(self.default_resident_name, confirmation_holder.find_element_by_tag_name('p').text)

        # Log in to new resident account and edit preferred name in profile
        self.go_to_page_in_dropdown('Logout', 'accountDropdown')
        super().login_default_resident()
        self.go_to_page_in_dropdown('Profile', 'accountDropdown')      

        # Change preferred name and submit changes
        self.set_text_field_by_id('preferred_name', 'Megatron')
        self.browser.find_element_by_id('submit_changes').send_keys(Keys.ENTER)

        # Wait for successful notification popup to appear
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.ID, 'notification-message')))

        # Go back to meal plan and verify name updated
        self.go_to_page_in_dropdown('Logout', 'accountDropdown')
        super().login_default_admin()
        self.go_to_page_in_dropdown('Meal login', 'mealDropdown')
        confirmation_holder = self.browser.find_elements_by_class_name('col-6')[1]
        self.assertIn('Megatron', confirmation_holder.find_element_by_tag_name('p').text)

    def test_new_resident_add_room(self):
        """ Tests that newly created residents can be added to rooms. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()
        
        # Attempt to add a resident that doesn't exist to a room
        register_rooms_link = self.browser.find_element_by_link_text('Rooms')
        register_rooms_link.click()
        self.set_text_field_by_id('room_number', '57')
        self.set_text_field_by_id('room_status', 'Yes')
        self.set_text_field_by_id('room_type', 'No')
        self.set_text_field_by_id('occupants', 'testing123@gmail.com')
        self.browser.find_element_by_id('register_room').click()

        # Wait for failure notification
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'invalid-feedback')))

        # Create a new resident
        register_resident_link = self.browser.find_element_by_link_text('Residents')
        register_resident_link.click()

        # Set all fields and register resident
        self.set_text_field_by_id('register_form-email', 'testing123@gmail.com')
        self.set_text_field_by_id('register_form-first_name', 'Test')
        self.set_text_field_by_id('register_form-last_name', 'Testerson')
        register_button = self.browser.find_element_by_name('register_btn')
        register_button.click()

        # Now try to add the new resident and default resident to the room 
        register_room_link = self.browser.find_element_by_link_text('Rooms')
        register_room_link.click()
        self.set_text_field_by_id('room_number', '57')
        self.set_text_field_by_id('room_status', 'Yes')
        self.set_text_field_by_id('room_type', 'No')
        self.set_text_field_by_id('occupants', 'testing123@gmail.com,' + self.default_resident_email)
        self.browser.find_element_by_id('register_room').click()

        # Wait for success notification
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.ID, 'notification-message')))

        # Verify information added correctly, new rooms get added to the bottom of the table
        # Format is [Room Number][Room Status][Room Type][Number of Occupants]
        rooms_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = rooms_table.find_elements_by_tag_name('tr')[-1]
        last_row_entries = last_table_row.find_elements_by_tag_name('td')
        room_number = last_row_entries[0].find_element_by_class_name('form-control').get_attribute('value')
        room_status = last_row_entries[1].find_element_by_class_name('form-control').get_attribute('value')
        room_type = last_row_entries[2].find_element_by_class_name('form-control').get_attribute('value')
        num_occupants = last_row_entries[3].text
        self.assertEqual(room_number, '57')
        self.assertEqual(room_status, 'Yes')
        self.assertEqual(room_type, 'No')
        self.assertEqual(num_occupants, '2')
