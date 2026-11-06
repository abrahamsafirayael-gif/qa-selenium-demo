from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def item_names(self):
        self.wait_for_url_contains("cart")
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))
