import streamlit as st
from utils.carga_datos import cargar_datos_loteria
from utils.eda_helpers import resumen_dataset

st.title("🔍 3.3 Exploración inicial")

df = cargar_datos_loteria()

st.subheader("Resumen del dataset")
res = resumen_dataset(df)
st.json(res)

st.subheader("Primeras filas")
st.dataframe(df.head())
