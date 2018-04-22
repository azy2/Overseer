""" Tests functionality related to registering rooms. """
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.table_test import TableTest, InputTextElement

class TestRegisterRoom(TableTest):
    """ Tests functionality related to registering rooms. """

    def setUp(self):
        super().setUp()
        self.form_text_field_ids.append('room_number')
        self.form_text_field_ids.append('room_status')
        self.form_text_field_ids.append('room_type')
        self.form_text_field_ids.append('occupants')

        # Current format is [Room Number][Status][Type][Num Occupants]
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(None)

    def navigate_to_table_page(self):
        self.browser.find_element_by_link_text('Rooms').click()

    def test_register_room(self):
        """ Tests whether a room can be registered with the default resident. """
        self.add_table_test('429D', 'rented', 'single', self.default_resident_email)

        # Need to also verify that the number of occupants is 1
        last_table_row = self.get_last_table_row()
        num_occupants = last_table_row[3].text.strip()
        self.assertEqual(num_occupants, '1')

    def test_update_delete_room(self):
        """ Tests that registered rooms can be updated and deleted. """
        self.test_register_room()
        self.update_delete_table_test('420D', 'Status goes here', 'Type goes here', None)

    def test_register_room_invalid(self):
        """ Tests that rooms cannot be registered for residents that do not exist. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Attempt to add a resident that doesn't exist to a room
        self.navigate_to_table_page()
        self.add_to_table('123', 'Legitimate Status', 'Yes', 'real_email@gmail.com')

        # Wait for failure notification
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'invalid-feedback')))
