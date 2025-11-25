import streamlit as st
from utils.carga_datos import cargar_datos_loteria

st.title("🤖 7.7 Aplicación de IA Generativa")

df = cargar_datos_loteria()

st.write("Describe el comportamiento de los premios en 2023:")

explicacion = f"""
Los premios variaron entre **{df['premio_mayor_millones'].min()} y {df['premio_mayor_millones'].max()} millones**.
La ciudad con mayor número de premios fue **{df['ciudad'].mode()[0]}**.
El monto promedio del premio fue de **{df['premio_mayor_millones'].mean():.2f} millones**.
"""

st.info(explicacion)
