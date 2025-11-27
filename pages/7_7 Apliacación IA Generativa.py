import streamlit as st
from utils.carga_datos import cargar_datos_loteria
from utils.ai_helpers import *
import pandas as pd

st.title("🤖 7. Aplicación de IA Generativa (Gemini)")

st.markdown("""
## 🎯 Objetivo de esta Etapa

Utilizar Google Gemini para análisis asistido por IA, generación automática de insights,
respuestas a preguntas sobre los datos y creación de reportes narrativos.
""")

# Verificar configuración
st.header("⚙️ Configuración")

# Intentar inicializar Gemini
model = inicializar_gemini()

if model is None:
    st.error("""
    ❌ **No se pudo inicializar Gemini**
    
    Para usar esta funcionalidad, necesitas configurar tu API key de Google Gemini:
    
    1. Obtén tu API key en: https://makersuite.google.com/app/apikey
    2. Crea el archivo `.streamlit/secrets.toml` en la raíz del proyecto
    3. Agrega tu API key:
    
    ```toml
    [gemini]
    api_key = "TU_API_KEY_AQUI"
    ```
    
    4. Reinicia la aplicación
    """)
    
    st.info("""
    **Nota**: También puedes copiar el archivo `.streamlit/secrets.toml.example` 
    a `.streamlit/secrets.toml` y completar con tu API key.
    """)
    
    st.stop()

st.success("✅ Gemini inicializado correctamente")

