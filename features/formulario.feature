Feature: Registro de estudiante en demoqa

  Scenario: Seleccionar género masculino
    Given estoy en la página de registro
    When selecciono el género masculino
    Then el radio masculino debe estar marcado
  
  Scenario: Seleccionar hobby deportes
    Given estoy en la página de registro
    When selecciono el hobby deportes
    Then el checkbox deportes debe estar marcado

  Scenario: El Calendar devuelve la fecha por defecto
    Given estoy en la página de registro
    When selecciono el Date of Birth
    Then calendar me devuelve la fecha por default

  Scenario Outline: Cambiar la fecha de nacimiento por una anterior
    Given estoy en la página de registro
    When selecciono el campo Date of Birth
    And elijo el año "<año>"
    And elijo el mes "<mes>"
    And elijo el día "<día>"
    Then el calendario muestra la fecha "<día> <mes> <año>"

    Examples:
      | mes   | día | año  |
      | July  | 10  | 2025 |
      | June  | 15  | 2024 |
      | May   | 20  | 2023 |




