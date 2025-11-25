import streamlit as st
import pandas as pd

st.title("4. Limpieza y preparación de datos")

file_path = "static/datasets/datos_clientes.csv"

try:
    df = pd.read_csv(file_path)

    st.subheader("Antes de limpiar:")
    st.write(df.head())

    # Limpieza simple
    df["fecha_alta"] = pd.to_datetime(df["fecha_alta"])
    df["fecha_ultima_compra"] = pd.to_datetime(df["fecha_ultima_compra"])

    df = df.dropna()

    st.subheader("Después de limpiar:")
    st.write(df.head())

    # Exportar dataset limpio
    df.to_csv("static/datasets/datos_limpios.csv", index=False)

    st.success("Archivo 'datos_limpios.csv' generado exitosamente.")

except Exception as e:
    st.error(f"Error: {str(e)}")
