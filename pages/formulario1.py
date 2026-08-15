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
        self.date_input = page.locator('//*[@id="dateOfBirthInput"]')
        self.prev_month_button = page.locator('//*[@id="dateOfBirth"]/div[2]/div[2]/div/div/div/button[1]')
        self.next_month_button = page.locator('//*[@id="dateOfBirth"]/div[2]/div[2]/div/div/div/button[2]')
        self.month_label = page.locator('//*[@id="dateOfBirth"]/div[2]/div[2]/div/div/div/div/div[1]/h2]')
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
        
    def wait(self, ms=3000):
        self.page.wait_for_timeout(ms)
        