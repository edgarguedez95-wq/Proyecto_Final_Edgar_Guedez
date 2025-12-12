import pytest 
from pages.login_page import LoginPage # Asegúrate de que esta importación sea correcta
from utils.logger import logger # Asegúrate de que esta importación sea correcta

from faker import Faker
fake = Faker()

def generar_datos_fallidos(num_casos=2):
    """Genera una lista de N tuplas con credenciales aleatorias."""
    datos = []
    for _ in range(num_casos):
        # Generamos un usuario y una clave aleatorios. 
        # El resultado esperado es False, ya que SauceDemo solo acepta credenciales fijas.
        datos.append((fake.user_name(), fake.password(length=10), False))
    return datos

# Definimos la lista de casos de prueba usando la función generadora
CASOS_FALLIDOS_FAKER = generar_datos_fallidos(2)


@pytest.mark.ui
@pytest.mark.parametrize("usuario, password, debe_funcionar", CASOS_FALLIDOS_FAKER)
def test_login_validation_faker(driver, usuario, password, debe_funcionar):
    """
    Verifica que las credenciales generadas aleatoriamente (Faker) 
    resulten en un error (comportamiento negativo esperado).
    """
    
    logger.info('TEST FAKER: Iniciando login con credenciales aleatorias')

    # 1. Configurar e Instanciar Page Object (usamos el fixture 'driver')
    login = LoginPage(driver)
    login.abrir()
    
    # 2. Realizar la acción de login con los datos generados
    # Nota: Asegúrate de que login_completo en LoginPage usa 'password' o 'clave'
    login.login_completo(usuario, password) 

    # 3. Lógica de validación (Asserts)
    
    # Como el valor de debe_funcionar es siempre False en este test,
    # verificamos que la validación de fallo sea exitosa.
    if not debe_funcionar:
        logger.info('Verificando mensaje de error tras intento de login aleatorio.')
        
        # Obtenemos el mensaje de error de la página
        mensaje_error = login.obtener_mensaje_error() 
        
        # Validamos que el mensaje de error de SauceDemo esté presente
        assert "Epic sadface" in mensaje_error, "Fallo: Se esperaba un error pero no se mostró el mensaje."
    
    logger.info('TEST FAKER: Finalizado.')