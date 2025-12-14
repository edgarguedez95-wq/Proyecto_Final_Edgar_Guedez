# tests/test_inventory.py
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import logger

# Importamos el fixture 'driver' de conftest.py

@pytest.fixture(scope="function")
def usuario_logueado(driver):
    """
    Fixture que asegura un estado inicial de 'Usuario logueado'.
    Retorna la instancia de la InventoryPage para usar en el test.
    """
    logger.info("SETUP: Preparando usuario logueado (standard_user)")
    login_page = LoginPage(driver)
    login_page.abrir()
    
    # Realizar login usando el Page Object Model
    login_page.login_completo("standard_user", "secret_sauce")
    
    # Retornamos el objeto de la página a la que fuimos redirigidos
    return InventoryPage(driver)


@pytest.mark.ui
@pytest.mark.smoke
def test_catalogo_visible(usuario_logueado: InventoryPage):
    """
    Verifica que el título sea correcto y que haya al menos 3 productos visibles.
    """
    logger.info("TEST: Verificando título y conteo de productos")

    # 1. Verificar el título
    titulo = usuario_logueado.obtener_titulo()
    assert titulo == 'Products', f"Título incorrecto: {titulo}"

    # 2. Verificar el conteo de productos
    conteo_productos = usuario_logueado.obtener_contador_productos_visibles()
    assert conteo_productos >= 3, f"Se esperaban al menos 3 productos, se encontraron {conteo_productos}"

    logger.info(f"VERIFICACION EXITOSA: {conteo_productos} productos encontrados.")


@pytest.mark.ui
def test_agregar_producto_a_carrito(usuario_logueado: InventoryPage):
    """
    Verifica que al agregar un producto, el contador del carrito se actualice a 1.
    """
    logger.info("TEST: Agregando el primer producto al carrito")

    # 1. Agregar el primer producto
    usuario_logueado.agregar_primer_producto()

    # 2. Verificar el contador del carrito (esperamos explícitamente el cambio)
    contador = usuario_logueado.obtener_contador_carrito()
    assert contador == 1, f"El contador del carrito debería ser 1, es {contador}"
    
    logger.info("VERIFICACION EXITOSA: Contador de carrito OK (valor 1).")
