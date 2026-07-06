import streamlit as st
import pandas as pd
import plotly.express as px

from api_client import obtener_pca_tfidf, obtener_pca_word2vec


def volver_inicio():
    if st.button("Volver al inicio"):
        st.session_state["pagina"] = "inicio"
        st.rerun()


def mostrar_opciones():
    st.subheader("Parametros para la visualización")

    modelo_vista = st.selectbox(
        "Representación vectorial o vectorización",
        ["TF-IDF + PCA", "Word2Vec + PCA"]
    )

    tipo_grafico = st.selectbox(
        "Dimensiones",
        ["2D", "3D"]
    )

    if tipo_grafico == "2D":
        dimensiones = 2
    else:
        dimensiones = 3

    return modelo_vista, dimensiones


def obtener_datos_visualizacion(modelo_vista, dimensiones):
    if modelo_vista == "TF-IDF + PCA":
        datos = obtener_pca_tfidf(dimensiones)
    else:
        datos = obtener_pca_word2vec(dimensiones)

    return datos


def preparar_dataframe(datos):
    puntos = datos["puntos"]

    df = pd.DataFrame(puntos)

    return df


def mostrar_varianza(datos):
    varianza = datos["varianza_explicada"]

    st.write("Que tanta información original se logra conservar al reducir las dimensiones por cada componente:")

    for i in range(len(varianza)):
        porcentaje = varianza[i] * 100
        st.write(f"Componente {i + 1}: {porcentaje:.2f}%")


def graficar_2d(df):
    figura = px.scatter(
        df,
        x="componente_1",
        y="componente_2",
        color="testamento",
        hover_data=["libro", "texto"],
        title="Visualización 2D de versículos"
    )

    st.plotly_chart(figura, use_container_width=True)


def graficar_3d(df):
    figura = px.scatter_3d(
        df,
        x="componente_1",
        y="componente_2",
        z="componente_3",
        color="testamento",
        hover_data=["libro", "texto"],
        title="Visualización 3D de versículos"
    )

    st.plotly_chart(figura, use_container_width=True)

def mostrar_visualizador():
    st.title("Visualizador PCA y Word2Vec")

    volver_inicio()

    st.write(
        "En este apartado se puede visualizar el PCA bajo dos vectorizaciones diferentes: TF-IDF y Word2Vec."
    )

    modelo_vista, dimensiones = mostrar_opciones()

    if st.button("Generar visualización"):
        try:
            datos = obtener_datos_visualizacion(modelo_vista, dimensiones)

        except Exception as error:
            st.error("No se pudo obtener la visualización desde la API.")
            st.write("Revisa que la API esté encendida.")
            st.write(error)
            return

        df = preparar_dataframe(datos)

        if len(df) == 0:
            st.warning("No hay puntos para mostrar.")
            return

        st.divider()

        st.subheader(modelo_vista)

        mostrar_varianza(datos)

        if dimensiones == 2:
            graficar_2d(df)
        else:
            graficar_3d(df)