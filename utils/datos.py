import csv
import pathlib

def leer_csv_login(ruta_archivo):
    """
    Lee un archivo CSV y devuelve una lista de tuplas
    para usar en parametrización de pytest.
    """
    datos = []
    # Usa pathlib para manejar rutas de forma segura en distintos SO
    ruta = pathlib.Path(ruta_archivo)
    
    with open(ruta, newline='', encoding='utf-8') as archivo:
        # Usamos DictReader para acceder a las columnas por nombre (usuario, clave, debe_funcionar)
        lector = csv.DictReader(archivo)
        for fila in lector:
            # 1. Convertir string 'True'/'False' a booleano
            debe_funcionar = fila['debe_funcionar'].lower() == 'true'
            # 2. Añadir la tupla (usuario, clave/password, resultado_esperado)
            # Nota: Asumo que la columna de la contraseña es 'clave' o 'password'. Usaré 'clave' de la versión HEAD.
            datos.append((fila['usuario'], fila['clave'], debe_funcionar)) 
            
    return datos

# Definición de la lista de casos de prueba para importación en los tests
CASOS_LOGIN = leer_csv_login('datos/login.csv')