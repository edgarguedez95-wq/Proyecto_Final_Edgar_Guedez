# conftest.py
import pytest
import time
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# 1. Definir la ruta donde se guardarán las capturas
target = pathlib.Path('reports/screens')
target.mkdir(parents=True, exist_ok=True) 

# 2. Hook de captura inteligente (Clase 13)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Se ejecuta después de cada fase del test."""
    outcome = yield              
    report = outcome.get_result()  

    #  Solo captura en fallos de la fase principal (call)
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')  # Intenta obtener el driver
        if driver:
            # Crear nombre único para el archivo
            file_name = target / f"{item.name}.png"
            driver.save_screenshot(str(file_name))  # 📸 Captura
            
            #  Adjuntar al reporte HTML [32]
            if hasattr(report, 'extra'):
                # Si el reporte ya tiene una lista 'extra', agregamos la captura
                report.extra.append({
                    'name': 'Screenshot de Fallo',
                    'format': 'image',
                    'content': str(file_name)
                })

# 3. Hook para personalizar la tabla de resultados (opcional pero profesional)
def pytest_html_results_table_header(cells):
     cells.insert(2, 'URL')
     
def pytest_html_results_table_row(report, cells):
     cells.insert(2, getattr(report, 'page_url', '-'))


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
    # chrome_options.add_argument("--headless") # Descomentar para CI/CD (Clase 15)
    
    # Inicializar el driver (Selenium 4.x suele manejar el binario automáticamente)
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Espera implícita: red de seguridad para la sincronización (Clase 8)
    driver.implicitly_wait(5)
    
    # Entregar el control al test
    yield driver
    
    # Teardown: Limpieza que se ejecuta después del test, incluso si falla.
    print("\nCerrando navegador...")
    time.sleep(1)  # Pequeña pausa para ver el resultado localmente
    driver.quit()