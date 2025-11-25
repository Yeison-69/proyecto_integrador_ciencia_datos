import streamlit as st
from utils.carga_datos import cargar_datos_loteria
from utils.validaciones import validar_columnas

st.title("🧹 4.3 Limpieza de datos")

df = cargar_datos_loteria()
faltantes = validar_columnas(df)

if faltantes:
    st.error(f"Columnas faltantes: {faltantes}")
else:
    st.success("Todas las columnas están correctas.")

st.dataframe(df)
