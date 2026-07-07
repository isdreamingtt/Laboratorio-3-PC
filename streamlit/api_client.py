import os
import requests
from dotenv import load_dotenv


ruta_env = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ruta_env)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def api_get(base_url: str, path: str, params: dict | None = None):
    respuesta = requests.get(
        f"{base_url.rstrip('/')}{path}",
        params=params,
        timeout=30
    )

    respuesta.raise_for_status()
    return respuesta.json()


def obtener_dashboard(parametros):
    return api_get(API_URL, "/dashboard", parametros)

def buscar_versiculos(consulta, k, modelo):
    parametros = {
        "consulta": consulta,
        "k": k, #numero de resultados a consultar.
        "modelo": modelo #esto es para poder cambiar el modeo, entre tf-idf y word2vec.
    }

    return api_get(API_URL, "/buscar", parametros)

def obtener_pca_tfidf(dimensiones):
    parametros = {
        "dimensiones": dimensiones
    }

    return api_get(API_URL, "/pca-tfidf", parametros)


def obtener_pca_word2vec(dimensiones):
    parametros = {
        "dimensiones": dimensiones
    }

    return api_get(API_URL, "/pca-word2vec", parametros)

def generar_versiculo(modelo, palabra_inicial, max_palabras, cantidad_resultados):
    parametros = {
        "modelo": modelo,
        "palabra_inicial": palabra_inicial,
        "max_palabras": max_palabras,
        "cantidad_resultados": cantidad_resultados
    }

    return api_get(API_URL, "/generar", parametros)