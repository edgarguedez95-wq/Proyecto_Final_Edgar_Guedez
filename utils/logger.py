import logging
import pathlib

<<<<<<< HEAD
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
=======
audit_dir = pathlib.Path('logs')
audit_dir.mkdir(exist_ok=True)

log_file = audit_dir/ 'suite.log'

logger = logging.getLogger("TalentoTech")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(log_file,mode="a", encoding="utf-8")

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
>>>>>>> b441d3ee5de032a142c0872ea3cfca91f1bc5660
