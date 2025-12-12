import pytest
from pages.login_page import LoginPage
from utils.datos import CASOS_LOGIN
from utils.logger import logger

# ----------------------------------------------------------------------
# NOTA: Pytest inyectará el fixture 'driver' y la prueba se ejecutará 
# una vez por cada tupla en CASOS_LOGIN
# ----------------------------------------------------------------------

@pytest.mark.ui
@pytest.mark.parametrize("usuario, clave, debe_funcionar", CASOS_LOGIN)
def test_login_ddt(driver, usuario, clave, debe_funcionar):
    """
    Test parametrizado de login usando Data Driven Testing (DDT) 
    con datos de utils/datos.py.
    """
    
    # 1. Configurar y Abrir la página usando el Page Object
    login = LoginPage(driver)
    
    # Usamos el método 'abrir' o 'abrir_pagina' si lo unificaste así
    # Basado en tu código de LoginPage limpio: usa 'abrir()'
    login.abrir() 
    
    logger.info('Iniciando login con usuario: %s', usuario)

    # 2. Realizar la acción de login
    # Nota: Asegúrate de que login_completo en LoginPage usa 'clave' o 'password' consistentemente.
    login.login_completo(usuario, clave) 

    # 3. Lógica de validación condicional (Asserts)
    if debe_funcionar:
        # Si el login debe ser exitoso:
        logger.info('Verificando login exitoso. URL esperada: inventory.html')
        assert "inventory.html" in driver.current_url, "Fallo: No se redirigió a la página de inventario."
    else:
        # Si el login debe fallar (usuario bloqueado o credenciales erróneas):
        logger.info('Verificando login fallido. Error esperado.')
        assert login.hay_error(), "Fallo: Se esperaba un error pero no se mostró el mensaje."

    logger.info('Test de login finalizado para el usuario: %s', usuario)