from fastapi import FastAPI
from .corpus_loader import cargar_corpus, procesar_corpus
from .preprocesamiento import Preprocesador
from typing import Optional
from .tfidf import CalculadorTFIDF
from .procesador_semantico import BuscadorSemantico
from sklearn.decomposition import PCA
import numpy as np
from gensim.models import Word2Vec
from .generador_ngramas import GeneradorNGramas

app = FastAPI()

corpus_original = cargar_corpus()
corpus, lista_tokens = procesar_corpus(corpus_original)
preprocesador = Preprocesador()
calculador_tfidf = CalculadorTFIDF()
matriz_tfidf = calculador_tfidf.calcular_tfidf_corpus(lista_tokens)
buscador = BuscadorSemantico(corpus, matriz_tfidf, preprocesador, calculador_tfidf)
modelo_word2vec = Word2Vec(sentences=lista_tokens, vector_size=100, window=5, min_count=1, workers=4)
generador_ngramas = GeneradorNGramas()
generador_ngramas.entrenar(lista_tokens)

@app.get("/")
def home():
    return {"mensaje": "API funcionando"}

@app.get("/test-corpus")
def test_corpus():
    return {
        "cantidad_versiculos": len(corpus),
        "cantidad_libros": corpus["libro"].nunique(),
        "primer_texto": corpus["texto"].iloc[0],
        "primer_texto_tokens": corpus["tokens"].iloc[0]
    }
    
    #"gola"

@app.get("/dashboard")
def dashboard(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    datos = corpus

    if testamento:
        datos = datos[datos["testamento"] == testamento]

    if libro:
        datos = datos[datos["libro"] == libro]

    if capitulo is not None:
        datos = datos[datos["capitulo"] == capitulo]

    cantidad_por_libro = datos.groupby("libro").size().to_dict()

    longitudes = datos["tokens"].astype(str).apply(lambda texto: len(texto.split()))
    longitudes = longitudes.astype(int)

    datos_con_longitud = datos.copy()
    datos_con_longitud["longitud"] = longitudes

    longitud_promedio_por_libro = (datos_con_longitud.groupby("libro")["longitud"].mean())

    longitud_promedio_por_libro = longitud_promedio_por_libro.round(2).to_dict()

    todas_las_palabras = " ".join(datos["tokens"].astype(str)).split()

    frecuencias = {}

    for palabra in todas_las_palabras:
        if palabra not in frecuencias:
            frecuencias[palabra] = 1
        else:
            frecuencias[palabra] += 1

    frecuencias_ordenadas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)

    top_palabras = []

    for palabra, frecuencia in frecuencias_ordenadas[:20]:
        top_palabras.append({
            "palabra": palabra,
            "frecuencia": int(frecuencia)
        })

    return {
        "cantidad_por_libro": cantidad_por_libro,
        "longitud_promedio_por_libro": longitud_promedio_por_libro,
        "top_palabras": top_palabras
    }

@app.get("/buscar")
def buscar(consulta: str, k: int = 10):
    resultados = buscador.buscar(consulta, k)

    resultados_limpios = []
    for r in resultados:
        resultados_limpios.append({
            "libro": r["libro"],
            "capitulo": int(r["capitulo"]),
            "versiculo": int(r["versiculo"]),
            "texto": r["texto"],
            "similitud": float(r["similitud"])
        })

    return {"resultados": resultados_limpios}

@app.get("/pca-tfidf")
def pca_tfidf(dimensiones: int = 2):
    vocabulario = sorted(calculador_tfidf.idf.keys())
    vocab_index = {palabra: i for i, palabra in enumerate(vocabulario)}

    n_docs = len(matriz_tfidf)
    n_vocab = len(vocabulario)
    matriz_densa = np.zeros((n_docs, n_vocab))

    for i, vector in enumerate(matriz_tfidf):
        for palabra, valor in vector.items():
            if palabra in vocab_index:
                matriz_densa[i][vocab_index[palabra]] = valor

    pca = PCA(n_components=dimensiones)
    coordenadas = pca.fit_transform(matriz_densa)

    puntos = []
    for i in range(len(coordenadas)):
        punto = {
            "libro": corpus["libro"].iloc[i],
            "testamento": corpus["testamento"].iloc[i],
            "texto": corpus["texto"].iloc[i]
        }
        for d in range(dimensiones):
            punto[f"componente_{d+1}"] = float(coordenadas[i][d])
        puntos.append(punto)

    return {
        "varianza_explicada": pca.explained_variance_ratio_.tolist(),
        "puntos": puntos
    }

@app.get("/pca-word2vec")
def pca_word2vec(dimensiones: int = 2):
    vectores_versiculos = []

    for tokens in lista_tokens:
        vectores_palabras = [modelo_word2vec.wv[palabra] for palabra in tokens if palabra in modelo_word2vec.wv]

        if len(vectores_palabras) > 0:
            vector_promedio = np.mean(vectores_palabras, axis=0)
        else:
            vector_promedio = np.zeros(modelo_word2vec.vector_size)

        vectores_versiculos.append(vector_promedio)

    matriz_vectores = np.array(vectores_versiculos)

    pca = PCA(n_components=dimensiones)
    coordenadas = pca.fit_transform(matriz_vectores)

    puntos = []
    for i in range(len(coordenadas)):
        punto = {
            "libro": corpus["libro"].iloc[i],
            "testamento": corpus["testamento"].iloc[i],
            "texto": corpus["texto"].iloc[i]
        }
        for d in range(dimensiones):
            punto[f"componente_{d+1}"] = float(coordenadas[i][d])
        puntos.append(punto)

    return {
        "varianza_explicada": pca.explained_variance_ratio_.tolist(),
        "puntos": puntos
    }

@app.get("/generar")
def generar(modelo: str, palabra_inicial: str, max_palabras: int = 20):
    palabra_inicial = palabra_inicial.lower()

    if palabra_inicial not in generador_ngramas.unigramas:
        return {"error": "La palabra inicial no está en el vocabulario del corpus"}

    if modelo == "unigrama":
        texto = generador_ngramas.generar_unigrama(palabra_inicial, max_palabras)
    elif modelo == "bigrama":
        texto = generador_ngramas.generar_bigrama(palabra_inicial, max_palabras)
    elif modelo == "trigrama":
        texto = generador_ngramas.generar_trigrama(palabra_inicial, max_palabras)
    elif modelo == "cuatrigrama":
        texto = generador_ngramas.generar_cuatrigrama(palabra_inicial, max_palabras)
    else:
        return {"error": "Modelo no válido. Usa: unigrama, bigrama, trigrama o cuatrigrama"}

    return {"modelo": modelo, "texto_generado": texto}