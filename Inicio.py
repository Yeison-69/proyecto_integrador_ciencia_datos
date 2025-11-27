import streamlit as st
from utils.carga_datos import cargar_datos_loteria

st.set_page_config(
    page_title="Proyecto Integrador – Lotería Medellín",
    page_icon="🎰",
    layout="wide"
)

# Título principal
st.title("🎰 Proyecto Integrador – Análisis de la Lotería de Medellín")

# Introducción
st.markdown("""
### Bienvenido al Proyecto de Ciencia de Datos

Este proyecto aplica metodologías de ciencia de datos para analizar **18 años de historia de sorteos de la Lotería de Medellín** (2007-2025), 
identificando patrones en números ganadores, series, tendencias temporales y generando insights accionables mediante visualizaciones interactivas e IA.
""")

# Cargar datos para mostrar métricas clave
try:
    df = cargar_datos_loteria()
    
    # Métricas clave en la portada
    st.header("📊 Métricas Clave del Proyecto")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Sorteos",
            value=f"{len(df):,}",
            delta=f"{df['año'].nunique()} años"
        )
    
    with col2:
        st.metric(
            label="Periodo Analizado",
            value=f"{df['año'].min()}-{df['año'].max()}",
            delta=f"{df['año'].max() - df['año'].min()} años"
        )
    
    with col3:
        numero_mas_comun = df['número'].mode()[0]
        frecuencia = (df['número'] == numero_mas_comun).sum()
        st.metric(
            label="Número Más Frecuente",
            value=f"{numero_mas_comun:04d}",
            delta=f"{frecuencia} veces"
        )
    
    with col4:
        serie_mas_comun = df['serie'].mode()[0]
        frecuencia_serie = (df['serie'] == serie_mas_comun).sum()
        st.metric(
            label="Serie Más Frecuente",
            value=f"{serie_mas_comun}",
            delta=f"{frecuencia_serie} veces"
        )
    
    # Objetivo del proyecto
    st.header("🎯 Objetivo del Proyecto")
    st.markdown("""
    **"Analizar 18 años de historia de sorteos de la Lotería de Medellín para identificar patrones en números ganadores, 
    series y tendencias temporales, utilizando visualizaciones interactivas e inteligencia artificial para generar insights útiles."**
    
    #### Alcance:
    - ✅ Análisis de **976 sorteos** desde 2007 hasta 2025
    - ✅ Identificación de patrones en números y series ganadores
    - ✅ Análisis de tendencias temporales (por año, mes, día de semana)
    - ✅ Visualizaciones interactivas con Plotly
    - ✅ Estadísticas descriptivas e inferenciales
    - ✅ Asistente de IA con Gemini para análisis y Q&A
    - ❌ **No incluye**: Predicción de números futuros ni garantías de ganar
    """)
    
    # Vista previa de datos
    st.header("📋 Vista Previa de los Datos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            df[['fecha', 'sorteo', 'número', 'serie', 'año', 'mes_nombre']].head(15),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.info(f"""
        **Información del Dataset:**
        - 📅 Periodo: {df['fecha'].min().strftime('%Y-%m-%d')} a {df['fecha'].max().strftime('%Y-%m-%d')}
        - 📊 Total Sorteos: {len(df):,}
        - 🎲 Rango Números: 0-9999
        - 🎫 Rango Series: {df['serie'].min()}-{df['serie'].max()}
        - 📈 Años Cobertura: {df['año'].nunique()}
        """)
    
    # Estadísticas rápidas
    st.header("📈 Estadísticas Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Números")
        st.write(f"**Promedio:** {df['número'].mean():.0f}")
        st.write(f"**Mediana:** {df['número'].median():.0f}")
        st.write(f"**Desv. Estándar:** {df['número'].std():.0f}")
        st.write(f"**Mínimo:** {df['número'].min()}")
        st.write(f"**Máximo:** {df['número'].max()}")
    
    with col2:
        st.subheader("Series")
        st.write(f"**Promedio:** {df['serie'].mean():.0f}")
        st.write(f"**Mediana:** {df['serie'].median():.0f}")
        st.write(f"**Desv. Estándar:** {df['serie'].std():.0f}")
        st.write(f"**Mínimo:** {df['serie'].min()}")
        st.write(f"**Máximo:** {df['serie'].max()}")
    
    with col3:
        st.subheader("Sorteos por Año")
        sorteos_año = df.groupby('año').size()
        st.write(f"**Promedio:** {sorteos_año.mean():.1f}")
        st.write(f"**Año con más:** {sorteos_año.idxmax()} ({sorteos_año.max()})")
        st.write(f"**Año con menos:** {sorteos_año.idxmin()} ({sorteos_año.min()})")
    
    # Guía de navegación
    st.header("🧭 Guía de Navegación")
    st.markdown("""
    Usa el menú lateral para navegar por las diferentes etapas del proyecto:
    
    1. **📌 Definición del Problema** - Objetivos, KPIs y alcance del análisis
    2. **📂 Recolección de Datos** - Fuentes, metadata y calidad del dataset
    3. **🔍 Exploración de Datos (EDA)** - Análisis exploratorio con visualizaciones interactivas
    4. **🧹 Limpieza y Preparación** - Transformaciones y feature engineering
    5. **📈 Evaluación e Interpretación** - Métricas, estadísticas y análisis de patrones
    6. **📊 Comunicación de Resultados** - Dashboard completo y storytelling
    7. **🤖 IA Generativa** - Asistente inteligente con Gemini para análisis y Q&A
    """)
    
    # Información del equipo
    st.header("👥 Información del Proyecto")
    st.markdown("""
    Este proyecto fue desarrollado aplicando metodologías estándar de ciencia de datos:
    - **CRISP-DM**: Metodología de minería de datos
    - **Análisis Exploratorio**: Identificación de patrones y tendencias
    - **Visualización Interactiva**: Plotly para gráficos dinámicos
    - **IA Generativa**: Gemini para insights automáticos
    
    **Tecnologías utilizadas:** Python, Streamlit, Plotly, Pandas, Google Gemini AI
    """)

except Exception as e:
    st.error(f"❌ Error cargando los datos: {e}")
    st.info("Verifica que el archivo `data/premio_mayor_loteria_medellin.csv` existe y es accesible.")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())
