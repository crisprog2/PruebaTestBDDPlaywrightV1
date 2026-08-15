import logging
import pytest
from pytest_bdd import parsers, scenarios, given, when, then
from pages.formulario1 import FormularioPage

logger = logging.getLogger(__name__)

scenarios('../features/formulario.feature')

@pytest.fixture
def formulario_page(page):
    page.goto("https://demoqa.com/automation-practice-form")
    return FormularioPage(page)

@given('estoy en la página de registro')
def step_impl(formulario_page):
    pass

@when('selecciono el género masculino')
def step_impl(formulario_page):
    formulario_page.select_gender_male()
    
@then("el radio masculino debe estar marcado")
def step_impl(formulario_page):
    formulario_page.validate_gender_male_selected()
    formulario_page.wait()
    
@when('selecciono el hobby deportes')
def step_impl(formulario_page):
    formulario_page.select_hobby_sports()

@then("el checkbox deportes debe estar marcado")
def step_impl(formulario_page):
    formulario_page.validate_hobby_sports_selected()
    formulario_page.wait()
    
@when('selecciono el Date of Birth')
def step_impl(formulario_page):
    default_date = formulario_page.get_default_date()
    logger.info(f"Fecha por defecto: {default_date}")

@then("calendar me devuelve la fecha por default")
def step_impl(formulario_page):
    default_date = formulario_page.get_default_date_as_datetime()
    logger.info(f"Fecha por defecto como datetime: {default_date}")
    formulario_page.wait()
    
@when("selecciono el campo Date of Birth")
def step_impl(formulario_page):
    formulario_page.date_of_birth_input.click()

@when(parsers.parse('elijo el año "{año}"'))
def step_impl(formulario_page, año):
    formulario_page.year_dropdown.select_option(label=año)

@when(parsers.parse('elijo el mes "{mes}"'))
def step_impl(formulario_page, mes):
    formulario_page.month_dropdown.select_option(label=mes)

@when(parsers.parse('elijo el día "{día}"'))
def step_impl(formulario_page, día):
    formulario_page.page.locator(f".react-datepicker__day--0{int(día):02d}").click()

@then(parsers.parse('el calendario muestra la fecha "{día} {mes} {año}"'))
def step_impl(formulario_page, día, mes, año):
    expected = f"{día} {mes} {año}"
    formulario_page.validate_date(expected)
    formulario_page.wait()
    