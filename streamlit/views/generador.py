import streamlit as st

from api_client import generar_versiculo


def volver_inicio():
    if st.button("Volver al inicio"):
        st.session_state["pagina"] = "inicio"
        st.rerun()


def parametros_generador():
    st.subheader("Parámetros del generador")

    opciones_modelo = {
        "Unigrama": "unigrama",
        "Bigrama": "bigrama",
        "Trigrama": "trigrama",
        "Cuatrigrama": "cuatrigrama"
    }

    modelo_seleccionado = st.selectbox(
        "Modelo de n-gramas",
        ["Unigrama", "Bigrama", "Trigrama", "Cuatrigrama"]
    )

    modelo = opciones_modelo[modelo_seleccionado]

    palabra_inicial = st.text_input(
        "Palabra inicial (recordar en inglés)"
    )

    max_palabras = st.number_input(
        "Largo máximo del oracion resultante",
        min_value=5,
        max_value=80,
        value=20,
        step=1
    )

    cantidad_resultados = st.number_input(
        "Cantidad de oraciones a generar",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

    generar = st.button("Generar oraciones")

    return modelo, modelo_seleccionado, palabra_inicial, int(max_palabras), int(cantidad_resultados), generar

def mostrar_resultado(datos):
    if "error" in datos:
        st.warning(datos["error"])
        return

    resultados_generados = datos["resultados_generados"]

    st.subheader("Resultados generados")

    for i in range(len(resultados_generados)):
        st.markdown(f"**Resultado {i + 1}:**")
        st.write(resultados_generados[i])
        st.divider()


def mostrar_generador():
    st.title("Generador de versículos")

    volver_inicio()

    st.write(
        "En esta sección se puede generar una serie de versículos a partir de una palabra inicial, usando modelos de n-gramas (unigrama, bigrama, trigrama y cuatrigrama)."
    )

    modelo, modelo_seleccionado, palabra_inicial, max_palabras, cantidad_resultados, generar = parametros_generador()

    if generar:
        if palabra_inicial.strip() == "":
            st.warning("Debe ingresar una palabra inicial.")
            return

        try:
            datos = generar_versiculo(
                modelo,
                palabra_inicial.strip().lower(),
                max_palabras,
                cantidad_resultados
            )

        except Exception as error:
            st.error("No se pudo generar el texto.")
            st.write("Revisa que la API esté encendida.")
            st.write(error)
            return

        st.divider()
        mostrar_resultado(datos)