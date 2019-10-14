from unittest import skip
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request and does not load the list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'
            ))

        # She tries adding some text for the item, and the error disappears
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'
            ))

        # and she can submit it successfully
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Once again the browser will not comply
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'
            ))

        # And she can correct it by filling some text in
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Make tea")
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'
            ))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")

    def test_cannot_add_duplicate_items(self):
        # A user goes to the homepage and starts a new list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy wellies")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy wellies")

        # they accidentally enter an item again
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy wellies")
        inputbox.send_keys(Keys.ENTER)

        # . . . and get a helpful error message
        self.wait_for(lambda: self.assertEqual(
                self.get_error_element().text,
                "You've already got this in your list"
            ))

    def test_errors_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        self.get_item_input_box().send_keys('a')

        # error message disappears when text is entered
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
