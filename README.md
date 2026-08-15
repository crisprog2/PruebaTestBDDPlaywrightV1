# Suite de Automatización BDD con Playwright

## 📋 Descripción General

Suite de automatización de pruebas end-to-end (E2E) para el formulario de registro de [DemoQA](https://demoqa.com/automation-practice-form). Este proyecto es un repositorio de aprendizaje que demuestra las mejores prácticas de automatización en Python usando:

- **Playwright**: Framework de automatización de navegador multiplataforma
- **pytest-bdd**: Framework de testing con especificaciones BDD (Behavior-Driven Development)
- **Gherkin**: Lenguaje de especificación de comportamiento legible por humanos

---

## 🏗️ Estructura del Proyecto

```
├── conftest.py                           # Configuración central de pytest
├── requirements.txt                      # Dependencias del proyecto
├── README.md                            # Este archivo
├── features/
│   └── formulario.feature               # Escenarios de prueba en Gherkin
├── pages/
│   └── formulario1.py                   # Page Object Model (POM)
├── tests/
│   └── test_form.py                     # Implementación de pasos BDD
└── videos_evidencia/                    # Grabaciones de pruebas (generadas)
```

---

## 🔧 Tecnologías y Dependencias

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS o Linux

### Librerías Principales

| Librería | Versión | Propósito |
|----------|---------|----------|
| `playwright` | 1.62 | Automatización de navegador |
| `pytest` | 9.1.1 | Framework de testing |
| `pytest-bdd` | 8.1.0 | Soporte para especificaciones BDD |

---

## 📦 Instalación

### 1. Clonar o descargar el repositorio
```bash
git clone <url-del-repositorio>
cd PruebaTestBDDPlaywrightV1
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Instalar navegadores de Playwright
```bash
playwright install
```

---

## 🚀 Ejecución de Pruebas

### Ejecutar todas las pruebas
```bash
pytest
```

### Ejecutar pruebas con reporte detallado
```bash
pytest --bdd-report=report.html
```

### Ejecutar un escenario específico
```bash
pytest tests/test_form.py -k "Seleccionar género masculino"
```

### Ejecutar en modo headless (sin interfaz gráfica)
Edita `conftest.py` y cambia:
```python
browser = playwright.chromium.launch(headless=True)  # Cambiar a True
```

---

## 📝 Descripción de Archivos

### `conftest.py`
**Propósito**: Configuración central de pytest

**Contenido**:
- Fixtures de Playwright para gestión del navegador y páginas
- Funciones auxiliares para marcar capturas de pantalla
- Hooks de pytest para capturar resultados de pruebas
- Configuración de logging

**Fixtures principales**:
- `browser`: Instancia del navegador Chromium (scope: session)
- `page`: Página con grabación de video habilitada (scope: function)

---

### `features/formulario.feature`
**Propósito**: Definición de escenarios de prueba en Gherkin

**Formato**: Lenguaje Gherkin (legible por humanos)

**Escenarios**:
1. **Seleccionar género masculino**: Valida selección del radio button de género
2. **Seleccionar hobby deportes**: Valida selección del checkbox de hobby
3. **Calendario devuelve fecha por defecto**: Verifica la fecha predeterminada
4. **Cambiar fecha de nacimiento** (Scenario Outline): Prueba múltiples fechas con parametrización

---

### `pages/formulario1.py`
**Patrón**: Page Object Model (POM)

**Responsabilidades**:
- **Localizadores**: Define selectores XPath y CSS para todos los elementos
- **Acciones**: Métodos que interactúan con elementos (click, select, fill)
- **Validaciones**: Métodos que verifican estados de elementos (checked, value)
- **Auxiliares**: Métodos de utilidad (esperas, conversión de datos)

**Estructura de clases**:
```python
class FormularioPage:
    - Localizadores (atributos de instancia)
    - Métodos de navegación: go_to()
    - Métodos de acción: select_gender_male(), select_hobby_sports(), etc.
    - Métodos de validación: validate_gender_male_selected(), etc.
    - Métodos auxiliares: wait(), get_default_date(), etc.
```

**Ventajas del POM**:
- Reutilización de selectores
- Mantenimiento centralizado
- Cambios en selectores no requieren actualizar tests
- Código más legible y organizado

---

### `tests/test_form.py`
**Propósito**: Implementación de pasos BDD (step definitions)

**Estructura**:
- **Fixture**: `formulario_page()` - Navega a URL y crea instancia de POM
- **Steps GIVEN**: Precondiciones (estado inicial)
- **Steps WHEN**: Acciones del usuario
- **Steps THEN**: Validaciones y verificaciones

**Decoradores utilizados**:
- `@given()`: Define pasos precondición
- `@when()`: Define pasos de acción
- `@then()`: Define pasos de validación
- `@parsers.parse()`: Parametriza valores en los steps

---

## 🔄 Flujo de Ejecución

```
1. pytest carga conftest.py
   ↓
2. Fixture 'browser' crea navegador Chromium
   ↓
3. Por cada test:
   - Fixture 'page' crea nueva página con video recording
   - Fixture 'formulario_page' navega a URL y crea POM
   ↓
4. pytest-bdd carga feature files (formulario.feature)
   ↓
5. Para cada scenario:
   - Ejecuta pasos GIVEN (precondiciones)
   - Ejecuta pasos WHEN (acciones)
   - Ejecuta pasos THEN (validaciones)
   ↓
6. Captura resultado y videos en videos_evidencia/
   ↓
7. Genera reporte (si se especifica --bdd-report)
```

---

## 🎯 Conceptos Clave

### BDD (Behavior-Driven Development)
Enfoque de testing que enfatiza la colaboración entre desarrolladores, testers y stakeholders usando un lenguaje común (Gherkin).

**Estructura**:
- **Given** (Dado): Estado inicial
- **When** (Cuando): Acción
- **Then** (Entonces): Resultado esperado
- **And/But** (Y/Pero): Concatenación lógica

### Gherkin
Lenguaje de dominio específico (DSL) para escribir escenarios de prueba de forma legible:
```gherkin
Feature: Descripción de funcionalidad
  Scenario: Caso de prueba específico
    Given condición inicial
    When se realiza acción
    Then se verifica resultado
```

### Scenario Outline
Permite ejecutar el mismo escenario con múltiples conjuntos de datos:
```gherkin
Scenario Outline: Cambiar fecha
  Given precondición
  When selecciono año "<año>"
  
  Examples:
    | año  |
    | 2025 |
    | 2024 |
```

---

## 🔍 Elementos del Formulario de DemoQA

| Elemento | Tipo | XPath/Selector | Variable |
|----------|------|----------------|----------|
| Nombre | Text Input | `#firstName` | `name_input` |
| Apellido | Text Input | `#lastName` | `surname_input` |
| Email | Text Input | `#userEmail` | `email_input` |
| Género | Radio Buttons | `#gender-radio-1/2/3` | `genderMaleRadio`, etc. |
| Teléfono | Text Input | `#userNumber` | `phone_input` |
| Fecha Nac. | Date Picker | `#dateOfBirthInput` | `date_of_birth_input` |
| Hobbies | Checkboxes | `#hobbies-checkbox-1/2/3` | `sportsCheckbox`, etc. |
| Dirección | TextArea | `#currentAddress` | `address_textarea` |
| Estado | React-Select | `#state` | `state_dropdown` |
| Ciudad | React-Select | `#city` | `city_dropdown` |
| Enviar | Button | `#submit` | `submit_button` |

---

## 📊 Resultados y Evidencia

### Logs
- Nivel: INFO
- Formato: `YYYY-MM-DD HH:MM:SS [NIVEL] mensaje`
- Ubicación: Consola durante ejecución

### Grabaciones de Video
- Ubicación: `videos_evidencia/`
- Formato: .webm
- Generadas automáticamente por Playwright
- Útiles para debugging de pruebas fallidas

### Reportes
- Generados con: `pytest --bdd-report=report.html`
- Ubicación: `report.html` en el directorio raíz
- Incluye resumen de pasos y resultados

---

## 🐛 Debugging y Troubleshooting

### Pruebas lentas
- Verificar conexión a internet
- Aumentar timeouts en esperas explícitas
- Ejecutar sin headless para ver progreso en tiempo real

### Selectores no encontrados
- Usar `page.pause()` para pausar la ejecución
- Inspeccionar elementos con DevTools del navegador
- Verificar que los IDs no hayan cambiado en DemoQA

### Video recording falla
- Verificar que `videos_evidencia/` existe
- Comprobar permisos de escritura en la carpeta
- Verificar espacio en disco disponible

---

## 📚 Recursos y Referencias

- [Documentación de Playwright](https://playwright.dev/python/)
- [Documentación de pytest](https://docs.pytest.org/)
- [Documentación de pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [Especificación de Gherkin](https://cucumber.io/docs/gherkin/)
- [DemoQA Practice Automation Form](https://demoqa.com/automation-practice-form)

---

## 📝 Prácticas Recomendadas

✅ **Haz**:
- Usar Page Object Model para encapsular elementos
- Escribir steps pequeños y reutilizables
- Usar nombres descriptivos en localizadores
- Documentar casos de prueba complejos
- Ejecutar pruebas regularmente
- Usar waits explícitos en lugar de sleep()

❌ **No hagas**:
- Hardcodear URLs o selectores en steps
- Crear dependencies entre pruebas
- Usar sleep() para esperar elementos
- Ignorar failing tests
- Ejecutar pruebas en paralelo sin estado independiente

---

## 👤 Autor

**Proyecto de aprendizaje** - Suite de automatización BDD con Playwright y pytest

---

## 📄 Licencia

Este proyecto es de código abierto y disponible para propósitos educativos.
