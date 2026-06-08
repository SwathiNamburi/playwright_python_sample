import logging
import json
from pathlib import Path
from playwright.sync_api import Page, Locator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_logging(log_file: str = "reports/test.log"):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

def wait_for_element(page: Page, locator: str, timeout=10000):
    """Wait for element to be visible"""
    page.wait_for_selector(locator, timeout=timeout, state='visible')

def clear_field(page: Page, locator: str):
    """Clear input field"""
    page.locator(locator).fill("")

def take_screenshot(page: Page, name: str):
    """Take and save screenshot"""
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    page.screenshot(path=f"reports/screenshots/{name}.png")

def read_test_data(file_path: str) -> dict:
    """Read test data from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

# Assertion methods using Playwright locators
def assert_element_visible(page: Page, locator: str, message: str = ""):
    """Assert that element is visible"""
    element = page.locator(locator)
    assert element.is_visible(), f"Element not visible: {message}"
    logger.info(f"✓ Element visible: {message}")

def assert_element_text(page: Page, locator: str, expected_text: str, message: str = ""):
    """Assert element contains text"""
    element = page.locator(locator)
    actual_text = element.text_content() or ""
    assert expected_text in actual_text, f"Expected text '{expected_text}' not found in '{actual_text}'. {message}"
    logger.info(f"✓ Text assertion passed: {message}")

def assert_element_count(page: Page, locator: str, expected_count: int, message: str = ""):
    """Assert element count"""
    elements = page.locator(locator)
    count = elements.count()
    assert count == expected_count, f"Expected {expected_count} elements but found {count}. {message}"
    logger.info(f"✓ Element count assertion passed: {message}")

def assert_url_contains(page: Page, url_fragment: str, message: str = ""):
    """Assert URL contains fragment"""
    assert url_fragment in page.url, f"Expected URL to contain '{url_fragment}' but got '{page.url}'. {message}"
    logger.info(f"✓ URL assertion passed: {message}")

def assert_input_value(page: Page, locator: str, expected_value: str, message: str = ""):
    """Assert input field value"""
    element = page.locator(locator)
    actual_value = element.input_value() or ""
    assert actual_value == expected_value, f"Expected '{expected_value}' but got '{actual_value}'. {message}"
    logger.info(f"✓ Input value assertion passed: {message}")
