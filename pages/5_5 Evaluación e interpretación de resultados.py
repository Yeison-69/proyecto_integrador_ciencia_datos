import streamlit as st
from utils.carga_datos import cargar_datos_loteria

st.title("📈 5.5 Evaluación e interpretación")

df = cargar_datos_loteria()

st.write("Promedio general del premio:")
st.metric("Promedio (millones)", df["premio_mayor_millones"].mean())
