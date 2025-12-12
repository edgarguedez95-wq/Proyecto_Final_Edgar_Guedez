# tests_api/test_crud_api.py
import requests
import pytest

# Se asume que utils/api_client.py contiene BASE_URL y generar_payload_post
# Se asume que utils/logger.py contiene el objeto logger
from utils.api_client import BASE_URL, generar_payload_post
from utils.logger import logger


# ----------------- FIXTURE DE CICLO DE VIDA (CRUD) -----------------
@pytest.fixture(scope='function')
def post_creado():
    """
    Fixture que crea un post (SETUP) y lo elimina al finalizar el test (TEARDOWN).
    Esto permite encadenar peticiones y garantizar la limpieza del entorno.
    """
    payload = generar_payload_post()
    logger.info("FIXTURE SETUP: Creando post temporal para el test...")
    
    # 1. Ejecutar POST (SETUP)
    response = requests.post(BASE_URL, json=payload)
    
    # Validación interna de la creación para evitar contaminar el test si el setup falla
    if response.status_code != 201:
        pytest.fail(f"Fallo en la creación del recurso, status: {response.status_code}")
        
    post_id = response.json().get('id')
    
    yield post_id # Entrega el ID al test
    
    # 2. Ejecutar DELETE (TEARDOWN - Se ejecuta siempre)
    logger.info("FIXTURE TEARDOWN: Eliminando post temporal ID: %s", post_id)
    requests.delete(f'{BASE_URL}/{post_id}') 


# --------------------- CASOS DE PRUEBA API (GET, POST, DELETE) ---------------------

@pytest.mark.api
@pytest.mark.smoke
def test_get_resource():
    """Caso 1: GET - Obtener un recurso existente (Post ID 1) [1]."""
    logger.info("TEST API (GET): Iniciando consulta para post ID 1")
    
    # Realizar la petición GET
    response = requests.get(f'{BASE_URL}/1')
    
    # Nivel 1: Status Code [2]
    assert response.status_code in [200, 204]
    
    # Nivel 3: Estructura JSON - debe contener las claves básicas (id, title, body, userId) [3]
    data = response.json()
    expected_keys = {'id', 'title', 'body', 'userId'}
    assert expected_keys <= set(data.keys()) 
    
    # Nivel 4: Contenido - validar el ID [3]
    assert data['id'] == 1 

    logger.info("TEST API (GET): Consulta exitosa.")


@pytest.mark.api
def test_post_create_resource():
    """Caso 2: POST - Crear un nuevo recurso [1, 4]."""
    payload = generar_payload_post()
    logger.info("TEST API (POST): Creando nuevo post con datos aleatorios.")
    
    # Realizar la petición POST
    response = requests.post(BASE_URL, json=payload)
    
    # Nivel 1: Status Code (201 Created) [5]
    assert response.status_code == 201 
    
    # Nivel 4: Contenido - El recurso creado debe reflejar los datos enviados
    new_post = response.json()
    assert new_post['title'] == payload['title']
    assert 'id' in new_post and new_post.get('id') is not None

    logger.info("TEST API (POST): Recurso creado exitosamente.")


@pytest.mark.api
@pytest.mark.e2e
def test_delete_created_resource(post_creado):
    """
    Caso 3: DELETE - Usa el ID del recurso creado por el fixture [6, 7].
    Valida la eliminación del post [8].
    """
    post_id = post_creado
    logger.info("TEST API (DELETE): Eliminando post recién creado ID: %s", post_id)
    
    # Realizar la petición DELETE
    response = requests.delete(f'{BASE_URL}/{post_id}')
    
    # Nivel 1: Status Code (200 o 204) [9]
    assert response.status_code in [10, 11]
    
    # Nivel 3: Validación de cuerpo vacío (confirmación de eliminación) [9, 12]
    assert response.json() == {} 
    
    logger.info("TEST API (DELETE): Eliminación exitosa para ID: %s", post_id)