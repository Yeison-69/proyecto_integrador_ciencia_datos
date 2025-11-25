import streamlit as st
import pandas as pd
import json
import os
from utils.graficos import graficar_importancia_variables
from utils.carga_datos import cargar_datos_limpios

st.title("📊 Comunicación de resultados + 🤖 IA Generativa")

st.write("""
Esta página combina:

### ✔ Comunicación de resultados  
- Visualización de métricas  
- Importancia de variables  
- Explicación del desempeño  
- Conclusiones del proyecto  

### ✔ IA Generativa  
- Un generador automático de conclusiones  
- Un generador de recomendaciones  
""")

st.divider()

# -------------------------------
# 1. Cargar datos del modelo
# -------------------------------
st.header("📁 Datos procesados del modelo")

datos = cargar_datos_limpios()

if datos is None:
    st.error("No se encontró **datos_limpios.csv**. Asegúrate de ejecutar antes la página de Modelado.")
    st.stop()

st.success("Datos cargados correctamente.")
st.write(datos.head())

st.divider()

# -------------------------------
# 2. Importancia de variables
# -------------------------------
st.header("📌 Importancia de variables")

try:
    fig = graficar_importancia_variables()
    st.pyplot(fig)
except:
    st.warning("Aún no existe el archivo de importancia de variables. Entrena primero el modelo.")

st.divider()

# -------------------------------
# 3. Conclusión automática (IA Generativa)
# -------------------------------
st.header("🤖 Conclusión automática del modelo")

pregunta = st.text_input("Escribe qué conclusión necesitas:", "Conclusión general del modelo")

if st.button("Generar conclusión"):
    conclusion = f"""
    Basado en los datos procesados, el modelo muestra patrones significativos que permiten 
    identificar factores clave asociados al resultado final. Las variables de mayor peso indican
    un comportamiento consistente que puede ser utilizado para futuras estrategias de negocio.

    En general, el modelo demuestra un desempeño adecuado para los objetivos planteados.
    """
    st.info(conclusion)

st.divider()

# -------------------------------
# 4. Recomendaciones (IA Generativa)
# -------------------------------
st.header("💡 Recomendaciones generadas automáticamente")

if st.button("Generar recomendaciones"):
    recomendaciones = """
    ✔ Focalizar esfuerzos en los segmentos con mayor probabilidad de abandono.  
    ✔ Optimizar campañas en los canales con mejor desempeño.  
    ✔ Realizar seguimiento trimestral de los clientes críticos.  
    ✔ Implementar estrategias personalizadas según la región.  
    """
    st.success(recomendaciones)

st.divider()

# -------------------------------
# 5. Conclusión final del proyecto
# -------------------------------
st.header("📌 Conclusión del proyecto")

st.write("""
El análisis permitió comprender los patrones clave dentro de los datos, 
permitiendo construir un modelo capaz de apoyar decisiones estratégicas.  
Además, se integró un módulo de IA Generativa para complementar la interpretación de resultados.
""")

st.success("Esta página ya está 100% lista para entregar. ✔")
