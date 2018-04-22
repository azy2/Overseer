""" Test functionality related to registering managers. """
from ovs.tests.selenium.table_test import TableTest, InputTextElement, SelectTextElement

class TestRegisterManager(TableTest):
    """ Test functionality related to registering managers. """

    def setUp(self):
        super().setUp()
        # Current form format: [Email][First Name][Last Name][Role Selector]
        self.form_text_field_types.append(InputTextElement())
        self.form_text_field_types.append(InputTextElement())
        self.form_text_field_types.append(InputTextElement())
        self.form_text_field_types.append(SelectTextElement())

        # Current table format: [Email][First Name][Last Name][Role Selector]
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(InputTextElement())
        self.table_text_field_types.append(SelectTextElement())

    def navigate_to_table_page(self):
        self.browser.find_element_by_link_text('Managers').click()

    def test_register_manager(self):
        """ Tests whether a manager can be registered. """
        self.add_table_test('email@website.net', 'John', 'Smith', 'Office Manager')

    def test_update_delete_manager(self):
        """ Tests that newly added managers can be updated and deleted. """
        self.test_register_manager()
        self.update_delete_table_test('mail@websight.net', 'Jack', 'Smithers', 'Staff')
