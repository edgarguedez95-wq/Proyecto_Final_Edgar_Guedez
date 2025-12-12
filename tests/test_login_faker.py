# tests/test_login_faker.py

from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest 

from pages.login_page import LoginPage
from utils.logger import logger 

from faker import Faker
fake = Faker()


@pytest.mark.ui # Asegúrate de que tienes esta marca
@pytest.mark.parametrize("usuario, password, debe_funcionar", [
    # Credenciales aleatorias que siempre deben fallar
    (fake.user_name(), fake.password(length=10), False),
    (fake.user_name(), fake.password(length=8), False),
])
def test_login_validation_faker(driver, usuario, password, debe_funcionar):
    """
    Verifica que las credenciales generadas aleatoriamente (Faker) 
    resulten en un error (comportamiento negativo esperado).
    """
    
    logger.info('TEST FAKER: Iniciando login con credenciales aleatorias')

    # 1. Configurar e Instanciar Page Object (usa el fixture 'driver')
    login = LoginPage(driver)
    login.abrir()
    
    # 2. Realizar la acción de login con los datos generados
    login.login_completo(usuario, password)

    # 3. Lógica de validación (Asserts)
    
    if debe_funcionar == True:
        # Bloque que nunca se ejecutará, pero está aquí por si acaso
        assert "/inventory.html" in driver.current_url, "No se redirigio al inventario"
    else:
        # Esperamos el error porque las credenciales no son válidas
        mensaje_error = login.obtener_mensaje_error() 
        assert "Epic sadface" in mensaje_error, "El mensaje de error no se está mostrando para credenciales inválidas."

    logger.info('TEST FAKER: Finalizado.')