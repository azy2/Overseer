""" Tests functionality related to registering rooms. """
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestRegisterRoom(SeleniumBaseTestCase):
    """ Tests functionality related to registering rooms. """

    def test_register_room(self):
        """ Tests whether a room can be registered with the default resident. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Click on link to register rooms
        register_rooms_link = self.browser.find_element_by_link_text('Rooms')
        register_rooms_link.click()

        # Verify page changed
        self.assertIn('Rooms', self.browser.title)

        # Register a room
        self.set_text_field_by_id('room_number', '429D')
        self.set_text_field_by_id('room_status', 'rented')
        self.set_text_field_by_id('room_type', 'single')
        self.set_text_field_by_id('occupants', self.default_resident_email)
        submit_button = self.browser.find_element_by_id('register_room')
        submit_button.send_keys(Keys.ENTER)

        # Wait for successful notification popup to appear
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
        self.assertEqual(room_number, '429D')
        self.assertEqual(room_status, 'rented')
        self.assertEqual(room_type, 'single')
        self.assertEqual(num_occupants, '1')

    def test_register_room_invalid(self):
        """ Tests that rooms cannot be registered for residents that do not exist. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Attempt to add a resident that doesn't exist to a room
        register_rooms_link = self.browser.find_element_by_link_text('Rooms')
        register_rooms_link.click()
        self.set_text_field_by_id('room_number', '123')
        self.set_text_field_by_id('room_status', 'Legitimate Status')
        self.set_text_field_by_id('room_type', 'Yes')
        self.set_text_field_by_id('occupants', 'real_email@gmail.com')
        self.browser.find_element_by_id('register_room').click()

        # Wait for failure notification
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'invalid-feedback')))
