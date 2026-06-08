from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to URL with load wait"""
        self.page.goto(url)
        self.page.wait_for_load_state('load')

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_element(self, locator: str, timeout: int = 10000):
        """Explicit wait for visibility"""
        self.page.wait_for_selector(locator, timeout=timeout, state='visible')

    def click_element(self, locator: str):
        self.page.locator(locator).click()

    def fill_element(self, locator: str, text: str):
        self.page.locator(locator).fill(text)

    def get_element_text(self, locator: str) -> str:
        return self.page.locator(locator).text_content() or ""

    def is_element_visible(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()
