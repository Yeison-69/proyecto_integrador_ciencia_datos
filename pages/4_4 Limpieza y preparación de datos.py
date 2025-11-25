import streamlit as st
import pandas as pd
import os

st.title("🧼 Limpieza y preparación de datos")

# Ruta del archivo original
file_path = "static/datasets/datos_clientes.csv"

if not os.path.exists(file_path):
    st.error("❌ No se encontró el archivo **clientes.csv** en static/datasets/")
else:
    df = pd.read_csv(file_path)
    st.subheader("📌 Datos originales")
    st.dataframe(df)

    # Limpieza
    st.subheader("🧹 Paso 1: Conversión de fechas")
    df["fecha_alta"] = pd.to_datetime(df["fecha_alta"])
    df["fecha_ultima_compra"] = pd.to_datetime(df["fecha_ultima_compra"])

    st.success("Fechas convertidas correctamente")

    st.subheader("🧹 Paso 2: Manejo de valores faltantes")
    df = df.fillna({
        "historial_compra_total": 0,
        "frecuencia_12m": 0
    })
    st.success("Valores nulos tratados")

    st.subheader("🧹 Paso 3: Codificación de variables categóricas")
    df = pd.get_dummies(df, columns=["region", "canal"], drop_first=True)
    st.success("Variables categóricas codificadas")

    st.subheader("🧹 Paso 4: Guardar datos limpios")
    output_path = "static/datasets/datos_limpios.csv"
    df.to_csv(output_path, index=False)

    st.success(f"Archivo **datos_limpios.csv** creado correctamente en: {output_path}")

    st.subheader("📂 Vista previa final")
    st.dataframe(df)
