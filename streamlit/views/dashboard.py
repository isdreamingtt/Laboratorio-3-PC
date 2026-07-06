import streamlit as st
import requests
import pandas as pd


def volver_inicio():
    if st.button("Volver al inicio"):
        st.session_state["pagina"] = "inicio"
        st.rerun()


def mostrar_filtros():
    st.sidebar.header("Filtros del dashboard")

    testamento = st.sidebar.selectbox(
        "Testamento",
        ["Todos", "OT", "NT"]
    )

    libro = st.sidebar.text_input(
        "Libro",
        placeholder="Ejemplo: Genesis"
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


def obtener_datos_dashboard(api_url, parametros):
    respuesta = requests.get(
        api_url + "/dashboard",
        params=parametros
    )

    respuesta.raise_for_status()

    return respuesta.json()


def mostrar_resumen(datos):
    cantidad_por_libro = datos["cantidad_por_libro"]
    top_palabras = datos["top_palabras"]

    total_versiculos = sum(cantidad_por_libro.values())
    cantidad_libros = len(cantidad_por_libro)

    col1, col2, col3 = st.columns(3)

    col1.metric("Versículos encontrados", total_versiculos)
    col2.metric("Libros encontrados", cantidad_libros)
    col3.metric("Palabras frecuentes", len(top_palabras))


def mostrar_cantidad_por_libro(datos):
    st.subheader("Cantidad de versículos por libro")

    cantidad_por_libro = datos["cantidad_por_libro"]

    df_cantidad = pd.DataFrame(
        list(cantidad_por_libro.items()),
        columns=["Libro", "Cantidad de versículos"]
    )

    if len(df_cantidad) == 0:
        st.warning("No hay datos para los filtros seleccionados.")
        return

    df_cantidad = df_cantidad.sort_values(
        "Cantidad de versículos",
        ascending=False
    )

    st.bar_chart(df_cantidad.set_index("Libro"))
    st.dataframe(df_cantidad, use_container_width=True)


def mostrar_longitud_promedio(datos):
    st.subheader("Longitud promedio de versículos por libro")

    longitud_promedio = datos["longitud_promedio_por_libro"]

    df_longitud = pd.DataFrame(
        list(longitud_promedio.items()),
        columns=["Libro", "Longitud promedio"]
    )

    if len(df_longitud) == 0:
        st.warning("No hay datos de longitud promedio.")
        return

    df_longitud = df_longitud.sort_values(
        "Longitud promedio",
        ascending=False
    )

    st.bar_chart(df_longitud.set_index("Libro"))
    st.dataframe(df_longitud, use_container_width=True)


def mostrar_top_palabras(datos):
    st.subheader("Top palabras más frecuentes")

    top_palabras = datos["top_palabras"]

    df_palabras = pd.DataFrame(top_palabras)

    if len(df_palabras) == 0:
        st.warning("No hay palabras frecuentes para mostrar.")
        return

    st.bar_chart(df_palabras.set_index("palabra"))
    st.dataframe(df_palabras, use_container_width=True)


def mostrar_dashboard(api_url):
    st.title("Dashboard principal")

    volver_inicio()

    st.write(
        "Los filtros se envían a la API. La API filtra y calcula los resultados; "
        "Streamlit solo los muestra."
    )

    parametros = mostrar_filtros()

    try:
        datos = obtener_datos_dashboard(api_url, parametros)

    except Exception as error:
        st.error("No se pudo obtener información desde la API.")
        st.write("Verifica que la API esté encendida.")
        st.write(error)
        return

    mostrar_resumen(datos)

    st.divider()

    mostrar_cantidad_por_libro(datos)

    st.divider()

    mostrar_longitud_promedio(datos)

    st.divider()

    mostrar_top_palabras(datos)