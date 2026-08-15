from datetime import datetime

from playwright.sync_api import Page, expect

class FormularioPage:
    def __init__(self, page: Page):
        self.page = page
        self.name_input = page.locator('//*[@id="firstName"]')
        self.surname_input = page.locator('//*[@id="lastName"]')
        self.email_input = page.locator('//*[@id="userEmail"]')
        self.genderMaleRadio = page.locator('//*[@id="gender-radio-1"]')
        self.genderFemaleRadio = page.locator('//*[@id="gender-radio-2"]')
        self.genderOtherRadio = page.locator('//*[@id="gender-radio-3"]')
        self.phone_input = page.locator('//*[@id="userNumber"]')
        self.date_of_birth_input = page.locator("#dateOfBirthInput")
        self.month_dropdown = page.locator(".react-datepicker__month-select")
        self.year_dropdown = page.locator(".react-datepicker__year-select")
        self.subject_input = page.locator('//*[@id="subjectsInput"]')  # campo de autocompletado
        self.suggestions = page.locator('//*[@id="subjectsContainer"]/div/div[1]/div[2]')  # menú desplegado
        self.sportsCheckbox = page.locator('//*[@id="hobbies-checkbox-1"]')
        self.readingCheckbox = page.locator('//*[@id="hobbies-checkbox-2"]')
        self.musicCheckbox = page.locator('//*[@id="hobbies-checkbox-3"]')
        self.address_textarea = page.locator('//*[@id="currentAddress"]')
        self.state_dropdown = page.locator('//*[@id="state"]')  # contenedor del dropdown
        self.city_dropdown = page.locator('//*[@id="city"]')
        self.state_input = page.locator('//*[@id="state"]/div/input')  # input interno de react-select
        self.city_input = page.locator('//*[@id="city"]/div/input')
        self.submit_button = page.locator('//*[@id="submit"]')

    def go_to(self, url):
        self.page.goto(url)
        
    # Acciones
    def select_gender_male(self):
        self.genderMaleRadio.click()
        
    def select_gender_female(self):
        self.genderFemaleRadio.click()

    def select_gender_other(self):
        self.genderOtherRadio.click()

    def select_hobby_sports(self):
        self.sportsCheckbox.click()
        
    def select_hobby_reading(self):
        self.readingCheckbox.click()

    def select_hobby_music(self):
        self.musicCheckbox.click()
        
    def select_date(self, mes: str, dia: str, año: str):
        self.date_of_birth_input.click()
        self.year_dropdown.select_option(label=año)
        self.month_dropdown.select_option(label=mes)
        self.page.locator(f".react-datepicker__day--0{int(dia):02d}").click()
    
    #def select_date(self, mes: str, dia: str, año: str):
    #    # Paso 1: abrir el calendario
    #    self.date_of_birth_input.click()

    #    # Paso 2: esperar a que aparezca el dropdown de año
    #    self.page.wait_for_selector(".react-datepicker__year-select")

    #    # Paso 3: seleccionar mes y año
    #    self.page.locator(".react-datepicker__month-select").select_option(label=mes)
    #    self.page.locator(".react-datepicker__year-select").select_option(label=año)

    #    # Paso 4: seleccionar día
    #    self.page.locator(f".react-datepicker__day--0{int(dia):02d}").click()

    # Validaciones
    def validate_gender_male_selected(self):
        expect(self.page.locator("#gender-radio-1")).to_be_checked()
        
    def validate_gender_female_selected(self):
        expect(self.page.locator("#gender-radio-2")).to_be_checked()
            
    def validate_gender_other_selected(self):
        expect(self.page.locator("#gender-radio-3")).to_be_checked()

    def validate_hobby_sports_selected(self):
        expect(self.page.locator("#hobbies-checkbox-1")).to_be_checked()

    def validate_hobby_reading_selected(self):
        expect(self.page.locator("#hobbies-checkbox-2")).to_be_checked()

    def validate_hobby_music_selected(self):
        expect(self.page.locator("#hobbies-checkbox-3")).to_be_checked()
        
    def validate_date(self, expected: str):
        # Normaliza el formato esperado para que coincida con DemoQA
        replacements = {
            "January": "Jan", "February": "Feb", "March": "Mar",
            "April": "Apr", "May": "May", "June": "Jun",
            "July": "Jul", "August": "Aug", "September": "Sep",
            "October": "Oct", "November": "Nov", "December": "Dec"
        }
        # Convertir meses largos a abreviados
        for full, short in replacements.items():
            expected = expected.replace(full, short)
        # Ahora sí validar con Playwrigh
        expect(self.date_of_birth_input).to_have_value(expected)
        
    # Nuevo método para obtener la fecha por defecto
    def get_default_date(self):
        value = self.date_of_birth_input.input_value()  # Ejemplo: "14 Aug 2026"
        return value
        
    # Si quieres parsear a datetime
    def get_default_date_as_datetime(self):
        value = self.date_of_birth_input.input_value()
        return datetime.strptime(value, "%d %b %Y")
    
    # Espera
    def wait(self, ms=3000):
        self.page.wait_for_timeout(ms)
    
    
    