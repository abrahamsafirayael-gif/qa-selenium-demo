from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "inventory_item")
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_SELECT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def title(self):
        return self.text_of(self.TITLE)

    def item_count(self):
        return len(self.find_all(self.ITEMS))

    def add_backpack(self):
        self.click(self.ADD_BACKPACK)

    def add_bike_light(self):
        self.click(self.ADD_BIKE_LIGHT)

    def remove_backpack(self):
        self.click(self.REMOVE_BACKPACK)

    def cart_count(self):
        """Devuelve la cantidad en el badge del carrito (0 si no hay badge)."""
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def sort_by(self, value):
        """value: az, za, lohi, hilo"""
        from selenium.webdriver.support.ui import Select

        Select(self.find(self.SORT_SELECT)).select_by_value(value)

    def prices(self):
        return [
            float(el.text.replace("$", ""))
            for el in self.find_all(self.ITEM_PRICES)
        ]

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
