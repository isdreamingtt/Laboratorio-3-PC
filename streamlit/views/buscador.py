import streamlit as st
import pandas as pd

from api_client import buscar_versiculos


def volver_inicio():
    if st.button("Volver al inicio"):
        st.session_state["pagina"] = "inicio"
        st.rerun()


def parametros_busqueda():
    st.subheader("Buscar versículos similares")

    consulta = st.text_input(
        "Escribe una frase para buscar",
        placeholder="Ejemplo: love your enemies"
    )

    modelo = st.selectbox(
        "Modelo de búsqueda",
        ["tfidf", "word2vec"],
        format_func=lambda x: "TF-IDF" if x == "tfidf" else "Word2Vec" #Solo para mostrar en la interfaz, sirve para que se vea mpas 'bonito'
    )

    k = st.number_input(
        "Cantidad de resultados",
        min_value=1,
        max_value=20,
        value=10,
        step=1
    )

    buscar = st.button("Buscar")

    return consulta, int(k), modelo, buscar


def mostrar_resultados(datos):
    resultados = datos["resultados"]

    if len(resultados) == 0:
        st.warning(
            "No se encontraron versículos similares. "
            "Intenta probar otra frase o incluso probar una del corpus."
        )
        return

    df = pd.DataFrame(resultados)

    df = df.rename(columns={
        "libro": "Libro",
        "capitulo": "Capítulo",
        "versiculo": "Versículo",
        "texto": "Texto",
        "similitud": "Similitud"
    })

    df["Similitud"] = df["Similitud"].round(4)

    st.dataframe(df, use_container_width=True)


def buscador():
    st.title("Buscador semántico")

    volver_inicio()

    st.write(
        "Buscador semántico busca la similitud entre una consulta y los versículos de la Biblia, puedes elegir entre dos modelos: TF-IDF y Word2Vec. " \
        "Recordar que la consulta debe estar en inglés, ya que el corpus de la Biblia está en ese idioma."
        "Para este apartado se uso la tecnica de la similitud del coseno."
    )

    consulta, k, modelo, buscar = parametros_busqueda()

    if buscar:
        if consulta.strip() == "":
            st.warning("Debe ingresar una frase antes de buscar.")
            return

        try:
            datos = buscar_versiculos(consulta.strip(), k, modelo)

        except Exception as error:
            st.error("No se pudo realizar la búsqueda.")
            st.write("Revisa que la API esté encendida.")
            st.write(error)
            return

        st.divider()

        st.subheader(f"Resultados para: {consulta}")

        if modelo == "tfidf":
            st.caption("Modelo utilizado: TF-IDF")
        else:
            st.caption("Modelo utilizado: Word2Vec")

        mostrar_resultados(datos)