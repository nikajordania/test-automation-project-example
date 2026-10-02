import allure
import pytest
from allure_commons.types import AttachmentType


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a full-page screenshot and page URL to the Allure report when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    allure.attach(
        page.screenshot(full_page=True),
        name="Failure screenshot",
        attachment_type=AttachmentType.PNG,
    )
    allure.attach(page.url, name="URL at failure", attachment_type=AttachmentType.TEXT)
