import requests
from faker import Faker
import pytest
from utils.logger import logger # Importamos el logger

# URL Base para la simulación de Posts
BASE_URL = 'https://jsonplaceholder.typicode.com/posts'
fake = Faker()

def generar_payload_post():
    """Genera un cuerpo de post (payload) con datos aleatorios."""
    return {
        'title': fake.sentence(),
        'body': fake.text(),
        'userId': fake.random_int(1, 100)
    }