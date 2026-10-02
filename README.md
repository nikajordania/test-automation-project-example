# test-case-automation

UI test automation with **Python + Playwright + pytest + Allure**.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (installs Python 3.13+ and dependencies)
- Java (JDK/JRE 11+) — required by the Allure CLI
- Git

## Environment setup

```shell
# 1. Install Python dependencies into .venv
uv sync

# 2. Install Playwright browsers
uv run playwright install

# 3. Install the Allure CLI locally into ./.allure (also happens automatically on first use)
uv run python allure_tool.py install
```

## Running tests

```shell
# Headless (default)
uv run pytest --alluredir=allure-results

# Headed (visible browser)
uv run pytest --headed --alluredir=allure-results

# Headed + slowed down (ms between actions)
uv run pytest --headed --slowmo 500 --alluredir=allure-results

# Choose a browser: chromium (default), firefox, webkit
uv run pytest --headed --browser firefox --alluredir=allure-results

# Run a single test
uv run pytest tests/test_example.py::TestHomePage::test_has_title --headed --alluredir=allure-results

# Run by Allure tag / keyword
uv run pytest -k "title" --alluredir=allure-results
```

## Running on other browsers

No code changes are needed, use the `--browser` option:

```shell
uv run pytest --browser firefox --alluredir=allure-results
uv run pytest --browser webkit --alluredir=allure-results

# several browsers in one run (every test runs once per browser)
uv run pytest --browser chromium --browser firefox --alluredir=allure-results

# installed Chrome / Edge instead of the bundled Chromium
uv run pytest --browser-channel chrome --alluredir=allure-results
uv run pytest --browser-channel msedge --alluredir=allure-results

# install a missing browser (goes to PLAYWRIGHT_BROWSERS_PATH)
uv run playwright install firefox webkit
```

Test names get a browser suffix (e.g. `[firefox]`) in the Allure report.
To change the default browser, add `--browser firefox` to `addopts` in `pyproject.toml`.

## Parallel execution

Configured in `pyproject.toml` (`-n 4 --dist loadfile`, via pytest-xdist): each test **file** runs on one worker,
different files run in parallel, and tests inside a file stay sequential.

```shell
uv run pytest --alluredir=allure-results          # 4 workers (default)
uv run pytest -n 2 --alluredir=allure-results     # change worker count
uv run pytest -n auto --alluredir=allure-results  # one worker per CPU core
uv run pytest -n 0 --alluredir=allure-results     # disable parallelism (debugging)
```

## Allure report

```shell
# (Optional) delete the old allure-results folder first for a clean report

# Generate the report and open it in the browser
uv run python allure_tool.py serve

# Or generate a static report into ./allure-report
uv run python allure_tool.py generate
```

The Allure version can be changed with the `ALLURE_VERSION` environment variable (default `2.46.1`).

## Screenshots

- Tests attach step screenshots explicitly via `allure.attach(page.screenshot(), ...)`.
- `conftest.py` automatically attaches a full-page screenshot and the page URL
  to the report whenever a test **fails**.
- Playwright's own screenshots can also be saved: `uv run pytest --screenshot on`
  (`on` / `off` / `only-on-failure`).

## Code quality

```shell
uv run ruff check .
uv run ruff format .
uv run mypy .
```

## Project layout

| Path               | Purpose                                                  |
|--------------------|----------------------------------------------------------|
| `tests/test_the_internet.py` | TC-01..06: The Internet login form (from `tasks.md`) |
| `tests/test_saucedemo.py`   | TC-01..07: SauceDemo login, cart, checkout           |
| `tests/test_demoqa.py`      | TC-01..05: DemoQA practice form                      |
| `tests/test_example.py`     | Sample Playwright tests                              |
| `pages/`           | Page Objects (locators + actions as Allure steps)        |
| `tasks.md`         | Test-case specification the tests are based on           |
| `pyproject.toml`   | Dependencies and pytest settings (test discovery, parallel run) |
| `conftest.py`      | Attaches failure screenshots to Allure                   |
| `allure_tool.py`   | Downloads/runs the Allure CLI locally (like allure-maven) |
| `.allure/`         | Locally installed Allure CLI (git-ignored)               |
| `allure-results/`  | Raw test results (git-ignored)                           |
