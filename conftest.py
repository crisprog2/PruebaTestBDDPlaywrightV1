import logging
import pytest
from playwright.sync_api import sync_playwright
from pytest_bdd_report import attach
from PIL import Image, ImageDraw

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

# --- Función para marcar la captura ---
def mark_screenshot(path, success=True):
    img = Image.open(path)
    draw = ImageDraw.Draw(img)

    if success:
        # Rectángulo verde + texto
        draw.rectangle([(50, 50), (300, 150)], outline="green", width=5)
        draw.text((60, 60), "VALIDACIÓN OK", fill="green")
    else:
        # Rectángulo rojo + texto
        draw.rectangle([(50, 50), (300, 150)], outline="red", width=5)
        draw.text((60, 60), "ERROR", fill="red")

    marked_path = "marked_" + path
    img.save(marked_path)
    return marked_path

# --- Hook para capturar resultado de cada test ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Ejecuta el resto de los plugins primero
    outcome = yield
    rep = outcome.get_result()

    # Guarda el resultado en el objeto del test
    if "page" in item.fixturenames:
        setattr(item, "rep_" + rep.when, rep)
        
def pytest_configure(config):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )