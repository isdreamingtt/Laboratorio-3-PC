# Laboratorio 3 - Streamlit

## Objetivo del laboratorio

Desarrollar un sistema cliente-servidor orientado al análisis y visualización interactiva del corpus bíblico,
utilizando una API para realizar el procesamiento textual y una aplicación Streamlit para la presentación
y exploración de resultados.

---

## Integrantes

- Harold Ramos
- Cristian Perez

---

## Estructura del proyecto

```text
Laboratorio 3 PC/
│
├── api/
│   ├── main.py
│   ├── corpus_loader.py
│   ├── preprocesamiento.py
│   ├── tfidf.py
│   ├── similitud_coseno.py
│   ├── procesador_semantico.py
│   ├── generador_ngramas.py
│   ├── visualizador.py
│   ├── requirements_api.txt
│   └── datos/
│       └── dataset_original/
│       |   ├── t_bbe.csv
│       |   └── key_english.csv
|       └── dataset_procesado/
│             
├── streamlit/
│   ├── main.py
│   ├── api_client.py
│   ├── requirements_app.txt
│   ├── .env
│   └── views/
│       ├── dashboard.py
│       ├── buscador.py
│       ├── visualizador.py
│       └── generador.py
│
└── README.md
```

---

## Requisitos

Para ejecutar el proyecto se necesita tener instalado:

- Python 3.10 o superior
- pip
- Un navegador web

---

## Instalación

Desde la raíz del proyecto, entrar a la carpeta `api/` y crear un entorno virtual:

```bash
conda create -n api
```

Activar el entorno virtual en Anaconda Prompt:

```bash
conda activate api
```

Instalar las dependencias de la API:

```bash
pip install -r requirements_api.txt
```

Desde la raíz del proyecto, entrar a la carpeta `streamlit/` y crear un entorno virtual:

```bash
conda create -n app
```

Activar el entorno virtual en Anaconda Prompt:

```bash
conda activate app
```

Instalar las dependencias de la aplicación Streamlit:

```bash
pip install -r requirements_app.txt
```

---

## Configuración de la aplicación

Dentro de la carpeta `streamlit/` debe existir un archivo `.env` con la URL de la API:

```env
API_URL=http://127.0.0.1:8000
```

---

## Ejecución del proyecto

Para ejecutar correctamente el sistema se deben abrir dos terminales Anaconda Prompt.

### Terminal 1: levantar la API

Desde la raíz del proyecto en la carpeta de `api/`:

```bash
conda activate api
cd ..
uvicorn api.main:app --reload
```

También se puede revisar la documentación automática de FastAPI en:

```text
http://127.0.0.1:8000/docs
```

---

### Terminal 2: levantar la app Streamlit

Desde la raíz del proyecto, en la carpeta `streamlit/`:

```bash
conda activate app
streamlit run main.py
```

La aplicación se abrirá en el navegador, normalmente en:

```text
http://localhost:8501
```

---

## Funcionalidades principales

### 1. Dashboard principal

La instancia que se encarga de mostrar las estadísticas de corpus.

Esta incluye:

- Cantidad de versículos por libro.
- Longitud promedio de versículos por libro.
- Palabras más frecuentes.
- Nube de palabras.
- Filtros por testamento, libro y capítulo.

---

### 2. Buscador semántico

Permite ingresar una frase y buscar los versículos más similares.

El sistema permite usar dos enfoques:

- TF-IDF + similitud coseno.
- Word2Vec + similitud coseno.

---

### 3. Visualización PCA y Word2Vec

Permite visualizar los versículos como puntos en un espacio reducido usando PCA.

Se pueden comparar dos representaciones:

- TF-IDF + PCA.
- Word2Vec + PCA.

También se puede elegir entre visualización 2D y 3D.

---

### 4. Generador de versículos

Permite generar texto a partir de una palabra inicial usando modelos de n-gramas.

Modelos disponibles:

- Unigrama.
- Bigrama.
- Trigrama.
- Cuatrigrama.

El usuario puede seleccionar:

- Modelo de n-gramas.
- Palabra inicial.
- Largo máximo de la oración.
- Cantidad de resultados a generar.

---

## Librerías utilizadas

### API

- FastAPI
- Uvicorn
- Pandas
- NumPy
- Scikit-learn
- Gensim

### Aplicación Streamlit

- Streamlit
- Requests
- Pandas
- Matplotlib
- WordCloud
- Plotly
- python-dotenv

---

## Consideraciones

- La API debe estar encendida antes de usar la aplicación Streamlit.
- El procesamiento del corpus, búsqueda, PCA y generación de texto se realizan en la API.
- Streamlit no carga ni procesa directamente todo el corpus.
- Los archivos del dataset deben estar ubicados en `api/datos/dataset_original/`.
- Si se modifica código de la API, esta puede reiniciarse automáticamente por el modo `--reload`.
---
## Aclaraciones

- La API se encarga del trabajo pesado, la aplicación solo muestra las consultas y resultados.
