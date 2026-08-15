"""
Definición de pasos (steps) de BDD para las pruebas de automatización.

Este módulo implementa los pasos de Gherkin definidos en formulario.feature usando
pytest-bdd. Cada paso corresponde a:
- GIVEN: Precondiciones (estado inicial)
- WHEN: Acciones del usuario
- THEN: Validaciones y verificaciones

Los pasos interactúan con FormularioPage (Page Object Model) que encapsula
los elementos y acciones del formulario de registro de DemoQA.
"""

import logging
import pytest
from pytest_bdd import parsers, scenarios, given, when, then
from pages.formulario1 import FormularioPage

# Logger para registrar eventos de prueba
logger = logging.getLogger(__name__)

# Carga automáticamente todos los escenarios definidos en formulario.feature
scenarios('../features/formulario.feature')

# ========== FIXTURES ==========

@pytest.fixture
def formulario_page(page):
    """
    Fixture que navegada a la URL del formulario de prueba y devuelve una instancia de FormularioPage.
    
    Esta fixture:
    1. Navega a https://demoqa.com/automation-practice-form
    2. Crea una instancia de FormularioPage con la página
    3. Proporciona un objeto POM listo para interactuar con el formulario
    
    Args:
        page: Fixture de Playwright que proporciona la instancia de página
        
    Returns:
        FormularioPage: Objeto Page Object Model del formulario
    """
    page.goto("https://demoqa.com/automation-practice-form")
    return FormularioPage(page)

# ========== PASOS GIVEN (PRECONDICIONES) ==========

@given('estoy en la página de registro')
def step_impl(formulario_page):
    """
    Paso GIVEN: Valida que el usuario está en la página de registro de DemoQA.
    
    Este paso es pasivo - solo verifica que se llegó a la página correcta.
    La navegación ocurre en la fixture formulario_page.
    """
    pass

# ========== PASOS WHEN - SELECCIÓN DE GÉNERO ==========

@when('selecciono el género masculino')
def step_impl(formulario_page):
    """
    Paso WHEN: Hace clic en el radio button de género masculino.
    
    Interactúa con FormularioPage para seleccionar la opción masculino.
    """
    formulario_page.select_gender_male()

# ========== PASOS THEN - VALIDACIÓN DE GÉNERO ==========

@then("el radio masculino debe estar marcado")
def step_impl(formulario_page):
    """
    Paso THEN: Valida que el radio button de género masculino está marcado.
    
    Usa la afirmación de Playwright (expect) para verificar el estado de checked.
    Incluye una espera de 3 segundos para observar el cambio (opcional para debugging).
    """
    formulario_page.validate_gender_male_selected()
    formulario_page.wait()

# ========== PASOS WHEN - SELECCIÓN DE HOBBIES ==========

@when('selecciono el hobby deportes')
def step_impl(formulario_page):
    """
    Paso WHEN: Hace clic en el checkbox de hobby "Deportes".
    
    Interactúa con FormularioPage para seleccionar la opción de deportes.
    """
    formulario_page.select_hobby_sports()

# ========== PASOS THEN - VALIDACIÓN DE HOBBIES ==========

@then("el checkbox deportes debe estar marcado")
def step_impl(formulario_page):
    """
    Paso THEN: Valida que el checkbox de hobby "Deportes" está marcado.
    
    Usa la afirmación de Playwright para verificar que el checkbox está checked.
    Incluye una espera de 3 segundos para observar el cambio.
    """
    formulario_page.validate_hobby_sports_selected()
    formulario_page.wait()

# ========== PASOS WHEN - FECHA DE NACIMIENTO (FECHA POR DEFECTO) ==========

@when('selecciono el Date of Birth')
def step_impl(formulario_page):
    """
    Paso WHEN: Obtiene la fecha por defecto del campo Date of Birth.
    
    Lee el valor actual del input de fecha sin modificarlo.
    Registra en el log la fecha por defecto del sistema.
    """
    default_date = formulario_page.get_default_date()
    logger.info(f"Fecha por defecto: {default_date}")

# ========== PASOS THEN - VALIDACIÓN DE FECHA POR DEFECTO ==========

@then("calendar me devuelve la fecha por default")
def step_impl(formulario_page):
    """
    Paso THEN: Valida la fecha por defecto y la convierte a formato datetime.
    
    - Obtiene la fecha del campo como string (ej: "14 Aug 2026")
    - La convierte a objeto datetime para análisis más detallado
    - Registra en el log la conversión
    - Espera 3 segundos para observación
    """
    default_date = formulario_page.get_default_date_as_datetime()
    logger.info(f"Fecha por defecto como datetime: {default_date}")
    formulario_page.wait()

# ========== PASOS WHEN - FECHA DE NACIMIENTO (CAMPOS INDIVIDUALES) ==========

@when("selecciono el campo Date of Birth")
def step_impl(formulario_page):
    """
    Paso WHEN: Abre el selector de fecha haciendo clic en el campo Date of Birth.
    
    Este paso abre el calendario para permitir la selección manual de fecha.
    """
    formulario_page.date_of_birth_input.click()

@when(parsers.parse('elijo el año "{año}"'))
def step_impl(formulario_page, año):
    """
    Paso WHEN: Selecciona un año del dropdown de años en el calendario.
    
    Este paso es parte de un Scenario Outline que parameteriza datos de prueba.
    
    Args:
        año (str): Año a seleccionar (ej: "2025", "2024", "2023")
    """
    formulario_page.year_dropdown.select_option(label=año)

@when(parsers.parse('elijo el mes "{mes}"'))
def step_impl(formulario_page, mes):
    """
    Paso WHEN: Selecciona un mes del dropdown de meses en el calendario.
    
    Este paso es parte de un Scenario Outline que parameteriza datos de prueba.
    
    Args:
        mes (str): Mes a seleccionar en inglés (ej: "July", "June", "May")
    """
    formulario_page.month_dropdown.select_option(label=mes)

@when(parsers.parse('elijo el día "{día}"'))
def step_impl(formulario_page, día):
    """
    Paso WHEN: Selecciona un día haciendo clic en el calendario.
    
    El selector CSS `react-datepicker__day--0X` contiene:
    - `--0`: Prefijo del componente
    - `X`: Número del día (01, 02, ..., 31) con formato 02d
    
    Args:
        día (str): Día a seleccionar (ej: "10", "15", "20")
    """
    formulario_page.page.locator(f".react-datepicker__day--0{int(día):02d}").click()

# ========== PASOS THEN - VALIDACIÓN DE FECHA SELECCIONADA ==========

@then(parsers.parse('el calendario muestra la fecha "{día} {mes} {año}"'))
def step_impl(formulario_page, día, mes, año):
    """
    Paso THEN: Valida que la fecha seleccionada coincide con la esperada.
    
    Este paso:
    1. Construye la fecha esperada en formato "DD MONTH YYYY" (ej: "10 July 2025")
    2. Llama a FormularioPage.validate_date() para verificar que el campo tiene el valor correcto
    3. Convierte meses largos a abreviados para coincidir con el formato de DemoQA
    4. Espera 3 segundos para observación
    
    Args:
        día (str): Día de la fecha esperada
        mes (str): Mes de la fecha esperada en inglés completo
        año (str): Año de la fecha esperada
    """
    expected = f"{día} {mes} {año}"
    formulario_page.validate_date(expected)
    formulario_page.wait()
    