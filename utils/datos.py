import csv
import pathlib

def leer_csv_login(ruta_archivo):
    """
    Lee un archivo CSV y devuelve una lista de tuplas
    para usar en parametrización de pytest [20].
    """
    datos = []
    # Usa pathlib para manejar rutas de forma segura en distintos SO
    ruta = pathlib.Path(ruta_archivo)
    
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Convertir string 'True'/'False' a booleano, esencial para la validación condicional [20]
            debe_funcionar = fila['debe_funcionar'].lower() == 'true'
            # Añadir la tupla (usuario, clave, resultado_esperado)
            datos.append((fila['usuario'], fila['clave'], debe_funcionar))
            
    return datos

# Definición de la lista de casos de prueba para importación
CASOS_LOGIN = leer_csv_login('datos/login.csv')