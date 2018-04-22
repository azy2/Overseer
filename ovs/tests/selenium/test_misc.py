""" Tests miscellaneous functionality. """
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestMisc(SeleniumBaseTestCase):
    """ Tests miscellaneous functionality. """

    def test_autocomplete(self):
        """ Tests whether autocomplete is working. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Click on Packages link, we will use the packages page to test autocomplete
        package_link = self.browser.find_element_by_link_text('Packages')
        package_link.click()

        # Verify page changed
        self.assertIn('Packages', self.browser.title)

        # Use email field with first 5 characters of default resident email
        email_field = self.browser.find_element_by_id('add_form-recipient_email')

        # Simulate typing slowly or autocomplete doesn't pick up on Selenium
        for i in range(5):
            email_field.send_keys(self.default_resident_email[i])
            self.browser.implicitly_wait(1)

        # Autocomplete should have appeared by now
        autocomplete_container = self.browser.find_element_by_id('ui-id-1')
        first_result = autocomplete_container.find_element_by_tag_name('li')
        first_result.click()

        # Get the email field again or it will be a stale element reference
        email_field = self.browser.find_element_by_id('add_form-recipient_email')
        self.assertEqual(email_field.get_attribute('value'), self.default_resident_email)
