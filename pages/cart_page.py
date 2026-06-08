from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators for SauceDemo cart
        self.checkout_button = "[data-test='checkout']"
        self.cart_item = ".cart_item"
        self.cart_list = ".cart_list"

    def wait_for_cart_load(self):
        """Wait for cart page to fully load"""
        expect(self.page.locator(self.cart_list)).to_be_visible(timeout=10000)

    def verify_item_in_cart(self) -> bool:
        """Verify that item is in cart"""
        return self.page.locator(self.cart_item).is_visible()

    def proceed_to_checkout(self):
        """Click checkout button to proceed to checkout"""
        expect(self.page.locator(self.checkout_button)).to_be_visible()
        self.page.locator(self.checkout_button).click()
        self.page.wait_for_load_state('networkidle')
        print("  ✓ Proceeded to checkout")
