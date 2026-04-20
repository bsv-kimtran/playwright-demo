import os
import subprocess
from typing import Generator
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from pages.login_page import LoginPage, LOGIN_URL, TOP_URL

REPORT_PATH = os.path.join(os.path.dirname(__file__), "report", "report.html")

VALID_EMAIL = os.getenv("TEST_EMAIL", "your_registered@email.com")
VALID_PASSWORD = os.getenv("TEST_PASSWORD", "YourPassword1!")

# HEADLESS=false → mở browser UI (dễ debug)
# HEADLESS=true  → chạy ngầm, không mở browser (CI/CD, nhanh hơn)
HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"


@pytest.fixture(scope="session")
def browser_instance() -> Generator[Browser, None, None]:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=HEADLESS,
            slow_mo=0 if HEADLESS else 300,
        )
        yield browser
        browser.close()


@pytest.fixture
def context(browser_instance: Browser) -> Generator[BrowserContext, None, None]:
    ctx = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture
def login_page(page: Page) -> Generator[LoginPage, None, None]:
    lp = LoginPage(page)
    lp.navigate()
    yield lp


def pytest_sessionfinish(session, exitstatus):
    """Tự động mở report.html trên browser sau khi chạy test xong"""
    if os.path.exists(REPORT_PATH):
        print(f"\n📊 Opening report: {REPORT_PATH}")
        subprocess.Popen(["open", REPORT_PATH])  # macOS: dùng 'open'
