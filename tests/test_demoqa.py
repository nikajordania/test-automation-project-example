import allure
import pytest
from allure_commons.types import Severity
from playwright.sync_api import Page

from pages.demoqa import PracticeFormPage


@allure.epic("Practice sites")
@allure.feature("DemoQA: Practice Form")
@allure.link(PracticeFormPage.url, name="Practice form")
@allure.label("owner", "nika.zhordania")
class TestDemoQaPracticeForm:
    @pytest.fixture(autouse=True)
    def form(self, page: Page) -> PracticeFormPage:
        return PracticeFormPage(page).open()

    @allure.story("Positive")
    @allure.title("TC-01: All required fields are valid, the form is submitted")
    @allure.severity(Severity.BLOCKER)
    @allure.tag("smoke", "positive")
    def test_tc01_valid_submission(self, form: PracticeFormPage):
        form.fill()
        form.submit()
        form.expect_submitted("Anna Test", "Female", "1234567890")
        form.screenshot("Confirmation modal")

    @allure.story("Negative")
    @allure.title("TC-02: Empty First Name blocks submission")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("negative")
    def test_tc02_empty_first_name(self, form: PracticeFormPage):
        form.fill(first="")
        form.submit()
        form.expect_not_submitted()
        form.expect_invalid(form.first_name)
        form.screenshot("Empty first name")

    @allure.story("Boundary")
    @allure.title("TC-03: 9-digit phone number blocks submission")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("boundary")
    def test_tc03_phone_9_digits(self, form: PracticeFormPage):
        form.fill(phone="123456789")
        form.submit()
        form.expect_not_submitted()
        form.expect_invalid(form.phone)
        form.screenshot("Phone 9 digits")

    @allure.story("Boundary")
    @allure.title("TC-04: 11-digit phone number is limited to 10 digits")
    @allure.severity(Severity.NORMAL)
    @allure.tag("boundary")
    def test_tc04_phone_11_digits(self, form: PracticeFormPage):
        form.fill(phone="12345678901")
        form.expect_phone_value("1234567890")
        form.screenshot("Phone 11 digits")

    @allure.story("Negative")
    @allure.title("TC-05: Invalid email 'anna@' blocks submission")
    @allure.severity(Severity.NORMAL)
    @allure.tag("negative")
    def test_tc05_invalid_email(self, form: PracticeFormPage):
        form.fill(email="anna@")
        form.submit()
        form.expect_not_submitted()
        form.expect_invalid(form.email)
        form.screenshot("Invalid email")
