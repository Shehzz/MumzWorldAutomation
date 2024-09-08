import random
from playwright.sync_api import expect

class MumzworldAutomation:
    def __init__(self, page):
        self.page = page

    def search_product(self, product_name):
        self.page.get_by_placeholder("What are you looking for?").click()
        self.page.get_by_placeholder("What are you looking for?").fill(product_name)
        expect(self.page.locator('ol.algoliaSearchBar-items-2x3.algoliaHits-items-T8p')).to_be_visible()
        self.page.locator('ol.algoliaSearchBar-items-2x3.algoliaHits-items-T8p').first.click()
        expect(self.page.get_by_role("button", name="Add to Bag")).to_be_visible()

    def add_to_bag(self):
        self.page.get_by_role("button", name="Add to Bag").click()
        expect(self.page.locator('div.feedbackPopup-message-1GV')).to_contain_text("Successfully added to bag")
        self.page.get_by_role("link", name="View Bag").click()
        expect(self.page).to_have_url("https://www.mumzworld.com/en/cart")

    def increase_quantity(self, times):
        for _ in range(times):
            self.page.get_by_role("button", name="Increase Quantity").click()
        expect(self.page.locator("input[name=quantity]").first).to_have_value("5")
        expect(self.page.locator("span.cartItemsQty-rootWithoutVerticalPadding-cwC")).to_have_text("5 items")

    def proceed_to_checkout(self):
        self.page.get_by_role("button", name="Proceed to Checkout").click()
        expect(self.page.locator('div.signIn-root-2yj')).to_contain_text("Sign in to your mumzworld account")
        self.page.get_by_role("button", name="Sign up").click()
        expect(self.page.locator('div.createAccountPage-contentContainer-hc_')).to_contain_text("Sign up to your mumzworld account")

    def fill_email(self, placeholder):
            random_number = random.randint(1, 2000)
            email = f"automation.user+{random_number}@ymail.com"
            self.page.get_by_placeholder(placeholder).fill(email)
            print(f"Filled email: {email}")

    def sign_up(self, first_name, last_name, email_placeholder, password):
        self.page.get_by_label("First Name").click()
        self.page.get_by_label("First Name").fill(first_name)
        self.page.get_by_label("Last Name").click()
        self.page.get_by_label("Last Name").fill(last_name)
        self.page.get_by_placeholder("john.doe@address.com").click()
        self.fill_email(email_placeholder)
        self.page.get_by_label("Password").click()
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Register").click()
        expect(self.page.get_by_role("button", name="Place Order")).to_be_disabled()
        expect(self.page).to_have_url("https://www.mumzworld.com/en/checkout")
