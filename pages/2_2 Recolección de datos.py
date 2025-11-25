import streamlit as st
from utils.carga_datos import cargar_datos_loteria

st.title("📂 2.2 Recolección de datos")

st.markdown("### Cargando archivo original…")

df = cargar_datos_loteria()

st.success("Archivo cargado correctamente")
st.dataframe(df)
