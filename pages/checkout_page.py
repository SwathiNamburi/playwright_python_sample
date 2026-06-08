from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators for SauceDemo checkout
        self.first_name_input = "[data-test='firstName']"
        self.last_name_input = "[data-test='lastName']"
        self.zip_code_input = "[data-test='postalCode']"
        self.continue_button = "[data-test='continue']"
        self.finish_button = "[data-test='finish']"
        self.confirmation_message = ".complete-header"
        self.checkout_info_container = ".checkout_info_container"

    def wait_for_checkout_page_load(self):
        """Wait for checkout page to fully load"""
        expect(self.page.locator(self.checkout_info_container)).to_be_visible(timeout=10000)

    def fill_checkout_details(self, first_name: str, last_name: str, zip_code: str):
        """Fill all checkout details on step one"""
        expect(self.page.locator(self.first_name_input)).to_be_visible()
        self.page.locator(self.first_name_input).fill(first_name)
        print(f"  ✓ First name filled: {first_name}")

        self.page.locator(self.last_name_input).fill(last_name)
        print(f"  ✓ Last name filled: {last_name}")

        self.page.locator(self.zip_code_input).fill(zip_code)
        print(f"  ✓ Zip code filled: {zip_code}")

        self.page.locator(self.continue_button).click()
        self.page.wait_for_load_state('networkidle')
        print("  ✓ Continue button clicked")

    def complete_order(self):
        """Click finish button to complete order"""
        expect(self.page.locator(self.finish_button)).to_be_visible()
        self.page.locator(self.finish_button).click()
        self.page.wait_for_load_state('networkidle')
        print("  ✓ Order completed")

    def is_order_complete(self) -> bool:
        """Verify order completion by checking confirmation message"""
        return self.page.locator(self.confirmation_message).is_visible()

    def get_confirmation_message(self) -> str:
        """Get the order confirmation message"""
        return self.page.locator(self.confirmation_message).text_content() or ""
