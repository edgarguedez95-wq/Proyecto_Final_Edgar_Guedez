<<<<<<< HEAD
# pages/inventory_page.py
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
    
        primer_boton_list = self.driver.find_elements(*self._ADD_BUTTONS)

        if primer_boton_list:
            primer_boton_list[0].click() 
        else:
            raise Exception("Error: No se encontraron botones de 'Add to cart' en la página.")
         
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
=======
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class InventoryPage:

    # Selectores

    _INVENTORY_ITEMS = (By.CLASS_NAME,"inventory_item")
    _ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".inventory_item button")
    _CART_COUNT = (By.CLASS_NAME,"shopping_cart_badge")
    _ITEM_NAME = (By.CLASS_NAME,"inventory_item_name")
    _CART_LINK = (By.CLASS_NAME,"shopping_cart_link")

    def __init__(self,driver):
        self.driver = driver 
        self.wait = WebDriverWait(driver,10)

    def obtener_todos_los_productos(self):
        self.wait.until(EC.visibility_of_all_elements_located(self._INVENTORY_ITEMS)) 
        productos = self.driver.find_elements(*self._INVENTORY_ITEMS)
        return productos
    
    def obtener_nombres_productos(self):
        productos = self.driver.find_elements(*self._ITEM_NAME)
        return [producto_nombre.text for producto_nombre in productos]
    
    def agregar_primer_producto(self):
        productos = self.wait.until(EC.visibility_of_all_elements_located(self._INVENTORY_ITEMS)) 

        primer_boton_producto = productos[0].find_element(*self._ADD_TO_CART_BUTTON)
        primer_boton_producto.click()

    def agregar_producto_por_nombre(self,nombre_producto):

        productos = self.driver.find_elements(*self._INVENTORY_ITEMS)   

        for producto in productos:
            nombre = producto.find_element(*self._ITEM_NAME).text

            if nombre.strip() == nombre_producto.strip():
                boton = producto.find_element(*self._ADD_TO_CART_BUTTON)
                boton.click()
                return self
        
        raise Exception(f"No se encontro el producto {nombre_producto}")
            
    def abrir_carrito(self):
        self.wait.until(EC.element_to_be_clickable(self._CART_LINK)).click()
        return self
    
    def obtener_conteo_carrito(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self._CART_COUNT)) 
            contador_carrito = self.driver.find_element(*self._CART_COUNT)
            return int(contador_carrito.text)
        except:
            return 0
>>>>>>> b441d3ee5de032a142c0872ea3cfca91f1bc5660
