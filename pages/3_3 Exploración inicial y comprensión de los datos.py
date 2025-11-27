import streamlit as st
from utils.carga_datos import cargar_datos_loteria
from utils.eda_helpers import *
from utils.graficos import *
import pandas as pd

st.title("🔍 3. Exploración Inicial y Comprensión de los Datos (EDA)")

st.markdown("""
## 🎯 Objetivo de esta Etapa

Realizar un análisis exploratorio exhaustivo para entender la estructura, distribuciones y patrones en los datos
antes de cualquier modelado o análisis avanzado.
""")

try:
    df = cargar_datos_loteria()
    
    # Tabs para organizar el EDA
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Resumen General",
        "🎲 Análisis de Números",
        "🎫 Análisis de Series",
        "📅 Análisis Temporal",
        "🔬 Análisis Estadístico"
    ])
    
    # TAB 1: Resumen General
    with tab1:
        st.header("📊 Resumen del Dataset")
        
        resumen = resumen_dataset(df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Filas", f"{resumen['Filas']:,}")
        with col2:
            st.metric("Columnas", resumen['Columnas'])
        with col3:
            st.metric("Años", df['año'].nunique())
        with col4:
            st.metric("Periodo", f"{df['año'].min()}-{df['año'].max()}")
        
        st.subheader("Tipos de Datos")
        tipos_df = pd.DataFrame({
            'Columna': list(resumen['Tipos de datos'].keys()),
            'Tipo': list(resumen['Tipos de datos'].values())
        })
        st.dataframe(tipos_df, use_container_width=True, hide_index=True)
        
        st.subheader("Estadísticas Descriptivas")
        st.dataframe(df[['sorteo', 'número', 'serie']].describe(), use_container_width=True)
        
        st.subheader("Primeras Filas")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
    
    # TAB 2: Análisis de Números
    with tab2:
        st.header("🎲 Análisis de Números Ganadores")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_distribucion_numeros(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_numeros_pares_impares(df), use_container_width=True)
        
        st.plotly_chart(grafico_top_numeros(df, top_n=20), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_frecuencia_digitos(df, 'primer'), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_frecuencia_digitos(df, 'ultimo'), use_container_width=True)
        
        st.plotly_chart(grafico_numeros_por_año(df), use_container_width=True)
        
        # Análisis de outliers
        st.subheader("🔍 Detección de Outliers en Números")
        outliers_info = analisis_outliers(df, 'número')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Q1 (Percentil 25)", f"{outliers_info['Q1']:.0f}")
        with col2:
            st.metric("Q3 (Percentil 75)", f"{outliers_info['Q3']:.0f}")
        with col3:
            st.metric("IQR", f"{outliers_info['IQR']:.0f}")
        
        if outliers_info['cantidad_outliers'] > 0:
            st.warning(f"Se detectaron {outliers_info['cantidad_outliers']} outliers ({outliers_info['porcentaje_outliers']:.2f}%)")
        else:
            st.success("No se detectaron outliers significativos")
    
    # TAB 3: Análisis de Series
    with tab3:
        st.header("🎫 Análisis de Series")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_distribucion_series(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_top_series(df, top_n=20), use_container_width=True)
        
        st.plotly_chart(grafico_series_por_año(df), use_container_width=True)
        
        st.plotly_chart(grafico_scatter_numero_serie(df), use_container_width=True)
        
        # Estadísticas de series
        st.subheader("📊 Estadísticas de Series")
        stats_series = estadisticas_por_grupo(df, 'rango_serie', 'serie')
        st.dataframe(stats_series, use_container_width=True, hide_index=True)
    
    # TAB 4: Análisis Temporal
    with tab4:
        st.header("📅 Análisis Temporal")
        
        st.plotly_chart(grafico_evolucion_por_año(df), use_container_width=True)
        
        st.plotly_chart(grafico_sorteos_tiempo(df), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_sorteos_por_dia_semana(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_tendencia_sorteos(df), use_container_width=True)
        
        st.plotly_chart(grafico_heatmap_mes_año(df), use_container_width=True)
        
        # Análisis de tendencias
        st.subheader("📈 Análisis de Tendencias")
        tendencias = analisis_tendencias(df, 'fecha', 'número')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tendencia", tendencias['tendencia'].capitalize())
        with col2:
            st.metric("R²", f"{tendencias['r_cuadrado']:.4f}")
        with col3:
            significativa = "Sí" if tendencias['significativa'] else "No"
            st.metric("Significativa", significativa)
        
        if tendencias['significativa']:
            st.info(f"Se detectó una tendencia {tendencias['tendencia']} estadísticamente significativa (p-value: {tendencias['p_valor']:.4f})")
        else:
            st.success(f"No hay tendencia significativa en los números (p-value: {tendencias['p_valor']:.4f})")
    
    # TAB 5: Análisis Estadístico
    with tab5:
        st.header("🔬 Análisis Estadístico Avanzado")
        
        st.subheader("Frecuencias de Números")
        freq_numeros = analisis_frecuencias(df, 'número')
        st.dataframe(freq_numeros.head(20), use_container_width=True, hide_index=True)
        
        st.subheader("Frecuencias de Series")
        freq_series = analisis_frecuencias(df, 'serie')
        st.dataframe(freq_series.head(20), use_container_width=True, hide_index=True)
        
        st.subheader("Análisis por Rango de Números")
        stats_rangos = estadisticas_por_grupo(df, 'rango_numero', 'número')
        st.dataframe(stats_rangos, use_container_width=True, hide_index=True)
        
        st.subheader("Valores Faltantes")
        faltantes = detectar_valores_faltantes(df)
        if len(faltantes) == 0:
            st.success("✅ No hay valores faltantes en el dataset")
        else:
            st.dataframe(faltantes, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Conclusiones del EDA
    st.header("📝 Conclusiones del EDA")
    
    st.markdown(f"""
    ### Hallazgos Principales:
    
    1. **Cobertura de Datos**: El dataset contiene **{len(df):,} sorteos** desde **{df['año'].min()}** hasta **{df['año'].max()}** ({df['año'].nunique()} años).
    
    2. **Distribución de Números**: 
       - Rango: 0-9999
       - Promedio: {df['número'].mean():.0f}
       - Mediana: {df['número'].median():.0f}
       - Números únicos: {df['número'].nunique():,}
    
    3. **Distribución de Series**:
       - Rango: {df['serie'].min()}-{df['serie'].max()}
       - Promedio: {df['serie'].mean():.0f}
       - Series únicas: {df['serie'].nunique():,}
    
    4. **Patrones Temporales**:
       - Sorteos por año: {df.groupby('año').size().mean():.1f} (promedio)
       - Día más común: {df['dia_semana_nombre'].mode()[0]}
    
    5. **Calidad de Datos**: 
       - Completitud: {((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100):.1f}%
       - Sin duplicados
    """)
    
    st.success("✅ Etapa 3 completada. Procede a la siguiente sección: Limpieza y Preparación de Datos.")

except Exception as e:
    st.error(f"❌ Error en el análisis: {e}")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())
