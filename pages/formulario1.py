"""
Implementación del Page Object Model (POM) para el formulario de registro de DemoQA.

Este módulo encapsula:
- Localizadores de todos los elementos del formulario
- Métodos para interactuar con el formulario (acciones)
- Métodos para validar estados de elementos (validaciones)
- Métodos auxiliares para manejo de fechas y esperas

Utiliza Playwright para la automatización y pytest.expect para las aserciones.
"""

from datetime import datetime
from playwright.sync_api import Page, expect

class FormularioPage:
    """
    Page Object Model para el formulario de registro de DemoQA.
    
    Encapsula la lógica de interacción con los elementos del formulario.
    Utiliza patrones de XPath y selectores CSS para localizar elementos.
    
    El formulario incluye campos para:
    - Nombre y apellido
    - Email
    - Género (radio buttons)
    - Teléfono
    - Fecha de nacimiento (date picker)
    - Asuntos (autocomplete)
    - Hobbies (checkboxes)
    - Dirección
    - Estado y ciudad (dropdowns)
    """
    def __init__(self, page: Page):
        """
        Inicializa el Page Object con localizadores de todos los elementos del formulario.
        
        Almacena la referencia a la página y pre-localiza todos los elementos del formulario.
        Esto permite reutilizar los localizadores sin tener que definirlos en cada método.
        
        Args:
            page (Page): Objeto de página de Playwright
        """
        self.page = page
        
        # ===== CAMPOS DE TEXTO =====
        self.name_input = page.locator('//*[@id="firstName"]')  # Campo de nombre
        self.surname_input = page.locator('//*[@id="lastName"]')  # Campo de apellido
        self.email_input = page.locator('//*[@id="userEmail"]')  # Campo de email
        self.phone_input = page.locator('//*[@id="userNumber"]')  # Campo de teléfono
        self.address_textarea = page.locator('//*[@id="currentAddress"]')  # Área de dirección
        
        # ===== CAMPO DE GÉNERO (RADIO BUTTONS) =====
        self.genderMaleRadio = page.locator('//*[@id="gender-radio-1"]')  # Opción: Masculino
        self.genderFemaleRadio = page.locator('//*[@id="gender-radio-2"]')  # Opción: Femenino
        self.genderOtherRadio = page.locator('//*[@id="gender-radio-3"]')  # Opción: Otro
        
        # ===== CAMPO DE FECHA DE NACIMIENTO =====
        self.date_of_birth_input = page.locator("#dateOfBirthInput")  # Input de fecha
        self.month_dropdown = page.locator(".react-datepicker__month-select")  # Dropdown de mes
        self.year_dropdown = page.locator(".react-datepicker__year-select")  # Dropdown de año
        
        # ===== CAMPO DE ASUNTOS (AUTOCOMPLETE) =====
        self.subject_input = page.locator('//*[@id="subjectsInput"]')  # Campo de entrada de asuntos
        self.suggestions = page.locator('//*[@id="subjectsContainer"]/div/div[1]/div[2]')  # Menú desplegable de sugerencias
        
        # ===== CAMPO DE HOBBIES (CHECKBOXES) =====
        self.sportsCheckbox = page.locator('//*[@id="hobbies-checkbox-1"]')  # Opción: Deportes
        self.readingCheckbox = page.locator('//*[@id="hobbies-checkbox-2"]')  # Opción: Lectura
        self.musicCheckbox = page.locator('//*[@id="hobbies-checkbox-3"]')  # Opción: Música
        
        # ===== CAMPOS DE ESTADO Y CIUDAD (REACT-SELECT) =====
        self.state_dropdown = page.locator('//*[@id="state"]')  # Contenedor del dropdown de estado
        self.city_dropdown = page.locator('//*[@id="city"]')  # Contenedor del dropdown de ciudad
        self.state_input = page.locator('//*[@id="state"]/div/input')  # Input interno de react-select para estado
        self.city_input = page.locator('//*[@id="city"]/div/input')  # Input interno de react-select para ciudad
        
        # ===== BOTÓN DE ENVÍO =====
        self.submit_button = page.locator('//*[@id="submit"]')  # Botón de envío del formulario

    # ===== MÉTODOS DE NAVEGACIÓN =====
    
    def go_to(self, url):
        """
        Navega a una URL específica.
        
        Args:
            url (str): URL a navegar
        """
        self.page.goto(url)

    # ===== MÉTODOS DE ACCIÓN - GÉNERO =====
    
    def select_gender_male(self):
        """
        Selecciona la opción de género "Masculino" haciendo clic en el radio button.
        """
        self.genderMaleRadio.click()
        
    def select_gender_female(self):
        """
        Selecciona la opción de género "Femenino" haciendo clic en el radio button.
        """
        self.genderFemaleRadio.click()

    def select_gender_other(self):
        """
        Selecciona la opción de género "Otro" haciendo clic en el radio button.
        """
        self.genderOtherRadio.click()

    # ===== MÉTODOS DE ACCIÓN - HOBBIES =====

    def select_hobby_sports(self):
        """
        Selecciona el hobby "Deportes" marcando el checkbox correspondiente.
        """
        self.sportsCheckbox.click()
        
    def select_hobby_reading(self):
        """
        Selecciona el hobby "Lectura" marcando el checkbox correspondiente.
        """
        self.readingCheckbox.click()

    def select_hobby_music(self):
        """
        Selecciona el hobby "Música" marcando el checkbox correspondiente.
        """
        self.musicCheckbox.click()

    # ===== MÉTODOS DE ACCIÓN - FECHA DE NACIMIENTO =====
    
    def select_date(self, mes: str, dia: str, año: str):
        """
        Selecciona una fecha completa en el selector de fecha.
        
        Este método realiza los pasos en orden:
        1. Abre el calendario haciendo clic en el input de fecha
        2. Selecciona el año del dropdown
        3. Selecciona el mes del dropdown
        4. Hace clic en el día del calendario
        
        Args:
            mes (str): Mes en formato de nombre completo en inglés (ej: "July")
            dia (str): Día del mes (1-31)
            año (str): Año (ej: "2025")
        """
        self.date_of_birth_input.click()
        self.year_dropdown.select_option(label=año)
        self.month_dropdown.select_option(label=mes)
        self.page.locator(f".react-datepicker__day--0{int(dia):02d}").click()
    
    # NOTA: Método alternativo comentado que puede ser útil en ciertos escenarios
    # def select_date(self, mes: str, dia: str, año: str):
    #     """
    #     Método alternativo con esperas explícitas entre pasos.
    #     Útil cuando el calendario es lento para cargar.
    #     """
    #     # Paso 1: abrir el calendario
    #     self.date_of_birth_input.click()
    #     # Paso 2: esperar a que aparezca el dropdown de año
    #     self.page.wait_for_selector(".react-datepicker__year-select")
    #     # Paso 3: seleccionar mes y año
    #     self.page.locator(".react-datepicker__month-select").select_option(label=mes)
    #     self.page.locator(".react-datepicker__year-select").select_option(label=año)
    #     # Paso 4: seleccionar día
    #     self.page.locator(f".react-datepicker__day--0{int(dia):02d}").click()

    # ===== MÉTODOS DE VALIDACIÓN - GÉNERO =====
    
    def validate_gender_male_selected(self):
        """
        Valida que el radio button de género "Masculino" está marcado.
        
        Lanza una excepción si la validación falla.
        """
        expect(self.page.locator("#gender-radio-1")).to_be_checked()
        
    def validate_gender_female_selected(self):
        """
        Valida que el radio button de género "Femenino" está marcado.
        
        Lanza una excepción si la validación falla.
        """
        expect(self.page.locator("#gender-radio-2")).to_be_checked()
            
    def validate_gender_other_selected(self):
        """
        Valida que el radio button de género "Otro" está marcado.
        
        Lanza una excepción si la validación falla.
        """
        expect(self.page.locator("#gender-radio-3")).to_be_checked()

    # ===== MÉTODOS DE VALIDACIÓN - HOBBIES =====

    def validate_hobby_sports_selected(self):
        """
        Valida que el checkbox de hobby "Deportes" está marcado.
        
        Lanza una excepción si la validación falla.
        """
        expect(self.page.locator("#hobbies-checkbox-1")).to_be_checked()

    def validate_hobby_reading_selected(self):
        """
        Valida que el checkbox de hobby "Lectura" está marcado.
        
        Lanza una excepción si la validación falla.
        """
        expect(self.page.locator("#hobbies-checkbox-2")).to_be_checked()

    def validate_hobby_music_selected(self):
        """
        Valida que el checkbox de hobby "Música" está marcado.
        
        Lanza una excepción si la validación falla.
        """
        expect(self.page.locator("#hobbies-checkbox-3")).to_be_checked()

    # ===== MÉTODOS DE VALIDACIÓN - FECHA DE NACIMIENTO =====
    
    def validate_date(self, expected: str):
        """
        Valida que el input de fecha de nacimiento contiene la fecha esperada.
        
        Normaliza el formato de la fecha esperada:
        - Convierte nombres de meses completos a abreviaciones (ej: "January" -> "Jan")
        - Valida que el input tenga el valor esperado
        
        Este paso es necesario porque el formulario de DemoQA almacena las fechas
        en formato abreviado (DD MMM YYYY), pero los escenarios usan nombres completos.
        
        Args:
            expected (str): Fecha esperada en formato "DD MONTH YYYY"
                           (ej: "10 July 2025")
                           
        Lanza una excepción si la validación falla.
        """
        # Diccionario de conversión: mes largo -> mes abreviado
        replacements = {
            "January": "Jan", "February": "Feb", "March": "Mar",
            "April": "Apr", "May": "May", "June": "Jun",
            "July": "Jul", "August": "Aug", "September": "Sep",
            "October": "Oct", "November": "Nov", "December": "Dec"
        }
        
        # Convertir meses largos a abreviados en la fecha esperada
        for full, short in replacements.items():
            expected = expected.replace(full, short)
            
        # Validar que el input tiene el valor esperado
        expect(self.date_of_birth_input).to_have_value(expected)

    # ===== MÉTODOS AUXILIARES - LECTURA DE FECHA =====
    
    def get_default_date(self):
        """
        Obtiene la fecha por defecto del campo de fecha de nacimiento como string.
        
        Returns:
            str: Fecha en formato "DD MMM YYYY" (ej: "14 Aug 2026")
        """
        value = self.date_of_birth_input.input_value()
        return value
        
    def get_default_date_as_datetime(self):
        """
        Obtiene la fecha por defecto del campo de fecha y la convierte a objeto datetime.
        
        Útil para realizar cálculos o comparaciones con fechas.
        
        Returns:
            datetime: Objeto datetime representando la fecha
            
        Raises:
            ValueError: Si la fecha no está en el formato esperado "%d %b %Y"
        """
        value = self.date_of_birth_input.input_value()
        return datetime.strptime(value, "%d %b %Y")

    # ===== MÉTODOS AUXILIARES - ESPERA =====
    
    def wait(self, ms=3000):
        """
        Pausa la ejecución del test por un tiempo especificado.
        
        Utilizado principalmente para:
        - Observar interacciones en tiempo real (debugging)
        - Esperar a que efectos visuales terminen
        - Esperar a que el navegador se estabilice después de cambios
        
        Nota: En pruebas automatizadas, es preferible usar wait_for_selector() 
        o wait_for_function() cuando sea posible, en lugar de esperas fijas.
        
        Args:
            ms (int): Tiempo de espera en milisegundos (default: 3000 = 3 segundos)
        """
        self.page.wait_for_timeout(ms)
    
    
    