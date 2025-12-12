import pytest
import pathlib
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage # Necesario para la fixture de login

# --- FIXTURES DE INTERFAZ DE USUARIO (UI) ---

@pytest.fixture(scope="function")
def driver():
    """
    Fixture que proporciona una instancia de WebDriver configurada (UI).
    Se usa el scope="function" para que el navegador se inicie y cierre
    por cada test individual.
    """
    # Configuraciones del navegador
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") # Ventana maximizada
    # Para GitHub Actions (CI), descomentar la siguiente línea:
    # chrome_options.add_argument("--headless") 
    
    # Inicializar el driver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Espera implícita
    driver.implicitly_wait(5)
    
    # Entregar el control al test
    yield driver
    
    # Teardown: Limpieza que se ejecuta después del test
    print("\nCerrando navegador...")
    time.sleep(1)
    driver.quit()

@pytest.fixture
def login_in_driver(driver, usuario, password):
    """Fixture que abre la página e inicia sesión para pruebas UI."""
    LoginPage(driver).abrir_pagina().login_completo(usuario, password)
    return driver

# --- FIXTURES DE API ---

@pytest.fixture
def url_base():
    """Retorna la URL base para las pruebas de API."""
    return "https://reqres.in/api/users"

@pytest.fixture
def header_request():
    """Retorna el header de autenticación/API Key para las peticiones API."""
    # Nota: Asegúrate de que la clave de tu header sea la que esperas (ej. "x-api-key")
    return {"X-Api-Key": "reqres-free-v1"}

# --- HOOKS PARA REPORTES Y CAPTURAS DE PANTALLA ---

# 1. Definir la ruta donde se guardarán las capturas
target = pathlib.Path('reports/screens')
target.mkdir(parents=True, exist_ok=True) # Crea la carpeta reports/screens si no existe

# 2. Hook de captura inteligente (Se ejecuta en caso de fallo)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Se ejecuta después de cada fase (setup/call/teardown) de cada test."""
    outcome = yield 
    report = outcome.get_result() 

    # Solo capturamos en fallos de la fase principal (call)
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')  # Intenta obtener el driver
        if driver:
            # Crear nombre único para el archivo (usa el nombre del test)
            file_name = target / f"{item.name}.png"
            driver.save_screenshot(str(file_name))  # Captura la pantalla
            
            # Adjuntar la captura al reporte HTML
            if hasattr(report, 'extra'):
                report.extra.append({
                    'name': 'Screenshot de Fallo',
                    'format': 'image',
                    'content': str(file_name)
                })