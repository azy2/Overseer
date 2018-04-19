""" Tests functionality related to packages. """
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestPackage(SeleniumBaseTestCase):
    """ Tests functionality related to packages. """

    def test_add_package(self):
        """ Tests whether packages can be added for the default resident. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Click on Packages link
        package_link = self.browser.find_element_by_link_text('Packages')
        package_link.click()

        # Verify page changed
        self.assertIn('Packages', self.browser.title)

        # Set all fields and register resident
        self.set_text_field_by_id('add_form-recipient_email', self.default_resident_email)
        self.set_text_field_by_id('add_form-description', 'The Stuff')
        check_package_button = self.browser.find_element_by_name('check_btn')
        check_package_button.click()

        # Wait for successful add notification
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.ID, 'notification-message')))

        # New packages get added to the bottom of the table, find last entry
        meal_plan_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = meal_plan_table.find_elements_by_tag_name('tr')[-1]
        row_entries = last_table_row.find_elements_by_tag_name('td')

        # Verify package information matches the last added package
        # Current format is [Recipient Whole Name][Email][User Checked By][Check Time][Description]
        recipient_name = row_entries[0].text
        recipient_email = row_entries[1].find_element_by_class_name('form-control').get_attribute('value')
        package_description = row_entries[4].find_element_by_class_name('form-control').get_attribute('value')
        self.assertIn(self.default_resident_name, recipient_name)
        self.assertEqual(recipient_email, self.default_resident_email)
        self.assertEqual(package_description, 'The Stuff')
