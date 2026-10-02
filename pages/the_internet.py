import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage

BASE_URL = "https://the-internet.herokuapp.com"


class LoginPage(BasePage):
    url = f"{BASE_URL}/login"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Login")
        self.flash = page.locator("#flash")

    @allure.step("Login as '{username}' / '{password}'")
    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    @allure.step("Verify message contains: {text}")
    def expect_message(self, text: str) -> None:
        expect(self.flash).to_contain_text(text)


class SecurePage(BasePage):
    url = f"{BASE_URL}/secure"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logout_link = page.get_by_role("link", name="Logout")

    @allure.step("Click Logout")
    def logout(self) -> LoginPage:
        self.logout_link.click()
        return LoginPage(self.page)
