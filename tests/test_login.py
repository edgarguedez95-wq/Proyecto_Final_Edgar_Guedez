import pytest
from pages.login_page import LoginPage
from utils.datos import CASOS_LOGIN
from utils.logger import logger

# Pytest inyectará el fixture 'driver' automáticamente
# y el decorador ejecutará la función una vez por cada tupla en CASOS_LOGIN

@pytest.mark.ui
@pytest.mark.parametrize("usuario, clave, debe_funcionar", CASOS_LOGIN)
def test_login_ddt(driver, usuario, clave, debe_funcionar):
    """
    Test parametrizado de login usando datos del archivo datos/login.csv.
    Cubre escenarios de éxito (debe_funcionar=True) y fallo (debe_funcionar=False).
    """
    
    # 1. Configurar y Abrir la página usando el Page Object
    login = LoginPage(driver)
    login.abrir()
    
    logger.info('Iniciando login con usuario: %s', usuario)

    # 2. Realizar la acción de login
    login.login_completo(usuario, clave)

    # 3. Lógica de validación condicional (Asserts)
    if debe_funcionar:
        # Si el login debe ser exitoso:
        # Verificamos que la URL contenga el path del inventario (inventario.html)
        logger.info('Verificando login exitoso. URL esperada: inventory.html')
        assert "inventory.html" in driver.current_url
    else:
        # Si el login debe fallar (usuario bloqueado o credenciales erróneas):
        # Verificamos que no haya cambiado la URL y que el mensaje de error esté visible
        logger.info('Verificando login fallido. Error esperado.')
        assert login.hay_error()

    logger.info('Test finalizado para el usuario: %s', usuario)