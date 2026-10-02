import re

import allure
from allure_commons.types import AttachmentType, Severity
from playwright.sync_api import Page, expect

BASE_URL = "https://playwright.dev/"


@allure.epic("Playwright Website")
@allure.feature("Home Page")
class TestHomePage:
    @allure.story("Page title")
    @allure.title("Home page has a title containing 'Playwright'")
    @allure.description(
        "Opens the Playwright home page and verifies that the browser tab title "
        "contains the word 'Playwright'."
    )
    @allure.severity(Severity.CRITICAL)
    @allure.tag("smoke", "ui", "title")
    @allure.label("owner", "nika.zhordania")
    @allure.link(BASE_URL, name="Playwright website")
    @allure.testcase(BASE_URL, name="TC-001: Verify home page title")
    def test_has_title(self, page: Page):
        with allure.step("Open playwright.dev"):
            page.goto(BASE_URL)
            allure.attach(
                page.url,
                name="Opened URL",
                attachment_type=AttachmentType.TEXT,
            )

        with allure.step("Verify page title contains 'Playwright'"):
            allure.attach(
                page.title(),
                name="Actual title",
                attachment_type=AttachmentType.TEXT,
            )
            expect(page).to_have_title(re.compile("Playwright"))

        with allure.step("Take screenshot of the home page"):
            allure.attach(
                page.screenshot(),
                name="Home page",
                attachment_type=AttachmentType.PNG,
            )

    @allure.story("Navigation")
    @allure.title("'Get started' link leads to the Installation page")
    @allure.description(
        "Clicks the 'Get started' link on the home page and verifies that the "
        "Installation page with its heading is displayed."
    )
    @allure.severity(Severity.NORMAL)
    @allure.tag("regression", "ui", "navigation")
    @allure.label("owner", "nika.zhordania")
    @allure.link(BASE_URL + "docs/intro", name="Installation docs")
    @allure.testcase(BASE_URL, name="TC-002: Verify 'Get started' navigation")
    def test_get_started_link(self, page: Page):
        with allure.step("Open playwright.dev"):
            page.goto(BASE_URL)

        with allure.step("Click the 'Get started' link"):
            page.get_by_role("link", name="Get started").click()
            allure.attach(
                page.url,
                name="URL after click",
                attachment_type=AttachmentType.TEXT,
            )

        with allure.step("Verify 'Installation' heading is visible"):
            expect(page.get_by_role("heading", name="Installation")).to_be_visible()

        with allure.step("Take screenshot of the Installation page"):
            allure.attach(
                page.screenshot(),
                name="Installation page",
                attachment_type=AttachmentType.PNG,
            )
