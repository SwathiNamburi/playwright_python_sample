import allure
import yaml
from pathlib import Path
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.common import read_test_data, take_screenshot

# Load config
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

test_data = read_test_data("testdata/test_data.json")

@allure.feature("SauceDemo Shopping")
@allure.story("Full Purchase Flow - Login, Sort, Add to Cart, Checkout")
def test_saucedemo_full_flow(page):
    """
    Complete SauceDemo purchase test flow:
    1. Login with valid credentials
    2. Sort products by price low to high
    3. Add first (cheapest) item to cart
    4. Go to cart
    5. Proceed to checkout
    6. Fill checkout details
    7. Complete order
    """
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    checkout_details = test_data['checkout_details']

    with allure.step("Navigate to SauceDemo login page"):
        login_page.navigate_to(config['base_url'])
        print("Navigated to SauceDemo login page")

    with allure.step("Login with valid credentials (standard_user)"):
        login_page.login(
            test_data['valid_credentials']['username'],
            test_data['valid_credentials']['password']
        )
        print("Login successful")
        allure.attach("Login Success", "User successfully logged in to SauceDemo", allure.attachment_type.TEXT)

    with allure.step("Wait for inventory page to load"):
        inventory_page.wait_for_inventory_load()
        # Additional stabilization
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)

        print("Inventory page loaded")

    with allure.step("Sort products by price - low to high"):
        inventory_page.sort_by_price_low_to_high()
        print("Products sorted by price (low to high)")
        allure.attach("Sort Action", "Products sorted by price from low to high", allure.attachment_type.TEXT)

    with allure.step("Add first (cheapest) item to cart"):
        inventory_page.add_first_item_to_cart()
        print("First item added to cart")
        allure.attach("Add to Cart", "First item successfully added to cart", allure.attachment_type.TEXT)

    with allure.step("Navigate to shopping cart"):
        inventory_page.go_to_cart()
        print("Navigated to cart")
        allure.attach("Cart Navigation", "Proceeded to shopping cart", allure.attachment_type.TEXT)

    with allure.step("Verify item is in cart"):
        cart_page.wait_for_cart_load()
        assert cart_page.verify_item_in_cart(), "Item should be present in cart"
        print("Item verified in cart")

    with allure.step("Proceed to checkout"):
        cart_page.proceed_to_checkout()
        print("Checkout initiated")
        allure.attach("Checkout Initiated", "Proceeded from cart to checkout", allure.attachment_type.TEXT)

    with allure.step("Wait for checkout page to load"):
        checkout_page.wait_for_checkout_page_load()
        print("Checkout page loaded")

    with allure.step("Fill checkout details"):
        checkout_page.fill_checkout_details(
            checkout_details['first_name'],
            checkout_details['last_name'],
            checkout_details['zip_code']
        )
        print("Checkout details filled")
        allure.attach(
            "Checkout Details",
            f"First Name: {checkout_details['first_name']}, Last Name: {checkout_details['last_name']}, Zip Code: {checkout_details['zip_code']}",
            allure.attachment_type.TEXT
        )

    with allure.step("Complete order"):
        checkout_page.complete_order()
        print("Order completed")
        allure.attach("Order Completed", "Order placed successfully", allure.attachment_type.TEXT)

    with allure.step("Verify order completion"):
        expect(page.locator(checkout_page.confirmation_message)).to_be_visible()
        assert checkout_page.is_order_complete(), "Order should be complete"
        confirmation_msg = checkout_page.get_confirmation_message()
        print(f"Order verification successful - {confirmation_msg}")
        allure.attach("Confirmation Message", confirmation_msg, allure.attachment_type.TEXT)

    with allure.step("Capture order confirmation screenshot"):
        take_screenshot(page, "saucedemo_order_confirmation")
        screenshot = page.screenshot()
        allure.attach(screenshot, "Order_Confirmation_Screenshot", allure.attachment_type.PNG)
        print("Screenshot captured")

