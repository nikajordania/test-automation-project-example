import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage

ERROR_RED = "rgb(220, 53, 69)"


class PracticeFormPage(BasePage):
    url = "https://demoqa.com/automation-practice-form"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.locator("#firstName")
        self.last_name = page.locator("#lastName")
        self.email = page.locator("#userEmail")
        self.phone = page.locator("#userNumber")
        self.female = page.locator("label[for='gender-radio-2']")
        self.submit_button = page.locator("#submit")
        self.modal_title = page.locator("#example-modal-sizes-title-lg")
        self.modal_body = page.locator(".modal-body")

    def open(self):
        super().open()
        with allure.step("Remove ad banners that overlap the form"):
            self.page.evaluate(
                "document.querySelectorAll('#fixedban, footer, iframe').forEach(e => e.remove())"
            )
        return self

    @allure.step("Fill form: first='{first}', last='{last}', email='{email}', phone='{phone}'")
    def fill(self, first: str = "Anna", last: str = "Test", email: str = "", phone: str = "1234567890") -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        if email:
            self.email.fill(email)
        self.female.click()
        self.phone.fill(phone)

    @allure.step("Submit the form")
    def submit(self) -> None:
        self.submit_button.scroll_into_view_if_needed()
        self.submit_button.click()

    @allure.step("Verify the confirmation modal contains: {texts}")
    def expect_submitted(self, *texts: str) -> None:
        expect(self.modal_title).to_have_text("Thanks for submitting the form")
        for text in texts:
            expect(self.modal_body).to_contain_text(text)

    @allure.step("Verify the form was not submitted")
    def expect_not_submitted(self) -> None:
        expect(self.modal_title).to_have_count(0)

    @allure.step("Verify the field is highlighted red")
    def expect_invalid(self, field) -> None:
        expect(field).to_have_css("border-color", ERROR_RED)

    @allure.step("Verify phone value is '{value}'")
    def expect_phone_value(self, value: str) -> None:
        expect(self.phone).to_have_value(value)
