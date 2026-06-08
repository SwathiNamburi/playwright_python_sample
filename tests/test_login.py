import allure
import yaml
from pathlib import Path
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.common import read_test_data, take_screenshot

# Load config
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

test_data = read_test_data("testdata/test_data.json")


@allure.feature("SauceDemo Login")
@allure.story("Valid Login")
def test_valid_login(page):
    """Test valid login - verify user can login and access inventory page"""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Navigate to SauceDemo login page"):
        login_page.navigate_to(config['base_url'])
        print("✓ Navigated to SauceDemo login page")

    with allure.step("Login with valid credentials"):
        login_page.login(
            test_data['valid_credentials']['username'],
            test_data['valid_credentials']['password']
        )
        print("✓ Login successful")
        allure.attach("Login Action", "User logged in with valid credentials", allure.attachment_type.TEXT)

    with allure.step("Verify inventory page is loaded"):
        inventory_page.wait_for_inventory_load()
        print("✓ Inventory page loaded after login")

        # Verify URL contains inventory
        assert "inventory" in page.url, "Should redirect to inventory page"
        print("✓ URL verified: User redirected to inventory page")
        allure.attach("Login Success", "User successfully logged in and redirected to inventory page",
                      allure.attachment_type.TEXT)

    with allure.step("Capture login success screenshot"):
        take_screenshot(page, "saucedemo_valid_login_success")
        screenshot = page.screenshot()
        allure.attach(screenshot, "Login_Success_Screenshot", allure.attachment_type.PNG)
        print("✓ Screenshot captured")


@allure.feature("SauceDemo Login")
@allure.story("Invalid Login")
def test_invalid_login(page):
    """Test invalid login - verify error message is displayed for invalid credentials"""
    login_page = LoginPage(page)

    with allure.step("Navigate to SauceDemo login page"):
        login_page.navigate_to(config['base_url'])
        print("✓ Navigated to SauceDemo login page")

    with allure.step("Attempt login with invalid credentials"):
        login_page.login(
            test_data['invalid_credentials']['username'],
            test_data['invalid_credentials']['password']
        )
        print("✓ Login attempted with invalid credentials")

    with allure.step("Verify error message is displayed"):
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_msg = login_page.get_error_message()
        print(f"✓ Error message displayed: {error_msg}")

        # Verify error contains expected text
        assert "Epic sadface" in error_msg, "Error should indicate invalid credentials"
        print("✓ Error message verified: Contains 'Epic sadface'")
        allure.attach("Login Error", f"Error message: {error_msg}", allure.attachment_type.TEXT)

    with allure.step("Capture error screenshot"):
        take_screenshot(page, "saucedemo_invalid_login_error")
        screenshot = page.screenshot()
        allure.attach(screenshot, "Invalid_Login_Error_Screenshot", allure.attachment_type.PNG)
        print("✓ Error screenshot captured")
