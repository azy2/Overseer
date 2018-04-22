""" Base test class for tests related to responsive tables. """
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ovs.tests.selenium.selenium_base_test import SeleniumBaseTestCase


class TableTest(SeleniumBaseTestCase):
    """ Base test class for tests related to responsive tables. """

    # Subclasses should append to form_text_field_types in order from top to bottom with TableTextElements
    # Subclasses should also append to table_text_field_types with instances of TableTextElement
    #  corresponding to the type of the field at that index in the row, None disregards the field
    def setUp(self):
        super().setUp()
        self.form_text_field_types = []
        self.table_text_field_types = []

    def get_last_table_row(self):
        """ Gets a list of WebElements corresponding to the data for the last row in the table.

            Returns:
                List of WebElement: The last row in the table.
        """
        table = self.browser.find_element_by_class_name('table-responsive')
        last_table_row = table.find_elements_by_tag_name('tr')[-1]
        return last_table_row.find_elements_by_tag_name('td')

    def add_to_table(self, *args):
        """ Sets the text in the form based on *args and the order of self.form_text_field_types
             then adds the entry to the table.

            Args:
                args: The text to enter in the form fields.
        """
        form_fields = self.browser.find_elements_by_class_name('form-group')

        for i in range(len(self.form_text_field_types)):
            new_text = args[i]
            if new_text != None:
                field_type = self.form_text_field_types[i]
                field_type.set_text(form_fields[i], new_text)

        add_button = self.browser.find_element_by_class_name('btn-primary')
        add_button.click()

    def verify_last_row_fields_match(self, *args):
        """ Verifies that the fields in the last row of the table match *args left to right.

            Args:
                args: The text to verify left to right. None will skip over that field.

            Returns:
                boolean: True if all fields match expected values, False otherwise
        """
        last_row_elements = self.get_last_table_row()

        args_index = 0
        for i in range(len(self.table_text_field_types)):
            if self.table_text_field_types[i] is None:
                continue

            if args[args_index] != None:
                actual_text = self.table_text_field_types[i].get_text(last_row_elements[i])
                if actual_text != args[args_index]:
                    return False

            args_index += 1

        return True

    def set_last_row_fields(self, *args):
        """ Sets the fields in the last row of the table to *args from left to right.

            Args:
                args: The text to set the fields to from left to right.
                        None will skip setting that field to anything new.
        """
        last_row_elements = self.get_last_table_row()

        args_index = 0
        for i in range(len(self.table_text_field_types)):
            if self.table_text_field_types[i] is None:
                continue

            if args[args_index] != None:
                self.table_text_field_types[i].set_text(last_row_elements[i], args[args_index])

            args_index += 1

    def click_last_row_button_at_index(self, index):
        """ Clicks the button in the last row of the table at the passed in index.

            Args:
                index (int): The row index for the button to click.
        """
        last_table_row = self.get_last_table_row()
        update_button_holder = last_table_row[index]
        update_button = update_button_holder.find_element_by_class_name('btn-secondary')
        update_button.click()

    def click_update_last_row(self):
        """ Clicks the update button for the last row on the table. """
        # Update button is the first element in the row after the text fields
        self.click_last_row_button_at_index(len(self.table_text_field_types))

    def click_delete_last_row(self):
        """ Clicks the delete button for the last row on the table. """
        # Delete button is the second element in the row after the text fields
        self.click_last_row_button_at_index(len(self.table_text_field_types) + 1)

    def navigate_to_table_page(self):
        """ Subclasses need to override this to get to the page with the corresponding table.
            Assumes that the page is currently reachable using the menu bar at the top. """
        pass

    def add_table_test(self, *args):
        """ Tests that *args can be added to the table through the form correctly.

            Args:
                args: The text to put in the form from top to bottom.
        """
        self.browser.get(self.base_url)
        self.assertIn('Overseer', self.browser.title)
        super().login_default_admin()

        # Go to the page with the table and add an entry to it
        self.navigate_to_table_page()
        self.add_to_table(*args)

        # Wait for successful add notification
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.visibility_of_element_located((By.ID, 'notification-message')))

        self.assertTrue(self.verify_last_row_fields_match(*args))

    def update_delete_table_test(self, *args):
        """ Tests that the table can be updated with *args from left to right.
            Also tests that rows can be deleted from the table.

            Args:
                args: The text to update in the table from left to right.
        """
        # Assumes that the last row in the table already exists and that we are on the table page
        # Verify that changing fields without pressing 'Update' does not change anything
        self.set_last_row_fields(*args)
        self.navigate_to_table_page()

        # Update the text and verify that it changes
        self.set_last_row_fields(*args)
        self.click_update_last_row()
        self.navigate_to_table_page()
        self.assertTrue(self.verify_last_row_fields_match(*args))

        # Delete the row and verify table has one less row
        # Changing the page like this makes old references stale, so table must be found again
        table = self.browser.find_element_by_class_name('table-responsive')
        num_rows = len(table.find_elements_by_tag_name('tr'))
        self.click_delete_last_row()
        table = self.browser.find_element_by_class_name('table-responsive')
        self.assertEqual(num_rows - 1, len(table.find_elements_by_tag_name('tr')))

class RowTextElement:
    """ Represents a WebElement that contains a text element in a row of the table. """

    def get_text(self, table_element):
        """ Gets the text from the passed in WebElement of the corresponding type.

            Args:
                table_element (WebElement): The element of this type to get the text from.
        """
        pass

    def set_text(self, table_element, new_text):
        """ Sets the text on the passed in WebElement.

            Args:
                table_element (WebElement): The element of this type to set the text for.
                new_text (string): What to set the text to.
        """
        pass

class PlainTextElement(RowTextElement):
    """ Plain text elements that cannot be modified. """

    def get_text(self, table_element):
        """ Same as parent base class.

            Args:
                table_element (WebElement): The element of this type to get the text from.

            Returns:
                string: the text on the element.
        """

        return table_element.text

class InputTextElement(RowTextElement):
    """ Text fields that can be modified. """

    def get_text(self, table_element):
        """ Same as parent base class.

            Args:
                table_element (WebElement): The element of this type to get the text from.

            Returns:
                string: the text on the element.
        """
        # All non-plain-text text fields in table currently have 'form-control' class name
        return table_element.find_element_by_class_name('form-control').get_attribute('value')

    def set_text(self, table_element, new_text):
        """ Same as parent base class.

            Args:
                table_element (WebElement): The element of this type to set the text for.
                new_text (string): What to set the text to.
        """
        text_field = table_element.find_element_by_class_name('form-control')
        text_field.clear()
        text_field.send_keys(new_text)

class SelectTextElement(RowTextElement):
    """ Text fields that are a dropdown selector for a few text options. """

    def get_text(self, table_element):
        """ Same as parent base class.

            Args:
                table_element (WebElement): The element of this type to get the text from.

            Returns:
                string: the text on the element.
        """
        text_selector = Select(table_element.find_element_by_class_name('form-control'))
        return text_selector.first_selected_option.text

    def set_text(self, table_element, new_text):
        """ Same as parent base class.

            Args:
                table_element (WebElement): The element of this type to set the text for.
                new_text (string): What to set the text to.
        """
        text_selector = Select(table_element.find_element_by_class_name('form-control'))
        text_selector.select_by_visible_text(new_text)
