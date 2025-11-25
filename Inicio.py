import streamlit as st
from utils.carga_datos import cargar_datos_loteria

st.set_page_config(
    page_title="Proyecto Integrador – Lotería Medellín",
    page_icon="🎰",
    layout="wide"
)

st.title("🎰 Proyecto Integrador – Análisis de la Lotería de Medellín")
st.write("Bienvenido al proyecto donde analizamos los premios mayores de la Lotería de Medellín usando ciencia de datos.")

st.header("📌 Objetivo del Proyecto")
st.write("""
Este proyecto busca **analizar los sorteos del premio mayor de la Lotería de Medellín**
para identificar patrones históricos, tendencias por ciudad, series, números y valores entregados.

El objetivo final es:
**“Entender cómo se comportan los premios mayores y generar visualizaciones útiles para la toma de decisiones.”**
""")

st.header("📊 Vista rápida de los datos")
try:
    df = cargar_datos_loteria()
    st.dataframe(df.head())
except Exception as e:
    st.error(f"Error cargando los datos: {e}")

st.info("Usa el menú lateral para navegar entre las diferentes etapas del proyecto.")
