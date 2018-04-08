""" Test whether users can log in """
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestLogin(SeleniumBaseTestCase):
    """ Test whether users can log in """

    def test_resident_login(self):
        """ Tests whether residents can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        default_resident_email = current_app.config['RESIDENT']['email']
        default_resident_password = current_app.config['RESIDENT']['password']
        super().login_with_credentials(default_resident_email, default_resident_password)

        # Should be at resident greeting page
        default_resident_name = current_app.config['RESIDENT']['first_name']
        self.assertIn(default_resident_name, self.browser.title)

    def test_resident_logout(self):
        """ Tests whether residents can log out or not """
        self.test_resident_login()

        # Open dropdown with logout link option
        account_dropdown = self.browser.find_element_by_id('accountDropdown')
        account_dropdown.click()
        logout_link = self.browser.find_element_by_link_text('Logout')
        logout_link.click()

        # Should be back at Overseer home page
        self.assertIn('Overseer', self.browser.title)

    def test_manager_login(self):
        """ Tests whether managers can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        default_admin_email = current_app.config['ADMIN']['email']
        default_admin_password = current_app.config['ADMIN']['password']
        super().login_with_credentials(default_admin_email, default_admin_password)

        # Should be at manager greeting page
        default_admin_name = current_app.config['ADMIN']['first_name']
        self.assertIn(default_admin_name, self.browser.title)

    def test_bad_login(self):
        """ Tests whether a random email can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        super().login_with_credentials('testtesttest@gmail.com', 'password_goes_here')

        # Page should not have changed
        self.assertEqual('Overseer', self.browser.title)
