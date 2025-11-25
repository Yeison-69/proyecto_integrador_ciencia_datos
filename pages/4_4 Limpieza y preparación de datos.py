import streamlit as st
import pandas as pd
import os

st.title("🧹 Limpieza y preparación de datos")

# Cargar el dataset
file_path = "data/datos_clientes.csv"

if not os.path.exists(file_path):
    st.error("⚠️ No se encontró el archivo 'datos_clientes.csv' en la carpeta data/")
else:
    df = pd.read_csv(file_path)

    st.subheader("Datos originales")
    st.dataframe(df)

    # Convertir fechas
    df["fecha_alta"] = pd.to_datetime(df["fecha_alta"], errors="coerce")
    df["fecha_ultima_compra"] = pd.to_datetime(df["fecha_ultima_compra"], errors="coerce")

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Rellenar valores nulos
    df["region"] = df["region"].fillna("Sin región")
    df["canal"] = df["canal"].fillna("Desconocido")
    df["historial_compra_total"] = df["historial_compra_total"].fillna(0)

    st.subheader("Datos limpiados")
    st.dataframe(df)

    # Guardado
    cleaned_path = "data/datos_clientes_limpios.csv"
    df.to_csv(cleaned_path, index=False)

    st.success("✔ Archivo limpio guardado en data/datos_clientes_limpios.csv")
