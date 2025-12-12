from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    # LOCATORS UNIFICADOS
    _TITLE = (By.CLASS_NAME, "title") 
    _INVENTORY_ITEMS = (By.CLASS_NAME,"inventory_item")
    _ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".inventory_item button")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")


    def __init__(self, driver):
        self.driver = driver 
        self.wait = WebDriverWait(driver, 10)
        # Espera hasta que el título de la página esté visible
        self.wait.until(EC.visibility_of_element_located(self._TITLE))

    def obtener_todos_los_productos(self):
        """Devuelve la lista de todos los objetos web de productos."""
        self.wait.until(EC.visibility_of_all_elements_located(self._INVENTORY_ITEMS)) 
        return self.driver.find_elements(*self._INVENTORY_ITEMS)
    
    def agregar_primer_producto(self):
        """Agrega el primer producto al carrito. (Soluciona el error de 'click' en lista)."""
        # Espera que los elementos sean visibles
        productos = self.wait.until(EC.visibility_of_all_elements_located(self._INVENTORY_ITEMS)) 

        # Busca el botón DENTRO del primer contenedor de producto y hace clic
        primer_boton_producto = productos[0].find_element(*self._ADD_TO_CART_BUTTON)
        primer_boton_producto.click()
        return self

    def obtener_contador_carrito(self) -> int:
        """Obtiene el número de productos en el badge del carrito."""
        try:
            self.wait.until(EC.visibility_of_element_located(self._CART_BADGE)) 
            contador_carrito = self.driver.find_element(*self._CART_BADGE)
            return int(contador_carrito.text)
        except:
            return 0
    
    def hacer_logout(self):
        """Cierra la sesión del usuario."""
        self.driver.find_element(*self._MENU_BUTTON).click()
        logout_link = self.wait.until(
            EC.element_to_be_clickable(self._LOGOUT_LINK)
        )
        logout_link.click()