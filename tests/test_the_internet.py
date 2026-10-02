import allure
import pytest
from allure_commons.types import Severity
from playwright.sync_api import Page

from pages.the_internet import BASE_URL, LoginPage, SecurePage

VALID_USER = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"


@allure.epic("Practice sites")
@allure.feature("The Internet: Login form")
@allure.link(LoginPage.url, name="Login page")
@allure.label("owner", "nika.zhordania")
class TestTheInternetLogin:
    @pytest.fixture(autouse=True)
    def login_page(self, page: Page) -> LoginPage:
        return LoginPage(page).open()

    @allure.story("Positive")
    @allure.title("TC-01: Valid credentials open the secure area")
    @allure.severity(Severity.BLOCKER)
    @allure.tag("smoke", "positive")
    def test_tc01_valid_login(self, login_page: LoginPage):
        login_page.login(VALID_USER, VALID_PASSWORD)
        login_page.expect_url(f"{BASE_URL}/secure")
        login_page.expect_message("You logged into a secure area!")
        login_page.screenshot("Secure area")

    @allure.story("Negative")
    @allure.title("TC-02: Wrong password shows an error and stays on /login")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative")
    def test_tc02_wrong_password(self, login_page: LoginPage):
        login_page.login(VALID_USER, "wrong123")
        login_page.expect_message("Your password is invalid!")
        login_page.expect_url(LoginPage.url)
        login_page.screenshot("Wrong password")

    @allure.story("Negative")
    @allure.title("TC-03: Unknown username shows 'username is invalid'")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative")
    @allure.description(
        "The message reveals which field is wrong (user enumeration). "
        "Discussion point: is this a security bug?"
    )
    def test_tc03_wrong_username(self, login_page: LoginPage):
        login_page.login("anna", VALID_PASSWORD)
        login_page.expect_message("Your username is invalid!")
        login_page.screenshot("Wrong username")

    @allure.story("Negative")
    @allure.title("TC-04: Empty fields show 'username is invalid'")
    @allure.severity(Severity.NORMAL)
    @allure.tag("negative")
    def test_tc04_empty_fields(self, login_page: LoginPage):
        login_page.login("", "")
        login_page.expect_message("Your username is invalid!")
        login_page.screenshot("Empty fields")

    @allure.story("Boundary")
    @allure.title("TC-05: Username surrounded by spaces is not trimmed")
    @allure.severity(Severity.MINOR)
    @allure.tag("boundary")
    @allure.description(
        "Records the observed behaviour: leading/trailing spaces are NOT trimmed, "
        "so the login is rejected. A question for the analyst: is that intended?"
    )
    def test_tc05_username_with_spaces(self, login_page: LoginPage):
        login_page.login(f" {VALID_USER} ", VALID_PASSWORD)
        login_page.expect_message("Your username is invalid!")
        login_page.expect_url(LoginPage.url)
        login_page.screenshot("Username with spaces")

    @allure.story("Positive")
    @allure.title("TC-06: Logout ends the session and /secure becomes unavailable")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("positive")
    def test_tc06_logout(self, page: Page, login_page: LoginPage):
        login_page.login(VALID_USER, VALID_PASSWORD)
        login_page = SecurePage(page).logout()
        login_page.expect_message("You logged out of the secure area!")
        login_page.expect_url(LoginPage.url)

        SecurePage(page).open()
        login_page.expect_url(LoginPage.url)
        login_page.expect_message("You must login to view the secure area!")
        login_page.screenshot("After logout")
