from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators for SauceDemo inventory
        self.sort_dropdown = "[data-test='product-sort-container']"
        self.inventory_items = ".inventory_item"
        self.add_to_cart_buttons = ".btn_inventory"
        self.cart_icon = ".shopping_cart_link"
        self.inventory_container = ".inventory_container"

    def wait_for_inventory_load(self):
        """Wait for inventory page to fully load and ensure top elements are visible"""
        expect(self.page.locator(self.inventory_container)).to_be_visible(timeout=10000)

        # Take initial screenshot
        self.page.screenshot(path="reports/debug_initial.png")

        # Scroll to top to ensure all top elements are visible
        self.page.evaluate("window.scrollTo(0, 0)")

        # Wait for scroll to complete and page to stabilize
        self.page.wait_for_timeout(1000)

        # Take screenshot after scroll
        self.page.screenshot(path="reports/debug_after_scroll.png")

        # Check if sort dropdown is visible
        sort_visible = self.page.locator(self.sort_dropdown).is_visible()
        print(f"  DEBUG: Sort dropdown visible after scroll: {sort_visible}")

        # Additional wait to ensure no auto-scroll happens
        self.page.wait_for_load_state('networkidle')

        print("  ✓ Inventory page loaded and stabilized at top")

    def sort_by_price_low_to_high(self):
        """Sort products by price low to high with enhanced visibility checks"""
        # Wait for the sort dropdown to be attached
        self.page.wait_for_selector(self.sort_dropdown, state='attached', timeout=10000)

        # Ensure we're at the top of the page
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(500)

        # Scroll the sort dropdown into view
        sort_locator = self.page.locator(self.sort_dropdown)
        sort_locator.scroll_into_view_if_needed()

        # Wait for it to be visible and stable
        self.page.wait_for_selector(self.sort_dropdown, state='visible', timeout=5000)

        # Double-check visibility
        if not sort_locator.is_visible():
            self.page.wait_for_timeout(1000)  # Wait a bit more
            sort_locator.scroll_into_view_if_needed()

        # Now select the option
        sort_locator.select_option("lohi")
        self.page.wait_for_load_state('networkidle')
        print("  ✓ Products sorted by price (low to high)")

    def add_first_item_to_cart(self):
        """Add the first (cheapest) item to cart after sorting"""
        expect(self.page.locator(self.inventory_items).first).to_be_visible()
        # Get the first product's "Add to Cart" button
        self.page.locator(self.add_to_cart_buttons).first.click()
        print("  ✓ First item added to cart")

    def go_to_cart(self):
        """Navigate to cart"""
        expect(self.page.locator(self.cart_icon)).to_be_visible()
        self.page.locator(self.cart_icon).click()
        self.page.wait_for_load_state('networkidle')
        print("  ✓ Navigated to cart")
