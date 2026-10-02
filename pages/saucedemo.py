import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage

BASE_URL = "https://www.saucedemo.com/"


def _by_test(page: Page, name: str):
    return page.locator(f"[data-test='{name}']")


class LoginPage(BasePage):
    url = BASE_URL
    PASSWORD = "secret_sauce"

    def __init__(self, page: Page):
        super().__init__(page)
        self.error = _by_test(page, "error")

    @allure.step("Login as '{username}'")
    def login(self, username: str, password: str = PASSWORD) -> "InventoryPage":
        _by_test(self.page, "username").fill(username)
        _by_test(self.page, "password").fill(password)
        _by_test(self.page, "login-button").click()
        return InventoryPage(self.page)

    @allure.step("Verify error: {text}")
    def expect_error(self, text: str) -> None:
        expect(self.error).to_have_text(text)


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = _by_test(page, "title")
        self.items = _by_test(page, "inventory-item")
        self.cart_badge = _by_test(page, "shopping-cart-badge")

    @allure.step("Add to cart: {product_id}")
    def add_to_cart(self, product_id: str) -> None:
        _by_test(self.page, f"add-to-cart-{product_id}").click()

    @allure.step("Open the cart")
    def open_cart(self) -> "CartPage":
        _by_test(self.page, "shopping-cart-link").click()
        return CartPage(self.page)

    @allure.step("Verify the Products page is displayed")
    def expect_opened(self) -> None:
        expect(self.title).to_have_text("Products")
        expect(self.items.first).to_be_visible()

    @allure.step("Verify cart badge shows {count}")
    def expect_cart_count(self, count: int) -> None:
        expect(self.cart_badge).to_have_text(str(count))


class CartPage(BasePage):
    @allure.step("Click Checkout")
    def checkout(self) -> "CheckoutPage":
        _by_test(self.page, "checkout").click()
        return CheckoutPage(self.page)


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.error = _by_test(page, "error")

    @allure.step("Fill checkout info: '{first}' / '{last}' / '{postal}'")
    def fill_info(self, first: str, last: str, postal: str) -> None:
        _by_test(self.page, "firstName").fill(first)
        _by_test(self.page, "lastName").fill(last)
        _by_test(self.page, "postalCode").fill(postal)
        _by_test(self.page, "continue").click()

    @allure.step("Finish the order")
    def finish(self) -> None:
        _by_test(self.page, "finish").click()

    @allure.step("Verify error: {text}")
    def expect_error(self, text: str) -> None:
        expect(self.error).to_have_text(text)

    @allure.step("Verify order confirmation")
    def expect_order_complete(self) -> None:
        expect(_by_test(self.page, "complete-header")).to_have_text("Thank you for your order!")
