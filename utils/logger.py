import logging
import pathlib

# 1. Definir la ruta del archivo de log
# Usamos 'reports/logs' para que el artefacto sea más fácil de subir en GitHub Actions
audit_dir = pathlib.Path('reports/logs')
# Crear la carpeta si no existe
audit_dir.mkdir(parents=True, exist_ok=True)

log_file = audit_dir / 'suite.log'

# 2. Configuración del Logger (usando la lógica robusta de handlers)
logger = logging.getLogger("saucedemo_framework") # Usamos el nombre de la primera versión
logger.setLevel(logging.INFO)

# Esta verificación es crucial para evitar que Pytest agregue el handler múltiples veces
if not logger.handlers:
    # Handler que escribe el log en el archivo
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8") 

    # Formato del log
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Ahora la variable 'logger' está definida y exportada correctamente.