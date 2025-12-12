import pytest
<<<<<<< HEAD
import pathlib
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    """
    Fixture que proporciona una instancia de WebDriver configurada.
    Se usa el scope="function" para que el navegador se inicie y cierre
    por cada test individual.
    """
    # Configuraciones del navegador
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") # Ventana maximizada
    # chrome_options.add_argument("--headless") # Descomentar para CI/CD 
    
    # Inicializar el driver (Selenium 4.x suele manejar el binario automáticamente)
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Espera implícita: red de seguridad para la sincronización 
    driver.implicitly_wait(5)
    
    # Entregar el control al test
    yield driver
    
    # Teardown: Limpieza que se ejecuta después del test, incluso si falla.
    print("\nCerrando navegador...")
    time.sleep(1)  # Pequeña pausa para ver el resultado localmente
    driver.quit()

# 1. Definir la ruta donde se guardarán las capturas
target = pathlib.Path('reports/screens')
target.mkdir(parents=True, exist_ok=True) # Crea la carpeta reports/screens si no existe

# 2. Hook de captura inteligente
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
=======
from selenium import webdriver
from pages.login_page import LoginPage
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def login_in_driver(driver,usuario,password):
    LoginPage(driver).abrir_pagina().login_completo(usuario,password)
    return driver

@pytest.fixture
def url_base():
    return "https://reqres.in/api/users"

@pytest.fixture
def header_request():
    return {"x-api-key": "reqres-free-v1"}
>>>>>>> b441d3ee5de032a142c0872ea3cfca91f1bc5660
