""" Tests functionality across routes. """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestCrossSystem(SeleniumBaseTestCase):
    """ Tests functionality across routes. """

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
