import allure
import pytest
from allure_commons.types import Severity
from playwright.sync_api import Page

from pages.saucedemo import LoginPage

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"


@allure.epic("Practice sites")
@allure.feature("SauceDemo: Shop")
@allure.link(LoginPage.url, name="SauceDemo")
@allure.label("owner", "nika.zhordania")
class TestSauceDemo:
    @pytest.fixture(autouse=True)
    def login_page(self, page: Page) -> LoginPage:
        return LoginPage(page).open()

    @allure.story("Login")
    @allure.title("TC-01: standard_user sees the product list")
    @allure.severity(Severity.BLOCKER)
    @allure.tag("smoke", "positive")
    def test_tc01_standard_user_login(self, login_page: LoginPage):
        inventory = login_page.login("standard_user")
        inventory.expect_opened()
        inventory.screenshot("Products page")

    @allure.story("Login")
    @allure.title("TC-02: locked_out_user is rejected")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative")
    def test_tc02_locked_out_user(self, login_page: LoginPage):
        login_page.login("locked_out_user")
        login_page.expect_error("Epic sadface: Sorry, this user has been locked out.")
        login_page.screenshot("Locked out user")

    @allure.story("Login")
    @allure.title("TC-03: Empty username shows 'Username is required'")
    @allure.severity(Severity.NORMAL)
    @allure.tag("negative")
    def test_tc03_empty_username(self, login_page: LoginPage):
        login_page.login("", "")
        login_page.expect_error("Epic sadface: Username is required")
        login_page.screenshot("Empty username")

    @allure.story("Login")
    @allure.title("TC-04: Wrong password is rejected")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative")
    def test_tc04_wrong_password(self, login_page: LoginPage):
        login_page.login("standard_user", "wrong_password")
        login_page.expect_error(
            "Epic sadface: Username and password do not match any user in this service"
        )
        login_page.screenshot("Wrong password")

    @allure.story("Cart")
    @allure.title("TC-05: Adding 2 items sets the cart badge to 2")
    @allure.severity(Severity.NORMAL)
    @allure.tag("positive", "cart")
    def test_tc05_add_two_items(self, login_page: LoginPage):
        inventory = login_page.login("standard_user")
        inventory.add_to_cart(BACKPACK)
        inventory.add_to_cart(BIKE_LIGHT)
        inventory.expect_cart_count(2)
        inventory.screenshot("Cart badge")

    @allure.story("Checkout")
    @allure.title("TC-06: Checkout without First Name is rejected")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative", "checkout")
    def test_tc06_checkout_empty_first_name(self, login_page: LoginPage):
        inventory = login_page.login("standard_user")
        inventory.add_to_cart(BACKPACK)
        checkout = inventory.open_cart().checkout()
        checkout.fill_info("", "Test", "12345")
        checkout.expect_error("Error: First Name is required")
        checkout.screenshot("Empty first name")

    @allure.story("Checkout")
    @allure.title("TC-07: Full checkout completes the order")
    @allure.severity(Severity.BLOCKER)
    @allure.tag("smoke", "positive", "checkout")
    def test_tc07_full_checkout(self, login_page: LoginPage):
        inventory = login_page.login("standard_user")
        inventory.add_to_cart(BACKPACK)
        checkout = inventory.open_cart().checkout()
        checkout.fill_info("Anna", "Test", "12345")
        checkout.finish()
        checkout.expect_order_complete()
        checkout.screenshot("Order complete")
