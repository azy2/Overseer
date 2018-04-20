""" Test functionality related to logging in and out. """
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestLogin(SeleniumBaseTestCase):
    """ Tests functionality related to logging in and out. """

    def test_resident_login(self):
        """ Tests whether residents can log in. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_resident()

        # Should be at resident greeting page
        self.assertIn(self.default_resident_name, self.browser.title)

    def test_resident_logout(self):
        """ Tests whether residents can log out. """
        self.test_resident_login()

        # Use dropdown with logout link option
        self.go_to_page_in_dropdown('Logout', 'accountDropdown')

        # Should be back at Overseer home page
        self.assertIn('Overseer', self.browser.title)

    def test_manager_login(self):
        """ Tests whether managers can log in. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Should be at manager greeting page
        self.assertIn(self.default_admin_name, self.browser.title)

    def test_bad_login(self):
        """ Tests whether a random email can log in. """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_with_credentials('testtesttest@gmail.com', 'password_goes_here')

        # Page should not have changed
        self.assertEqual('Overseer', self.browser.title)
