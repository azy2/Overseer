""" Test whether users can log in """
from selenium.webdriver.common.keys import Keys
from ovs import app
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestLogin(SeleniumBaseTestCase):
    """ Test whether users can log in """

    def login_with_credentials(self, email, password):
        """ Logs in with the provided email and password """
        name_box = self.browser.find_element_by_name('email')
        name_box.send_keys(email)
        pass_box = self.browser.find_element_by_name('password')
        pass_box.send_keys(password)
        pass_box.send_keys(Keys.ENTER)

    def test_resident_login(self):
        """ Tests whether residents can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        self.login_with_credentials('resident@gmail.com', 'abcd1234')

        # Should be at resident greeting page
        self.assertIn('John', self.browser.title)

    def test_manager_login(self):
        """ Tests whether managers can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        self.login_with_credentials('admin@gmail.com', 'abcd1234')

        # Should be at manager greeting page
        self.assertIn(app.config['ADMIN']['first_name'], self.browser.title)

    def test_bad_login(self):
        """ Tests whether a random email can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        self.login_with_credentials('testtesttest@gmail.com', 'abcd1234')
        
        # Page should not have changed
        self.assertEqual('Overseer', self.browser.title)
