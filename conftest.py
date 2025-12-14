# conftest.py
import pytest
import time
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os # Necesario para verificar si estamos en un entorno de CI

# 1. Definir la ruta donde se guardarán las capturas
target = pathlib.Path('reports/screens')
target.mkdir(parents=True, exist_ok=True) 

# 2. Hook de captura inteligente (Clase 13)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Se ejecuta después de cada fase del test."""
    outcome = yield          
    report = outcome.get_result()   

    # Solo captura en fallos de la fase principal (call)
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')  # Intenta obtener el driver
        if driver:
            # Crear nombre único para el archivo
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            file_name = target / f"{item.name}_{timestamp}.png" # Mejorar nombre para evitar sobreescritura
            driver.save_screenshot(str(file_name))  # 📸 Captura
            
            # Adjuntar al reporte HTML
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
  
    chrome_options = Options()
    
    # 1. Detectar si estamos en un entorno de CI (como GitHub Actions)
    # La variable de entorno 'CI' se define automáticamente en GitHub Actions
    if os.environ.get('CI'):
        print("\nConfigurando Driver en modo Headless para CI/CD...")
        
        # 1.1 MODO HEADLESS (CRÍTICO para servidores sin interfaz gráfica)
        chrome_options.add_argument("--headless")
        
        # 1.2 Configuración para estabilidad en Linux (Necesario en Ubuntu/GitHub)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # 1.3 Maximizar ventana (Algunas versiones headless lo requieren)
        chrome_options.add_argument("--start-maximized") 
    else:
        # Modo local (Ventana visible)
        chrome_options.add_argument("--start-maximized") 
    
    # Inicializar el driver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Espera implícita: red de seguridad para la sincronización
    driver.implicitly_wait(10) # Aumentar un poco el wait es buena práctica en CI
    
    # Entregar el control al test
    yield driver
    
    # Teardown: Limpieza que se ejecuta después del test, incluso si falla.
    print("\nCerrando navegador...")
    # Quitar el time.sleep(1) en el teardown para CI/CD, ya que solo añade retraso
    driver.quit()