"""
The base test case for selenium that all other selenium tests should inherit from.
"""
import os
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from flask import current_app
from ovs import create_app, db
from ovs.datagen import DataGen

class SeleniumBaseTestCase(LiveServerTestCase):
    """
    The base test case for selenium that all other selenium tests should inherit from.
    """

    def create_app(self):
        """
        Creates a flask app instance for each test.
        Returns:
            Flask: a flask app.
        """
        app = create_app('config/config-selenium.json')
        return app

    def setUp(self):
        """ Creates a headless chrome instance for Selenium and clears the DB. """
        DataGen.create_defaults()
        db.session.flush()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1980,960") # Make screenshots larger
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(1)
        self.base_url = self.get_server_url()

        # Ensure browser executable is cleaned up at the end of the test
        self.addCleanup(self.browser.quit)

        # Set up default accounts for logging in
        default_resident = current_app.config['USERS']['RESIDENT']
        self.default_resident_email = default_resident['email']
        self.default_resident_password = default_resident['password']
        self.default_resident_name = default_resident['first_name']

        default_admin = current_app.config['USERS']['ADMIN']
        self.default_admin_email = default_admin['email']
        self.default_admin_password = default_admin['password']
        self.default_admin_name = default_admin['first_name']

    def tearDown(self):
        """ Closes selenium driver and OVSBaseTestCase clears the DB. """
        # Take screenshot at end of every test, Python unittesting has no non-hack way to detect a failed test case
        test_screenshot_dir = 'ovs/tests/selenium/Screenshots/' + type(self).__name__
        if not os.path.exists(test_screenshot_dir):
            os.makedirs(test_screenshot_dir)
        self.browser.save_screenshot(test_screenshot_dir + '/%s-last-test-run.png' % self._testMethodName)

    def login_default_resident(self):
        """ Convenience method to login with the default resident information. """
        self.login_with_credentials(self.default_resident_email, self.default_resident_password)

    def login_default_admin(self):
        """ Convenience method to login with the default admin information. """
        self.login_with_credentials(self.default_admin_email, self.default_admin_password)

    def login_with_credentials(self, email, password):
        """
        Logs in with the provided email and password.
        Args:
            email: Email to log in as.
            password: Password to use.
        """
        self.browser.find_element_by_id('login').send_keys(Keys.ENTER)
        name_box = self.browser.find_element_by_name('email')
        name_box.send_keys(email)
        pass_box = self.browser.find_element_by_name('password')
        pass_box.send_keys(password)
        pass_box.send_keys(Keys.ENTER)

    def set_text_field_by_id(self, field_id, new_text):
        """
        Sets the text in the given text form to the new text.
        Args:
            field_id: The html form id.
            new_text: The text to type.
        """
        text_field = self.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(new_text)

    def go_to_page_in_dropdown(self, page_link_name, dropdown_id):
        """ Clicks a dropdown and then selects the page to go to under that dropdown.
            Navigating to other pages requires doing this quite a bit.

            Args:
                dropdown_id (string): The ID of the dropdown to click.
                page_link_name (string): The name of the link that appears after clicking the dropdown.
         """
        dropdown = self.browser.find_element_by_id(dropdown_id)
        dropdown.click()
        link_in_dropdown = self.browser.find_element_by_link_text(page_link_name)
        link_in_dropdown.click()
