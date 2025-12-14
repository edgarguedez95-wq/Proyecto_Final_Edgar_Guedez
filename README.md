# Proyecto Final Integrador: Framework de Automatización QA (UI + API)

Este proyecto es un framework de automatización de pruebas completo desarrollado en Python, que integra pruebas de Interfaz de Usuario (UI) sobre SauceDemo y pruebas de API sobre JSONPlaceholder, demostrando dominio de Pytest, Page Object Model (POM) y estrategias de Integración Continua (CI/CD).

## Tecnologías y Patrones

El framework utiliza las siguientes tecnologías clave, cumpliendo con los requisitos del curso:

| Tecnología                  | Propósito                                                            |
| :-------------------------- | :------------------------------------------------------------------- |
| **Python**                  | Lenguaje de programación principal.                                  |
| **Pytest**                  | Framework de testing, manejo de fixtures y parametrización.          |
| **Selenium WebDriver**      | Automatización de pruebas de interfaz de usuario (UI).               |
| **Requests**                | Cliente HTTP para automatización de pruebas de API.                  |
| **Page Object Model (POM)** | Patrón de diseño para UI, asegurando mantenibilidad y escalabilidad. |
| **Data-Driven Testing**     | Separación de datos de prueba (CSV/JSON) de la lógica.               |
| **GitHub Actions**          | Configuración de Integración Continua (CI/CD).                       |

## Estructura del Proyecto

La organización del código sigue buenas prácticas de la industria, separando las responsabilidades de forma clara:

- `pages/`: Contiene todas las clases del **Page Object Model (POM)** (ej: `login_page.py`, `inventory_page.py`).
- `tests/`: Contiene los scripts de pruebas de **UI** (ej: `test_login.py`).
- `tests_api/`: Contiene los scripts de pruebas de **API** (ej: `test_crud_api.py`), cubriendo GET, POST, DELETE.
- `datos/`: Almacena los archivos de datos externos (`login.csv`) para parametrización.
- `utils/`: Funciones auxiliares (ej: `logger.py`, `api_client.py`).
- `reports/`: Almacena los reportes HTML, logs y capturas de pantalla automáticas.
- `.github/workflows/`: Contiene la configuración de **CI/CD** (`ci.yml`).

## Instalación y Configuración

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### 1. Requisitos Previos

Asegúrate de tener instalado Python y Git.

### 2. Clonar Repositorio

```bash
git clone https://github.com/TU_USUARIO/proyecto-final-automation-testing-[nombre-apellido].git
cd proyecto-final-automation-testing-[nombre-apellido]
```

### 3. Instalación de Dependencias

Instala todas las librerías necesarias (Pytest, Selenium, Requests, etc.) desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

## ▶Ejecución de Pruebas

Todos los tests se ejecutan usando Pytest.

| Objetivo                                                      | Comando                                                             |
| :------------------------------------------------------------ | :------------------------------------------------------------------ |
| **Ejecutar toda la suite (UI + API) y generar reporte final** | `pytest -v --html=reports/reporte_final.html --self-contained-html` |
| **Ejecutar solo tests de UI**                                 | `pytest tests/ -v`                                                  |
| **Ejecutar solo tests de API**                                | `pytest tests_api/ -v -m api`                                       |
| **Ejecutar solo Smoke Tests (UI y API)**                      | `pytest -v -m smoke`                                                |

## Observabilidad y Reportes

El framework está configurado para generar evidencia y facilitar la depuración:

1.  **Reporte HTML:** Al ejecutar el comando principal, el reporte se genera en `reports/reporte_final.html`, mostrando el estado, duración y detalle de cada test.
2.  **Logging Centralizado:** El archivo `reports/logs/suite.log` registra cronológicamente los pasos clave de la ejecución (nivel INFO y superior), útil para el análisis post-mortem de fallos.
3.  **Capturas Automáticas:** Si un test de UI falla, se genera automáticamente una captura de pantalla en `reports/screens/` y se adjunta al reporte HTML, proporcionando contexto visual inmediato del error.

## Integración Continua (CI/CD)

El pipeline está configurado en GitHub Actions (`.github/workflows/ci.yml`). El flujo se dispara automáticamente en cada **push** o **Pull Request** a las ramas `main` o `develop`, ejecutando la suite completa y generando los reportes como artefactos descargables.
