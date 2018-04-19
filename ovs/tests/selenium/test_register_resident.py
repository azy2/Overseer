""" Tests functionality related to registering residents. """
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestRegisterResident(SeleniumBaseTestCase):
    """ Tests functionality related to registering residents. """

    def test_register_resident(self):
        """ Tests whether residents can be registered. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Click on Residents link
        register_resident_link = self.browser.find_element_by_link_text('Residents')
        register_resident_link.click()

        # Verify page changed
        self.assertIn('Residents', self.browser.title)

        # Set all fields and register resident
        self.set_text_field_by_id('register_form-email', 'testing123@gmail.com')
        self.set_text_field_by_id('register_form-first_name', 'Test')
        self.set_text_field_by_id('register_form-last_name', 'Testerson')
        register_button = self.browser.find_element_by_name('register_btn')
        register_button.click()

        # New residents get added to the bottom of the table, find last entry
        meal_plan_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = meal_plan_table.find_elements_by_tag_name('tr')[-1]
        row_entries = last_table_row.find_elements_by_tag_name('td')

        # Verify resident information matches the last added resident
        # Current format is [Email][First Name][Last Name]
        last_added_email = row_entries[0].find_element_by_class_name('form-control').get_attribute('value')
        last_added_first_name = row_entries[1].find_element_by_class_name('form-control').get_attribute('value')
        last_added_last_name = row_entries[2].find_element_by_class_name('form-control').get_attribute('value')
        self.assertEqual(last_added_email, 'testing123@gmail.com')
        self.assertEqual(last_added_first_name, 'Test')
        self.assertEqual(last_added_last_name, 'Testerson')
