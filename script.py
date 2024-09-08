import random
import re
from playwright.sync_api import Playwright, sync_playwright, expect

def increase_quantity(page, times):
    for _ in range(times):
        page.get_by_role("button", name="Increase Quantity").click()

def fill_email(page, placeholder):
    random_number = random.randint(1, 1000)
    email = f"automation.user+{random_number}@ymail.com"
    page.get_by_placeholder(placeholder).fill(email)
    print(f"Filled email: {email}")

def test_mumzworld(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.mumzworld.com/")
    expect(page).to_have_title(re.compile("#1 Mother, Child & Baby Shop in the UAE - Mumzworld"))

    page.get_by_placeholder("What are you looking for?").click()
    page.get_by_placeholder("What are you looking for?").fill("bag")
    expect(page.locator('ol.algoliaSearchBar-items-2x3.algoliaHits-items-T8p')).to_be_visible()

    page.locator('ol.algoliaSearchBar-items-2x3.algoliaHits-items-T8p').first.click()
    expect(page.get_by_role("button", name="Add to Bag")).to_be_visible()

    page.get_by_role("button", name="Add to Bag").click()
    expect(page.locator('div.feedbackPopup-message-1GV')).to_contain_text("Successfully added to bag")

    page.get_by_role("link", name="View Bag").click()
    expect(page).to_have_url("https://www.mumzworld.com/en/cart")

    increase_quantity(page,4)
    expect(page.locator("input[name=quantity]").first).to_have_value("5")

    page.get_by_role("button", name="Proceed to Checkout").click()
    expect(page.locator('div.signIn-root-2yj')).to_contain_text("Sign in to your mumzworld account")

    page.get_by_role("button", name="Sign up").click()
    expect(page.locator('div.createAccountPage-contentContainer-hc_')).to_contain_text("Sign up to your mumzworld account")
    page.get_by_label("First Name").click()
    page.get_by_label("First Name").fill("tester")
    page.get_by_label("Last Name").click()
    page.get_by_label("Last Name").fill("user")
    page.get_by_placeholder("john.doe@address.com").click()
    fill_email(page,"john.doe@address.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("qwerty1234!")
    page.get_by_role("button", name="Register").click()
    expect(page.get_by_role("button", name="Place Order")).to_be_disabled()
    expect(page).to_have_url("https://www.mumzworld.com/en/checkout")

    context.close()
    browser.close()