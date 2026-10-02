import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Page, expect


class BasePage:
    url = ""

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        with allure.step(f"Open {self.url}"):
            self.page.goto(self.url)
        return self

    def screenshot(self, name: str) -> None:
        allure.attach(self.page.screenshot(), name=name, attachment_type=AttachmentType.PNG)

    def expect_url(self, url: str) -> None:
        with allure.step(f"Verify URL is {url}"):
            expect(self.page).to_have_url(url)
