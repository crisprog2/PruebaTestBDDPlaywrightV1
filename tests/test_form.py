import pytest
from pytest_bdd import scenarios, given, when, then
from pages.formulario1 import FormularioPage

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
    