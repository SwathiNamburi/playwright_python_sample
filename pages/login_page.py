from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators for SauceDemo
        self.username_input = "[data-test='username']"
        self.password_input = "[data-test='password']"
        self.login_button = "[data-test='login-button']"
        self.error_message = "[data-test='error']"

    def login(self, username: str, password: str):
        """Perform login with explicit waits"""
        expect(self.page.locator(self.username_input)).to_be_visible()
        self.page.locator(self.username_input).fill(username)
        self.page.locator(self.password_input).fill(password)
        self.page.locator(self.login_button).click()
        self.page.wait_for_load_state('networkidle')

    def get_error_message(self) -> str:
        """Get error text"""
        return self.page.locator(self.error_message).text_content() or ""

    def is_error_displayed(self) -> bool:
        """Check if error is visible with explicit wait"""
        try:
            expect(self.page.locator(self.error_message)).to_be_visible(timeout=10000)
            return True
        except:
            return False