# Cargar datos
try:
    df = cargar_datos_loteria()
    
    # Tabs para diferentes funcionalidades
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Q&A",
        "💡 Insights Automáticos",
        "📝 Reporte Narrativo",
        "🔍 Sugerencias de Análisis",
        "📊 Explicar Métricas"
    ])
    
    # TAB 1: Q&A
    with tab1:
        st.header("💬 Pregunta y Respuesta sobre los Datos")
        
        st.markdown("""
        Haz preguntas sobre los datos de la lotería y Gemini te responderá basándose en el contexto del dataset.
        """)
        
        # Ejemplos de preguntas
        st.subheader("Ejemplos de Preguntas")
        
        ejemplos = [
            "¿Cuál es el número que ha salido más veces?",
            "¿Hay algún patrón en los números ganadores?",
            "¿Qué día de la semana hay más sorteos?",
            "¿Los números pares salen más que los impares?",
            "¿Cuál es la tendencia de sorteos a lo largo de los años?",
            "¿Existe correlación entre el número y la serie?",
            "¿Qué tan uniforme es la distribución de números?",
            "¿Cuáles son los insights más importantes de este dataset?"
        ]
        
        col1, col2 = st.columns(2)
        
        with col1:
            for i in range(0, len(ejemplos), 2):
                if st.button(f"📌 {ejemplos[i]}", key=f"ej_{i}"):
                    st.session_state.pregunta_ejemplo = ejemplos[i]
        
        with col2:
            for i in range(1, len(ejemplos), 2):
                if st.button(f"📌 {ejemplos[i]}", key=f"ej_{i}"):
                    st.session_state.pregunta_ejemplo = ejemplos[i]
        
        # Input de pregunta
        pregunta_default = st.session_state.get('pregunta_ejemplo', '')
        pregunta = st.text_area(
            "Tu pregunta:",
            value=pregunta_default,
            height=100,
            placeholder="Escribe tu pregunta sobre los datos de la lotería..."
        )
        
        if st.button("🚀 Obtener Respuesta", type="primary"):
            if pregunta.strip():
                with st.spinner("🤔 Gemini está analizando..."):
                    respuesta = responder_pregunta(model, df, pregunta)
                    st.markdown("### 💡 Respuesta de Gemini:")
                    st.markdown(respuesta)
            else:
                st.warning("Por favor escribe una pregunta")
    
    # TAB 2: Insights Automáticos
    with tab2:
        st.header("💡 Insights Automáticos")
        
        st.markdown("""
        Gemini analizará el dataset y generará insights clave automáticamente.
        """)
        
        if st.button("🔍 Generar Insights", type="primary"):
            with st.spinner("🤖 Analizando datos y generando insights..."):
                insights = obtener_insights(model, df)
                st.markdown("### 📊 Insights Generados:")
                st.markdown(insights)
        
        st.info("""
        **Tip**: Los insights se generan basándose en:
        - Estadísticas descriptivas del dataset
        - Distribución de números y series
        - Patrones temporales
        - Análisis de frecuencias
        """)
    
    # TAB 3: Reporte Narrativo
    with tab3:
        st.header("📝 Reporte Narrativo")
        
        st.markdown("""
        Genera un reporte ejecutivo completo en formato narrativo sobre el análisis de la lotería.
        """)
        
        if st.button("📄 Generar Reporte", type="primary"):
            with st.spinner("✍️ Gemini está escribiendo el reporte..."):
                reporte = generar_reporte_narrativo(model, df)
                st.markdown("### 📋 Reporte Ejecutivo:")
                st.markdown(reporte)
                
                # Opción para descargar
                st.download_button(
                    label="⬇️ Descargar Reporte",
                    data=reporte,
                    file_name="reporte_loteria_medellin.md",
                    mime="text/markdown"
                )
        
        st.info("""
        **El reporte incluye:**
        - Resumen ejecutivo
        - Hallazgos principales
        - Patrones identificados
        - Recomendaciones
        """)
    
    # TAB 4: Sugerencias de Análisis
    with tab4:
        st.header("🔍 Sugerencias de Análisis Adicionales")
        
        st.markdown("""
        Gemini sugerirá análisis adicionales que podrían ser valiosos basándose en el dataset.
        """)
        
        if st.button("💭 Obtener Sugerencias", type="primary"):
            with st.spinner("🤔 Gemini está pensando en análisis adicionales..."):
                sugerencias = sugerir_analisis(model, df)
                st.markdown("### 🎯 Sugerencias de Análisis:")
                st.markdown(sugerencias)
        
        st.info("""
        **Las sugerencias pueden incluir:**
        - Análisis estadísticos avanzados
        - Visualizaciones adicionales
        - Pruebas de hipótesis
        - Modelos predictivos (con advertencias)
        - Análisis de series temporales
        """)
    
    # TAB 5: Explicar Métricas
    with tab5:
        st.header("📊 Explicar Métricas")
        
        st.markdown("""
        Selecciona una métrica y Gemini te explicará qué significa y cómo interpretarla.
        """)
        
        # Métricas disponibles
        metricas = {
            "Promedio de números": df['número'].mean(),
            "Desviación estándar de números": df['número'].std(),
            "Coeficiente de variación": (df['número'].std() / df['número'].mean() * 100),
            "Números únicos": df['número'].nunique(),
            "Proporción de números pares": (df['numero_par'] == 1).sum() / len(df) * 100,
            "Sorteos por año (promedio)": df.groupby('año').size().mean(),
            "Serie promedio": df['serie'].mean(),
            "Autocorrelación (lag-1)": df.sort_values('fecha')['número'].autocorr(lag=1) if len(df) > 1 else 0
        }
        
        metrica_seleccionada = st.selectbox(
            "Selecciona una métrica:",
            options=list(metricas.keys())
        )
        
        valor_metrica = metricas[metrica_seleccionada]
        
        st.metric(metrica_seleccionada, f"{valor_metrica:.2f}")
        
        if st.button("📖 Explicar esta Métrica", type="primary"):
            with st.spinner("🤓 Gemini está preparando la explicación..."):
                contexto = f"Dataset de lotería con {len(df)} sorteos desde {df['año'].min()} hasta {df['año'].max()}"
                explicacion = explicar_metrica(model, metrica_seleccionada, valor_metrica, contexto)
                st.markdown("### 💡 Explicación:")
                st.markdown(explicacion)
    
    st.markdown("---")
    
    # Información adicional
    st.header("ℹ️ Sobre la IA Generativa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Capacidades")
        st.markdown("""
        - Responder preguntas sobre los datos
        - Generar insights automáticos
        - Crear reportes narrativos
        - Sugerir análisis adicionales
        - Explicar métricas complejas
        - Interpretar resultados estadísticos
        """)
    
    with col2:
        st.subheader("⚠️ Limitaciones")
        st.markdown("""
        - Las respuestas son generadas por IA
        - Pueden contener imprecisiones
        - No reemplazan el análisis humano
        - Basadas en el contexto proporcionado
        - No tienen acceso a datos externos
        - Requieren validación humana
        """)
    
    st.warning("""
    **Importante**: Las respuestas de Gemini son generadas automáticamente y deben ser validadas.
    La IA es una herramienta de apoyo, no un reemplazo del análisis crítico humano.
    """)
    
    st.success("✅ Etapa 7 completada. ¡Has completado todas las etapas del proyecto!")
    
    st.balloons()

except Exception as e:
    st.error(f"❌ Error en la aplicación de IA: {e}")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())
