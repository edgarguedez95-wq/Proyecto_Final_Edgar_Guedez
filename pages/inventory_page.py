from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    # LOCATORS
    _TITLE = (By.CLASS_NAME, "title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Aseguramos que la página cargó esperando un elemento clave
        self.wait.until(EC.visibility_of_element_located(self._TITLE))

    def obtener_titulo(self):
        """Obtiene el título de la página de inventario, debe ser 'Products'."""
        return self.driver.find_element(*self._TITLE).text

    def obtener_productos(self):
        """Devuelve la lista de objetos web de productos."""
        return self.driver.find_elements(*self._PRODUCTS)

    def obtener_contador_productos_visibles(self):
        """Cuenta la cantidad de productos en el catálogo."""
        return len(self.obtener_productos())

    def agregar_primer_producto(self):
        """Encuentra y hace clic en el botón 'Add to cart' del primer producto."""
        # Se asume que el primer botón en la lista es el del primer producto
        primer_boton = self.driver.find_elements(*self._ADD_BUTTONS)
        if primer_boton:
            primer_boton[0].click()  # <--- ¡CORRECCIÓN APLICADA!
        
        # Devolvemos self para permitir el method chaining
        return self

    def obtener_contador_carrito(self) -> int:
        """Obtiene el número de productos en el badge del carrito."""
        try:
            badge = self.driver.find_element(*self._CART_BADGE)
            # Retorna el texto del badge, esperando que sea un número
            return int(badge.text)
        except:
            # Si el badge no existe (carrito vacío), retorna 0
            return 0

    def ir_al_carrito(self):
        """Navega a la página del carrito y retorna el objeto de la nueva página."""
        self.driver.find_element(*self._CART_LINK).click()
        # Importación lazy para evitar dependencias circulares (CartPage aún no existe)
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def hacer_logout(self):
        """Cierra la sesión del usuario."""
        self.driver.find_element(*self._MENU_BUTTON).click()
        logout_link = self.wait.until(
            EC.element_to_be_clickable(self._LOGOUT_LINK)
        )
        logout_link.click()
        return self # Opcionalmente, puedes retornar LoginPage