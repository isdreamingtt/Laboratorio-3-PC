import streamlit as st
import requests

st.title("Prueba de conexión")

if st.button("Probar API"):
    respuesta = requests.get("http://127.0.0.1:8000")
    st.write(respuesta.json())