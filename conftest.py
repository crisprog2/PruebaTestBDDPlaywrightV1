import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    context = browser.new_context(
            record_video_dir="videos_evidencia/"   # carpeta en raíz del proyecto
        )
    page = context.new_page()
    yield page
    context.close()
    page.close()
