"""
Configuración central de pytest para la suite de automatización.

Este módulo proporciona:
- Fixtures de Playwright para la gestión de navegador y páginas
- Funciones para marcar capturas de pantalla con estados de validación
- Hooks de pytest para capturar resultados de pruebas
- Configuración de logging para registrar eventos de prueba
"""

import logging
import pytest
from playwright.sync_api import sync_playwright
from pytest_bdd_report import attach
from PIL import Image, ImageDraw

# ========== FIXTURES DE PLAYWRIGHT ==========

@pytest.fixture(scope="session")
def browser():
    """
    Fixture a nivel de sesión que crea y proporciona una instancia del navegador Chromium.
    
    Se ejecuta una sola vez por sesión de prueba y se reutiliza para todas las pruebas.
    Garantiza que el navegador se cierre correctamente al finalizar todas las pruebas.
    
    Yields:
        Browser: Instancia del navegador Chromium de Playwright
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)  # headless=False permite ver el navegador
    yield browser
    browser.close()

@pytest.fixture
def page(browser):
    """
    Fixture que crea una nueva página en un contexto del navegador con grabación de video.
    
    Se ejecuta antes de cada prueba y:
    - Crea un nuevo contexto de navegador
    - Habilita la grabación de videos como evidencia de las pruebas
    - Almacena los videos en la carpeta 'videos_evidencia/'
    
    Args:
        browser: Fixture del navegador proporcionada por la fixture 'browser'
        
    Yields:
        Page: Página de Playwright lista para interactuar con elementos
        
    Cleanup:
        Cierra el contexto y la página después de cada prueba
    """
    page = browser.new_page()
    context = browser.new_context(
            record_video_dir="videos_evidencia/"  # Carpeta en raíz del proyecto para guardar videos
        )
    page = context.new_page()
    yield page
    context.close()
    page.close()

# ========== FUNCIONES AUXILIARES ==========

def mark_screenshot(path, success=True):
    """
    Marca una captura de pantalla con un rectángulo de validación y texto indicativo.
    
    Abre una imagen existente y dibuja sobre ella:
    - Si success=True: Dibuja un rectángulo verde con texto "VALIDACIÓN OK"
    - Si success=False: Dibuja un rectángulo rojo con texto "ERROR"
    
    La imagen marcada se guarda con el prefijo "marked_" en el mismo directorio.
    
    Args:
        path (str): Ruta del archivo de imagen a marcar
        success (bool): Indica si la validación fue exitosa (default: True)
        
    Returns:
        str: Ruta del archivo de imagen marcado
    """
    img = Image.open(path)
    draw = ImageDraw.Draw(img)

    if success:
        # Rectángulo verde + texto para validación exitosa
        draw.rectangle([(50, 50), (300, 150)], outline="green", width=5)
        draw.text((60, 60), "VALIDACIÓN OK", fill="green")
    else:
        # Rectángulo rojo + texto para validación fallida
        draw.rectangle([(50, 50), (300, 150)], outline="red", width=5)
        draw.text((60, 60), "ERROR", fill="red")

    marked_path = "marked_" + path
    img.save(marked_path)
    return marked_path

# ========== HOOKS DE PYTEST ==========

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de pytest que se ejecuta después de cada prueba para capturar su resultado.
    
    Este hook se ejecuta después de que todos los plugins hayan procesado el resultado
    de la prueba. Permite acceder al reporte de la prueba y almacenarlo en el objeto item.
    
    Args:
        item: Objeto de prueba de pytest
        call: Información de la llamada a la prueba
    """
    # Ejecuta el resto de los plugins primero
    outcome = yield
    rep = outcome.get_result()

    # Guarda el resultado en el objeto del test si tiene la fixture 'page'
    if "page" in item.fixturenames:
        setattr(item, "rep_" + rep.when, rep)

# ========== CONFIGURACIÓN DE LOGGING ==========

def pytest_configure(config):
    """
    Hook de pytest que se ejecuta antes de que comience la sesión de pruebas.
    
    Configura el sistema de logging para que registre todos los eventos de prueba
    con timestamps y niveles de severidad. El formato es:
    "YYYY-MM-DD HH:MM:SS [NIVEL] mensaje"
    
    Args:
        config: Objeto de configuración de pytest
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )