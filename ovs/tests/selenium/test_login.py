""" Test whether users can log in """
from flask import current_app
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase

class TestLogin(SeleniumBaseTestCase):
    """ Test whether users can log in """

    def test_resident_login(self):
        """ Tests whether residents can log in or not """
        from ovs.datagen import DataGen
        DataGen.create_defaults()

        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        super().login_with_credentials('resident@gmail.com', 'abcd1234')

        # Should be at resident greeting page
        self.assertIn('John', self.browser.title)

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

    #def test_manager_login(self):
    #    """ Tests whether managers can log in or not """
    #    from ovs.datagen import DataGen
    #    DataGen.create_defaults()

    #    self.browser.get(self.base_url)
    #    self.assertIn('Overseer', self.browser.title)

    #    super().login_with_credentials('admin@gmail.com', 'abcd1234')

    #    # Should be at manager greeting page
    #    self.assertIn(current_app.config['ADMIN']['first_name'], self.browser.title)

    def test_bad_login(self):
        """ Tests whether a random email can log in or not """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)

        super().login_with_credentials('testtesttest@gmail.com', 'abcd1234')

        # Page should not have changed
        self.assertEqual('Overseer', self.browser.title)
