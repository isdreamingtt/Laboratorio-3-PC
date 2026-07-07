import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from api_client import obtener_dashboard


def volver_inicio():
    if st.button("Volver al inicio"):
        st.session_state["pagina"] = "inicio"
        st.rerun()


def mostrar_filtros():
    st.sidebar.header("Filtros")

    testamento = st.sidebar.selectbox(
        "Testamento",
        ["Todos", "OT", "NT"]
    )

    libro = st.sidebar.text_input(
        "Libro"
    )

    capitulo = st.sidebar.number_input(
        "Capítulo",
        min_value=0,
        step=1
    )

    parametros = {}

    if testamento != "Todos":
        parametros["testamento"] = testamento

    if libro.strip() != "":
        parametros["libro"] = libro.strip()

    if capitulo > 0:
        parametros["capitulo"] = int(capitulo)

    return parametros


def resumen(datos):
    cantidad_por_libro = datos["cantidad_por_libro"]
    total_versiculos = sum(cantidad_por_libro.values())
    total_libros = len(cantidad_por_libro)

    col1, col2= st.columns(2)
    col1.metric("Versículos encontrados", total_versiculos)
    col2.metric("Libros encontrados", total_libros)


def cantidad_por_libro(datos):
    st.subheader("Cantidad de versículos por libro")

    cantidad_por_libro = datos["cantidad_por_libro"]

    df = pd.DataFrame(
        list(cantidad_por_libro.items()),
        columns=["Libro", "Cantidad"]
    )

    if len(df) == 0:
        st.warning("No hay datos, pruebe otros filtros.")
        return

    df = df.sort_values("Cantidad", ascending=False)

    st.bar_chart(df.set_index("Libro"))
    st.dataframe(df, use_container_width=True)


def longitud_promedio(datos):
    st.subheader("Longitud promedio de versículos por libro")

    longitud_promedio = datos["longitud_promedio_por_libro"]

    df = pd.DataFrame(
        list(longitud_promedio.items()),
        columns=["Libro", "Longitud promedio"]
    )

    if len(df) == 0:
        st.warning("No hay datos, pruebe otros filtros.")
        return

    df = df.sort_values("Longitud promedio", ascending=False)

    st.bar_chart(df.set_index("Libro"))
    st.dataframe(df, use_container_width=True)


def palabras_frecuentes(datos):
    st.subheader("Listado palabras más frecuentes (top 20)")

    top_palabras = datos["top_palabras"]
    df = pd.DataFrame(top_palabras)

    if len(df) == 0:
        st.warning("No hay palabras que mostrar.")
        return

    st.bar_chart(df.set_index("palabra"))
    st.dataframe(df, use_container_width=True)


def mostrar_nube_palabras(datos):
    st.subheader("Nube de palabras")

    top_palabras = datos["top_palabras"]
    df = pd.DataFrame(top_palabras)

    if len(df) == 0:
        st.warning("No hay palabras para generar la nube.")
        return

    frecuencias = {}

    for _, fila in df.iterrows():
        frecuencias[fila["palabra"]] = int(fila["frecuencia"])

    nube = WordCloud(
        width=900,
        height=400,
        background_color="white"
    ).generate_from_frequencies(frecuencias)

    figura, eje = plt.subplots(figsize=(12, 5))
    eje.imshow(nube, interpolation="bilinear")
    eje.axis("off")

    st.pyplot(figura)


def mostrar_dashboard():
    st.title("Dashboard principal")
    volver_inicio()

    st.write(
        "Recordar que la biblia analizada es la versión BBE (Bible in Basic English), por lo que todas las consultas deben hacerse en inglés."
    )

    parametros = mostrar_filtros()
    try:
        datos = obtener_dashboard(parametros)

    except Exception as error:
        st.error(f"No se pudo conectar con la API: {error}")
        return

    resumen(datos)

    st.divider()
    cantidad_por_libro(datos)

    st.divider()
    longitud_promedio(datos)

    st.divider()
    palabras_frecuentes(datos)

    st.divider()
    mostrar_nube_palabras(datos)