import pandas as pd
from .preprocesamiento import Preprocesador

def cargar_corpus():
    biblia = pd.read_csv("api/datos/dataset_original/t_bbe.csv")
    libros = pd.read_csv("api/datos/dataset_original/key_english.csv")

    biblia = biblia.rename(columns={
        "field": "id",
        "field.1": "id_libro",
        "field.2": "capitulo",
        "field.3": "versiculo",
        "field.4": "texto"
    })

    libros = libros.rename(columns={
        "field": "id_libro",
        "field.1": "libro",
        "field.2": "testamento",
        "field.3": "id_genero"
    })

    corpus = pd.merge(biblia, libros, on="id_libro", how="left")
    corpus = corpus[["id", "id_libro", "libro", "testamento", "id_genero", "capitulo", "versiculo", "texto"]]

    return corpus

def procesar_corpus(corpus_original):
    corpus_procesado = corpus_original.copy()
    preprocesador = Preprocesador()

    tokens_procesados = []
    lista_tokens = []

    for texto in corpus_original["texto"]:
        _, tokens = preprocesador.preprocesar_texto(texto)
        tokens_procesados.append(" ".join(tokens))
        lista_tokens.append(tokens)

    corpus_procesado["tokens"] = tokens_procesados

    return corpus_procesado, lista_tokens