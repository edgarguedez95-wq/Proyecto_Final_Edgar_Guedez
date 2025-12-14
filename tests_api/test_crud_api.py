import requests
import pytest
import time
from utils.api_client import BASE_URL, generar_payload_post
from utils.logger import logger

@pytest.mark.api
@pytest.mark.smoke
def test_get_resource():
    """Caso 1: GET - Obtener un recurso existente (Post ID 1) [16]."""
    logger.info("TEST API: Iniciando consulta GET para post ID 1")
    response = requests.get(f'{BASE_URL}/1')
    
    # Nivel 1: Status Code [17]
    assert response.status_code == 200 
    
    # Nivel 3: Estructura JSON - debe contener las claves [18]
    data = response.json()
    assert {'id', 'title', 'body', 'userId'} <= set(data.keys()) 
    
    # Nivel 4: Contenido - validar que el ID es 1
    assert data['id'] == 1 

    # Nivel 5: Performance (opcional) [19]
    assert response.elapsed.total_seconds() < 1.5 
    logger.info("TEST API: GET exitoso.")


@pytest.mark.api
def test_post_create_resource():
    """Caso 2: POST - Crear un nuevo recurso [20]."""
    payload = generar_payload_post()
    logger.info("TEST API: Creando nuevo post vía POST.")
    response = requests.post(BASE_URL, json=payload)
    
    # Nivel 1: Status Code [21]
    assert response.status_code == 201 
    
    # Nivel 4: Contenido - El recurso creado debe reflejar el título enviado [21]
    new_post = response.json()
    assert new_post['title'] == payload['title']
    assert 'id' in new_post and new_post['id'] is not None

    logger.info("TEST API: POST exitoso. Recurso creado con ID: %s", new_post.get('id'))



@pytest.fixture(scope='function')
def post_creado():
    """
    Fixture que crea un post (SETUP) y devuelve su ID. 
    Se encarga de la limpieza (TEARDOWN) al finalizar el test.
    Esto garantiza tests independientes y un flujo CRUD realista [8].
    """
    payload = generar_payload_post()
    logger.info("FIXTURE: Creando post temporal para el test...")
    response = requests.post(BASE_URL, json=payload)
    
    # Validamos creación (Status 201)
    if response.status_code != 201:
        pytest.fail(f"Fallo al crear recurso, status: {response.status_code}")
        
    post_id = response.json().get('id')
    
    yield post_id # Entrega el ID al test que lo solicite
    
    # TEARDOWN: Eliminación automática al terminar el test
    logger.info("FIXTURE: Eliminando post temporal ID: %s", post_id)
    requests.delete(f'{BASE_URL}/{post_id}') 


# --------------------- CASOS DE PRUEBA API ---------------------

@pytest.mark.api
@pytest.mark.smoke
def test_get_resource():
    """Caso 1: GET - Obtener un recurso existente."""
    logger.info("TEST API: Iniciando consulta GET para post ID 1")
    response = requests.get(f'{BASE_URL}/1')
    
    # Nivel 1: Status Code [9]
    assert response.status_code == 200 
    
    # Nivel 3: Estructura JSON - debe contener las claves [10]
    data = response.json()
    assert {'id', 'title', 'body', 'userId'} <= set(data.keys()) 
    
    # Nivel 4: Contenido - validar que el ID es 1 [11]
    assert data['id'] == 1 
    
    logger.info("TEST API: GET exitoso.")


@pytest.mark.api
def test_post_create_resource():
    """Caso 2: POST - Crear un nuevo recurso."""
    payload = generar_payload_post()
    logger.info("TEST API: Creando nuevo post vía POST.")
    response = requests.post(BASE_URL, json=payload)
    
    # Nivel 1: Se espera 201 Created [12]
    assert response.status_code == 201 
    
    # Nivel 4: Contenido - El recurso creado debe reflejar el título enviado [12]
    new_post = response.json()
    assert new_post['title'] == payload['title']
    assert 'id' in new_post and new_post['id'] is not None

    logger.info("TEST API: POST exitoso. ID: %s", new_post.get('id'))


@pytest.mark.api
@pytest.mark.e2e
def test_delete_created_resource(post_creado):
    """
    Caso 3: DELETE - Usa el ID del recurso creado por el fixture (post_creado).
    Este test valida que el ciclo de vida (POST -> DELETE) funcione [13].
    """
    post_id = post_creado
    logger.info("TEST API: Eliminando post recién creado ID: %s", post_id)
    
    response = requests.delete(f'{BASE_URL}/{post_id}')
    
    # Nivel 1: Status Code (200 o 204) [14]
    assert response.status_code in [200, 204]
    
    # Nivel 3: Validación de cuerpo vacío (simulando eliminación) [17]
    assert response.json() == {} 
    
    logger.info("TEST API: DELETE exitoso. Ciclo de vida completo validado para ID: %s", post_id)