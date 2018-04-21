""" Tests functionality related to packages. """
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestPackage(SeleniumBaseTestCase):
    """ Tests functionality related to packages. """

    def get_last_package_table_row(self):
        """ Gets a list of WebElements corresponding to the data for the last row in the package table.

            Return:
                List of WebElement: The last row in the package table.
        """
        package_table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = package_table.find_elements_by_tag_name('tr')[-1]
        return last_table_row.find_elements_by_tag_name('td')

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
        row_entries = self.get_last_package_table_row()

        # Verify package information matches the last added package
        # Current format is [Recipient Whole Name][Email][User Checked By][Check Time][Description]
        recipient_name = row_entries[0].text
        recipient_email = row_entries[1].find_element_by_class_name('form-control').get_attribute('value')
        package_description = row_entries[4].find_element_by_class_name('form-control').get_attribute('value')
        self.assertIn(self.default_resident_name, recipient_name)
        self.assertEqual(recipient_email, self.default_resident_email)
        self.assertEqual(package_description, 'The Stuff')

    def test_update_delete_package(self):
        """ Tests that packages can be updated and deleted """
        self.test_add_package()

        # Verify that changing fields without pressing 'Update' does not change anything
        # New packages get added to the bottom of the table, find last entry
        row_entries = self.get_last_package_table_row()
        package_desc_text_field = row_entries[4].find_element_by_class_name('form-control')

        desc_initial_text = package_desc_text_field.get_attribute('value')
        package_desc_text_field.clear()
        package_desc_text_field.send_keys('Testing')
        self.browser.find_element_by_link_text('Packages').click()
        row_entries = self.get_last_package_table_row()
        package_desc_text_field = row_entries[4].find_element_by_class_name('form-control')
        self.assertEqual(desc_initial_text, package_desc_text_field.get_attribute('value'))

        # Update the text and verify that it changes
        package_desc_text_field.clear()
        package_desc_text_field.send_keys('Testing')
        update_button = row_entries[5].find_element_by_class_name('btn')
        update_button.click()
        self.browser.find_element_by_link_text('Packages').click()
        row_entries = self.get_last_package_table_row()
        package_desc_text_field = row_entries[4].find_element_by_class_name('form-control')
        self.assertEqual('Testing', package_desc_text_field.get_attribute('value'))

        # Deliver the package and verify table has one less row
        package_table = self.browser.find_element_by_class_name('table-responsive')
        table_rows = package_table.find_elements_by_tag_name('tr')
        num_packages = len(table_rows)
        last_row_entries = table_rows[-1].find_elements_by_tag_name('td')
        deliver_button = last_row_entries[6].find_element_by_class_name('btn')
        deliver_button.click()
        package_table = self.browser.find_element_by_class_name('table-responsive')
        table_rows = package_table.find_elements_by_tag_name('tr')
        self.assertEqual(num_packages - 1, len(table_rows))
