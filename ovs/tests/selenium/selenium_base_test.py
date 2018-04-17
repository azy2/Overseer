"""
The base test case for selenium that all other selenium tests should inherit from
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from flask import current_app
from ovs import create_app, db
from ovs.datagen import DataGen
from ovs.tests.unittests.base_test import OVSBaseTestCase

class SeleniumBaseTestCase(OVSBaseTestCase):
    """
    The base test case for selenium that all other selenium tests should inherit from
    """

    def create_app(self):
        app = create_app('config/config-selenium.json')
        app.config['LIVESERVER_PORT'] = 0
        return app

    def setUp(self):
        """ Creates a headless chrome instance for selenium and clears the DB """
        super().setUp()
        DataGen.create_defaults()
        db.session.flush()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1980,960") # Make screenshots larger
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(1)
        self.base_url = self.get_server_url()

        # Set up default accounts for logging in
        default_resident = current_app.config['USERS']['RESIDENT']
        self.default_resident_email = default_resident['email']
        self.default_resident_password = default_resident['password']
        self.default_resident_name = default_resident['first_name']

        default_admin = current_app.config['USERS']['ADMIN']
        self.default_admin_email = default_admin['email']
        self.default_admin_password = default_admin['password']
        self.default_admin_name = default_admin['first_name']

    def login_default_resident(self):
        """ Convenience method to login with the default resident information """
        self.login_with_credentials(self.default_resident_email, self.default_resident_password)

    def login_default_admin(self):
        """ Convenience method to login with the default admin information """
        self.login_with_credentials(self.default_admin_email, self.default_admin_password)

    def login_with_credentials(self, email, password):
        """ Logs in with the provided email and password, most selenium tests will call this """
        name_box = self.browser.find_element_by_name('email')
        name_box.send_keys(email)
        pass_box = self.browser.find_element_by_name('password')
        pass_box.send_keys(password)
        pass_box.send_keys(Keys.ENTER)

    def set_text_field_by_id(self, field_id, new_text):
        """ Sets the text in the given text field to the new text """
        text_field = self.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(new_text)
