import streamlit as st
from utils.carga_datos import cargar_datos_loteria
from utils.graficos import *
import pandas as pd

st.title("📊 6. Comunicación de Resultados (Storytelling & Visualización)")

st.markdown("""
## 🎯 Objetivo de esta Etapa

Presentar los hallazgos del análisis de manera clara, visual e interactiva mediante un dashboard completo
que cuente la historia de 18 años de sorteos de la Lotería de Medellín.
""")

try:
    df = cargar_datos_loteria()
    
    # Estructura: Contexto → Hallazgos → Impacto → Recomendaciones
    
    # CONTEXTO
    st.header("📖 Contexto")
    
    st.markdown(f"""
    Este análisis examina **{len(df):,} sorteos** de la Lotería de Medellín realizados entre 
    **{df['año'].min()}** y **{df['año'].max()}**, abarcando **{df['año'].nunique()} años** de historia.
    
    Cada sorteo genera un número ganador (0-9999) y una serie específica, creando una rica base de datos
    para análisis estadístico y de patrones.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sorteos", f"{len(df):,}")
    with col2:
        st.metric("Años Analizados", df['año'].nunique())
    with col3:
        st.metric("Números Únicos", f"{df['número'].nunique():,}")
    with col4:
        st.metric("Series Únicas", f"{df['serie'].nunique():,}")
    
    st.markdown("---")
    
    # HALLAZGOS
    st.header("🔍 Hallazgos Principales")
    
    # Tabs para organizar hallazgos
    tab1, tab2, tab3 = st.tabs(["🎲 Números", "🎫 Series", "📅 Temporal"])
    
    with tab1:
        st.subheader("Análisis de Números Ganadores")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_distribucion_numeros(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_numeros_pares_impares(df), use_container_width=True)
        
        st.plotly_chart(grafico_top_numeros(df, 15), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_frecuencia_digitos(df, 'primer'), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_frecuencia_digitos(df, 'ultimo'), use_container_width=True)
        
        # Insights de números
        numero_mas_frecuente = df['número'].mode()[0]
        frecuencia = (df['número'] == numero_mas_frecuente).sum()
        pares = (df['numero_par'] == 1).sum()
        p_pares = pares / len(df)
        
        st.info(f"""
        **Insights Clave:**
        - El número más frecuente es **{numero_mas_frecuente:04d}** (apareció {frecuencia} veces)
        - {df['número'].nunique():,} números únicos de 10,000 posibles ({df['número'].nunique()/10000*100:.1f}%)
        - Distribución pares/impares: {pares} pares ({p_pares*100:.1f}%) vs {len(df)-pares} impares ({(1-p_pares)*100:.1f}%)
        - La distribución es aproximadamente uniforme, sugiriendo aleatoriedad
        """)
    
    with tab2:
        st.subheader("Análisis de Series")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_distribucion_series(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_top_series(df, 15), use_container_width=True)
        
        st.plotly_chart(grafico_scatter_numero_serie(df), use_container_width=True)
        
        # Insights de series
        serie_mas_frecuente = df['serie'].mode()[0]
        frecuencia_serie = (df['serie'] == serie_mas_frecuente).sum()
        
        st.info(f"""
        **Insights Clave:**
        - La serie más frecuente es **{serie_mas_frecuente}** (apareció {frecuencia_serie} veces)
        - {df['serie'].nunique():,} series únicas en el rango {df['serie'].min()}-{df['serie'].max()}
        - Serie promedio: {df['serie'].mean():.0f}
        - No hay correlación significativa entre número y serie
        """)
    
    with tab3:
        st.subheader("Análisis Temporal")
        
        st.plotly_chart(grafico_evolucion_por_año(df), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_sorteos_por_dia_semana(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_sorteos_tiempo(df), use_container_width=True)
        
        st.plotly_chart(grafico_heatmap_mes_año(df), use_container_width=True)
        
        # Insights temporales
        sorteos_año = df.groupby('año').size()
        dia_mas_comun = df['dia_semana_nombre'].mode()[0]
        
        st.info(f"""
        **Insights Clave:**
        - Promedio de sorteos por año: {sorteos_año.mean():.1f}
        - Año con más sorteos: {sorteos_año.idxmax()} ({sorteos_año.max()} sorteos)
        - Día más común para sorteos: {dia_mas_comun}
        - La frecuencia de sorteos ha variado a lo largo de los años
        """)
    
    st.markdown("---")
    
    # IMPACTO
    st.header("💡 Impacto y Conclusiones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Validaciones Positivas")
        st.markdown("""
        - **Aleatoriedad**: Los datos sugieren un sistema de sorteo aleatorio
        - **Uniformidad**: La distribución de números es aproximadamente uniforme
        - **Independencia**: Los sorteos parecen ser independientes entre sí
        - **Calidad**: Dataset completo y bien estructurado (100% completitud)
        - **Transparencia**: 18 años de historia pública disponible
        """)
    
    with col2:
        st.subheader("📊 Hallazgos Estadísticos")
        st.markdown(f"""
        - **Diversidad**: {df['número'].nunique():,} números únicos ({df['número'].nunique()/10000*100:.1f}% del espacio)
        - **Cobertura**: {df['año'].nunique()} años de datos históricos
        - **Consistencia**: Distribución estable en el tiempo
        - **Equidad**: Pares e impares aproximadamente 50-50
        - **Patrones**: No se detectaron patrones predecibles explotables
        """)
    
    st.markdown("---")
    
    # RECOMENDACIONES
    st.header("🎯 Recomendaciones")
    
    st.markdown("""
    ### Para Stakeholders:
    
    1. **Transparencia**: Continuar publicando datos históricos para mantener la confianza pública
    2. **Monitoreo**: Realizar auditorías periódicas de aleatoriedad y uniformidad
    3. **Educación**: Usar estos datos para educar sobre probabilidad y estadística
    4. **Documentación**: Mantener registros detallados de cada sorteo
    
    ### Para Analistas:
    
    1. **Actualización**: Incorporar nuevos sorteos conforme ocurran
    2. **Validación**: Repetir pruebas estadísticas periódicamente
    3. **Visualización**: Mantener dashboards actualizados
    4. **Investigación**: Explorar análisis más profundos (series temporales, clustering)
    
    ### Para el Público:
    
    1. **Comprensión**: Entender que la lotería es un juego de azar puro
    2. **Expectativas**: No existen patrones que garanticen ganar
    3. **Responsabilidad**: Jugar de manera responsable
    4. **Educación**: Usar estos datos para aprender sobre probabilidad
    """)
    
    st.markdown("---")
    
    # PRÓXIMOS PASOS
    st.header("🚀 Próximos Pasos")
    
    st.markdown("""
    1. **Integración con IA**: Usar Gemini para análisis asistido y generación de insights (ver siguiente sección)
    2. **Actualización Continua**: Incorporar nuevos sorteos automáticamente
    3. **Análisis Avanzado**: Implementar modelos de series temporales
    4. **Dashboard Público**: Publicar visualizaciones interactivas
    5. **API de Datos**: Crear API para acceso programático a los datos
    """)
    
    st.markdown("---")
    
    # LIMITACIONES
    st.header("⚠️ Limitaciones y Consideraciones")
    
    st.warning("""
    **Importante**: Este análisis tiene las siguientes limitaciones:
    
    - Es puramente descriptivo, no predictivo
    - Los patrones históricos no garantizan resultados futuros
    - La aleatoriedad perfecta es imposible de probar definitivamente
    - No incluye información sobre premios monetarios
    - Fines educativos y estadísticos únicamente
    
    **La lotería es un juego de azar. Juega responsablemente.**
    """)
    
    st.markdown("---")
    
    # DASHBOARD INTERACTIVO
    st.header("🎮 Dashboard Interactivo")
    
    st.markdown("""
    Usa los filtros para explorar los datos de manera interactiva:
    """)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        años_seleccionados = st.multiselect(
            "Filtrar por Año",
            options=sorted(df['año'].unique()),
            default=sorted(df['año'].unique())[-5:]  # Últimos 5 años por defecto
        )
    
    with col2:
        rango_numero = st.slider(
            "Rango de Números",
            0, 9999,
            (0, 9999)
        )
    
    with col3:
        rango_serie = st.slider(
            "Rango de Series",
            int(df['serie'].min()), int(df['serie'].max()),
            (int(df['serie'].min()), int(df['serie'].max()))
        )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['año'].isin(años_seleccionados)) &
        (df['número'] >= rango_numero[0]) &
        (df['número'] <= rango_numero[1]) &
        (df['serie'] >= rango_serie[0]) &
        (df['serie'] <= rango_serie[1])
    ]
    
    st.info(f"Mostrando {len(df_filtrado):,} sorteos de {len(df):,} totales")
    
    if len(df_filtrado) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(grafico_distribucion_numeros(df_filtrado), use_container_width=True)
        
        with col2:
            st.plotly_chart(grafico_distribucion_series(df_filtrado), use_container_width=True)
        
        st.dataframe(
            df_filtrado[['fecha', 'sorteo', 'número', 'serie', 'año']].sort_values('fecha', ascending=False).head(50),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados")
    
    st.success("✅ Etapa 6 completada. Procede a la siguiente sección: IA Generativa con Gemini.")

except Exception as e:
    st.error(f"❌ Error en la comunicación: {e}")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())
