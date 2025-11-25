import streamlit as st
from utils.carga_datos import cargar_datos_loteria
from utils.graficos import grafico_premios_por_ciudad, grafico_premios_en_el_tiempo

st.title("📊 6.6 Comunicación de resultados")

df = cargar_datos_loteria()

st.subheader("Premios por ciudad")
fig1 = grafico_premios_por_ciudad(df)
st.pyplot(fig1)

st.subheader("Premios a lo largo del tiempo")
fig2 = grafico_premios_en_el_tiempo(df)
st.pyplot(fig2)
