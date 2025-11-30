from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest 

from utils.datos import leer_csv_login
from pages.login_page import LoginPage

from utils.logger import logger


@pytest.mark.parametrize("usuario,password,debe_funcionar",leer_csv_login("datos/data_login.csv"))
def test_login_validation(login_in_driver,usuario,password,debe_funcionar):
    logger.info("Completando con los datos de usuario")
    driver = login_in_driver

    if debe_funcionar == True:
        logger.info("verficando redireccionamiento dentro de la pagina")
        assert "/inventory.html" in driver.current_url, "No se redirgio al inventario"
        logger.info("test de login completado")
    elif debe_funcionar == False:
        mensaje_error = LoginPage(driver).obtener_error()
        assert "Epic sadface" in mensaje_error, "el mensaje de error no se esta mostrando"



