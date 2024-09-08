import re
from playwright.sync_api import Playwright, sync_playwright, expect
from automation_methods import MumzworldAutomation  # Import the class

def test_checkout(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    automation = MumzworldAutomation(page)

    page.goto("https://www.mumzworld.com/")

    automation.search_product("bag")
    automation.add_to_bag()
    automation.increase_quantity(4)
    automation.proceed_to_checkout()
    automation.sign_up("automation", "tester", "john.doe@address.com", "qwerty1234!")

    context.close()
    browser.close()
