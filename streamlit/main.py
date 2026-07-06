import streamlit as st
from views.dashboard import mostrar_dashboard


def configurar_pagina():
    st.set_page_config(page_title="Laboratorio 3 - Corpus Bíblico", layout="wide")


def iniciar_estado():
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "inicio"


def mostrar_inicio():
    st.title("Laboratorio 3 - Streamlit")
    st.write("Esta app usa una API REST, la cual se encarga de hacer todo el análisis del corpus bíblico, en este apartado solo se muestran los resultados.")
    st.markdown("""
        Apartados de la app:
        - Dashboard
        - Buscador semántico
        - Visualización con PCA/Word2Vec
        - Generador de texto con n-gramas
    """)

    st.divider()

    if st.button("Dashboard"):
        st.session_state["pagina"] = "dashboard"
        st.rerun()


def main():
    configurar_pagina()
    iniciar_estado()

    if st.session_state["pagina"] == "inicio":
        mostrar_inicio()
    elif st.session_state["pagina"] == "dashboard":
        mostrar_dashboard()


if __name__ == "__main__":
    main()