import streamlit as st
from views.dashboard import mostrar_dashboard


API_URL = "http://127.0.0.1:8000"


def configurar_pagina():
    st.set_page_config(
        page_title="Laboratorio 3 - Streamlit",
        layout="wide"
    )


def estado_inicial():
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "inicio"


def mostrar_inicio():
    st.title("Laboratorio 3 - Streamlit")
    st.subheader("Curso: Programación Científica")
    st.write(
        "Sistema cliente-servidor para explorar y analizar el corpus bíblico."
    )

    st.markdown("### Funcionalidades del laboratorio")

    st.write("- Dashboard principal del corpus")
    st.write("- Buscador semántico de versículos")
    st.write("- Visualizador PCA y Word2Vec")
    st.write("- Generador de versículos con n-gramas")

    st.divider()

    if st.button("Ir al dashboard principal"):
        st.session_state["pagina"] = "dashboard"
        st.rerun()


def ejecutar_app():
    configurar_pagina()
    estado_inicial()

    if st.session_state["pagina"] == "inicio":
        mostrar_inicio()

    elif st.session_state["pagina"] == "dashboard":
        mostrar_dashboard(API_URL)


if __name__ == "__main__":
    ejecutar_app()