from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time # Solo para pausas de debugging si es necesario

class LoginPage:
    # 1. IDENTIDAD DE LA PÁGINA
    URL = "https://www.saucedemo.com/" # Centraliza la URL [4]

    # 2. LOCATORS (Privados y Centralizados)
    # Si los selectores cambian en SauceDemo, solo editas aquí [5]
    _USER_INPUT   = (By.ID,   "user-name")
    _PASS_INPUT   = (By.ID,   "password")
    _LOGIN_BUTTON = (By.ID,   "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']") # Selector para el mensaje de error [6]

    def __init__(self, driver):
        """Constructor que recibe la instancia del WebDriver del conftest.py [5]."""
        self.driver = driver
        # Inicializa una espera explícita para usar en pasos críticos [6]
        self.wait = WebDriverWait(driver, 10)

    def abrir(self):
        """Carga la URL de login en el navegador [7]."""
        self.driver.get(self.URL)
        return self

    def completar_usuario(self, usuario: str):
        """Escribe el nombre de usuario, esperando que el campo sea visible [7, 8]."""
        campo = self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        campo.clear()
        campo.send_keys(usuario)
        return self

    def completar_clave(self, clave: str):
        """Escribe la contraseña [8, 9]."""
        campo = self.driver.find_element(*self._PASS_INPUT)
        campo.clear()
        campo.send_keys(clave)
        return self
    
    def hacer_clic_login(self):
        """Hace clic en el botón Login [9, 10]."""
        self.driver.find_element(*self._LOGIN_BUTTON).click()
        return self

    def login_completo(self, usuario, clave):
        """Método de conveniencia para hacer login completo (acción de negocio) [10, 11]."""
        self.completar_usuario(usuario)
        self.completar_clave(clave)
        self.hacer_clic_login()
        return self

    def hay_error(self) -> bool:
        """Verificar si hay un mensaje de error visible (para tests negativos) [10, 11]."""
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            return True
        except:
            return False

    def obtener_mensaje_error(self) -> str:
        """Obtener el texto del mensaje de error [12, 13]."""
        if self.hay_error():
            return self.driver.find_element(*self._ERROR_MESSAGE).text
        return ""