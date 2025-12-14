import logging
import pathlib

# 1. Definir la ruta del archivo de log
audit_dir = pathlib.Path('reports/logs')
# Crear la carpeta si no existe (importante para CI/CD)
audit_dir.mkdir(parents=True, exist_ok=True)

# 2. Configuración global del logging (nivel y formato)
logging.basicConfig(
    filename=audit_dir / 'suite.log', # Escribe en reports/logs/suite.log
    level=logging.INFO,             # Registra mensajes de nivel INFO y superior
    format='%(asctime)s %(levelname)s %(name)s – %(message)s',
    datefmt='%H:%M:%S'
)

# 3. Logger específico (se usará en los tests)
logger = logging.getLogger('saucedemo_framework')