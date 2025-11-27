import streamlit as st
from utils.carga_datos import cargar_datos_loteria
from utils.eda_helpers import *
from utils.graficos import *
import pandas as pd
from scipy import stats

st.title("📈 5. Evaluación e Interpretación de Resultados")

st.markdown("""
## 🎯 Objetivo de esta Etapa

Evaluar los hallazgos del análisis exploratorio, realizar pruebas estadísticas y generar insights accionables
basados en los datos históricos de la lotería.
""")

try:
    df = cargar_datos_loteria()
    
    # Tabs para organizar
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Métricas Clave",
        "🔬 Pruebas Estadísticas",
        "💡 Insights",
        "📋 Interpretación"
    ])
    
    # TAB 1: Métricas Clave
    with tab1:
        st.header("📊 Métricas Clave del Análisis")
        
        st.subheader("KPIs Principales")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Cobertura Temporal",
                f"{df['año'].nunique()} años",
                delta=f"{df['año'].min()}-{df['año'].max()}"
            )
        
        with col2:
            completitud = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric(
                "Completitud",
                f"{completitud:.1f}%",
                delta="Excelente" if completitud > 95 else "Revisar"
            )
        
        with col3:
            numeros_unicos = df['número'].nunique()
            st.metric(
                "Números Únicos",
                f"{numeros_unicos:,}",
                delta=f"{(numeros_unicos/10000*100):.1f}% del total"
            )
        
        with col4:
            series_unicas = df['serie'].nunique()
            st.metric(
                "Series Únicas",
                f"{series_unicas:,}",
                delta=f"{len(df)} sorteos"
            )
        
        st.subheader("Frecuencia de Sorteos")
        
        sorteos_año = df.groupby('año').size()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Promedio por Año", f"{sorteos_año.mean():.1f}")
        
        with col2:
            st.metric("Año con Más Sorteos", f"{sorteos_año.idxmax()} ({sorteos_año.max()})")
        
        with col3:
            st.metric("Año con Menos Sorteos", f"{sorteos_año.idxmin()} ({sorteos_año.min()})")
        
        st.plotly_chart(grafico_evolucion_por_año(df), use_container_width=True)
        
        st.subheader("Distribución de Números y Series")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Estadísticas de Números**")
            st.write(f"Media: {df['número'].mean():.2f}")
            st.write(f"Mediana: {df['número'].median():.0f}")
            st.write(f"Desv. Estándar: {df['número'].std():.2f}")
            st.write(f"Coef. Variación: {(df['número'].std()/df['número'].mean()*100):.2f}%")
        
        with col2:
            st.write("**Estadísticas de Series**")
            st.write(f"Media: {df['serie'].mean():.2f}")
            st.write(f"Mediana: {df['serie'].median():.0f}")
            st.write(f"Desv. Estándar: {df['serie'].std():.2f}")
            st.write(f"Coef. Variación: {(df['serie'].std()/df['serie'].mean()*100):.2f}%")
    
    # TAB 2: Pruebas Estadísticas
    with tab2:
        st.header("🔬 Pruebas Estadísticas")
        
        st.subheader("1. Prueba de Uniformidad (Chi-cuadrado)")
        st.markdown("""
        Evaluamos si los números ganadores siguen una distribución uniforme (todos tienen la misma probabilidad).
        """)
        
        # Agrupar números en bins para chi-cuadrado
        bins = 20
        observed, bin_edges = np.histogram(df['número'], bins=bins, range=(0, 10000))
        expected = len(df) / bins
        
        chi2_stat, p_value = stats.chisquare(observed, f_exp=[expected]*bins)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Estadístico χ²", f"{chi2_stat:.2f}")
        
        with col2:
            st.metric("P-value", f"{p_value:.4f}")
        
        with col3:
            if p_value > 0.05:
                st.metric("Resultado", "Uniforme ✅")
            else:
                st.metric("Resultado", "No Uniforme ⚠️")
        
        if p_value > 0.05:
            st.success(f"✅ No se rechaza la hipótesis de uniformidad (p-value = {p_value:.4f} > 0.05). Los números parecen distribuirse uniformemente.")
        else:
            st.warning(f"⚠️ Se rechaza la hipótesis de uniformidad (p-value = {p_value:.4f} < 0.05). Puede haber sesgos en la distribución.")
        
        st.subheader("2. Prueba de Normalidad (Shapiro-Wilk)")
        
        # Tomar muestra si hay muchos datos
        muestra = df['número'].sample(min(5000, len(df)))
        stat_shapiro, p_shapiro = stats.shapiro(muestra)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Estadístico W", f"{stat_shapiro:.4f}")
        
        with col2:
            st.metric("P-value", f"{p_shapiro:.4f}")
        
        if p_shapiro > 0.05:
            st.info(f"Los números siguen una distribución normal (p-value = {p_shapiro:.4f})")
        else:
            st.info(f"Los números NO siguen una distribución normal (p-value = {p_shapiro:.4f})")
        
        st.subheader("3. Prueba de Independencia (Autocorrelación)")
        
        # Calcular autocorrelación lag-1
        numeros_array = df.sort_values('fecha')['número'].values
        if len(numeros_array) > 1:
            autocorr = np.corrcoef(numeros_array[:-1], numeros_array[1:])[0, 1]
            
            st.metric("Autocorrelación (lag-1)", f"{autocorr:.4f}")
            
            if abs(autocorr) < 0.1:
                st.success(f"✅ Los sorteos parecen ser independientes (autocorrelación ≈ 0)")
            else:
                st.warning(f"⚠️ Posible dependencia entre sorteos consecutivos")
        
        st.subheader("4. Análisis de Pares vs Impares")
        
        pares = (df['numero_par'] == 1).sum()
        impares = (df['numero_par'] == 0).sum()
        
        # Prueba binomial
        p_pares = pares / len(df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Números Pares", f"{pares} ({p_pares*100:.1f}%)")
        
        with col2:
            st.metric("Números Impares", f"{impares} ({(1-p_pares)*100:.1f}%)")
        
        with col3:
            diferencia = abs(p_pares - 0.5) * 100
            st.metric("Diferencia del 50%", f"{diferencia:.1f}%")
        
        if abs(p_pares - 0.5) < 0.05:
            st.success("✅ La proporción de pares e impares es aproximadamente 50-50")
        else:
            st.info(f"ℹ️ Hay un ligero sesgo hacia números {'pares' if p_pares > 0.5 else 'impares'}")
    
    # TAB 3: Insights
    with tab3:
        st.header("💡 Insights Principales")
        
        st.subheader("🎲 Sobre los Números Ganadores")
        
        numero_mas_frecuente = df['número'].mode()[0]
        frecuencia_max = (df['número'] == numero_mas_frecuente).sum()
        
        st.markdown(f"""
        1. **Número más frecuente**: {numero_mas_frecuente:04d} (apareció {frecuencia_max} veces)
        2. **Diversidad**: {df['número'].nunique():,} números únicos de 10,000 posibles ({df['número'].nunique()/10000*100:.1f}%)
        3. **Distribución**: {'Aproximadamente uniforme' if p_value > 0.05 else 'Con algunos sesgos'}
        4. **Pares vs Impares**: {pares} pares ({p_pares*100:.1f}%) vs {impares} impares ({(1-p_pares)*100:.1f}%)
        """)
        
        st.subheader("🎫 Sobre las Series")
        
        serie_mas_frecuente = df['serie'].mode()[0]
        frecuencia_serie = (df['serie'] == serie_mas_frecuente).sum()
        
        st.markdown(f"""
        1. **Serie más frecuente**: {serie_mas_frecuente} (apareció {frecuencia_serie} veces)
        2. **Diversidad**: {df['serie'].nunique():,} series únicas
        3. **Rango**: {df['serie'].min()} a {df['serie'].max()}
        4. **Promedio**: {df['serie'].mean():.0f}
        """)
        
        st.subheader("📅 Sobre los Patrones Temporales")
        
        dia_mas_comun = df['dia_semana_nombre'].mode()[0]
        sorteos_dia = (df['dia_semana_nombre'] == dia_mas_comun).sum()
        
        mes_mas_comun = df['mes_nombre'].mode()[0]
        sorteos_mes = (df['mes_nombre'] == mes_mas_comun).sum()
        
        st.markdown(f"""
        1. **Día más común**: {dia_mas_comun} ({sorteos_dia} sorteos)
        2. **Mes más común**: {mes_mas_comun} ({sorteos_mes} sorteos)
        3. **Frecuencia promedio**: {sorteos_año.mean():.1f} sorteos por año
        4. **Tendencia**: {'Creciente' if df.groupby('año').size().corr(pd.Series(range(len(sorteos_año)))) > 0 else 'Decreciente'} en el tiempo
        """)
        
        st.subheader("🔢 Sobre los Dígitos")
        
        primer_digito_comun = df['primer_digito'].mode()[0]
        ultimo_digito_comun = df['ultimo_digito'].mode()[0]
        
        st.markdown(f"""
        1. **Primer dígito más común**: {primer_digito_comun}
        2. **Último dígito más común**: {ultimo_digito_comun}
        3. **Suma promedio de dígitos**: {df['suma_digitos'].mean():.1f}
        """)
    
    # TAB 4: Interpretación
    with tab4:
        st.header("📋 Interpretación General")
        
        st.markdown(f"""
        ## Resumen Ejecutivo
        
        Basado en el análisis de **{len(df):,} sorteos** realizados entre **{df['año'].min()}** y **{df['año'].max()}**:
        
        ### ✅ Validación de Aleatoriedad
        
        - Los datos sugieren un sistema de sorteo {'razonablemente aleatorio' if p_value > 0.05 else 'con algunos patrones no aleatorios'}
        - La distribución de números es {'aproximadamente uniforme' if p_value > 0.05 else 'no completamente uniforme'}
        - Los sorteos parecen ser {'independientes' if abs(autocorr) < 0.1 else 'potencialmente dependientes'} entre sí
        
        ### 📊 Características del Dataset
        
        - **Completitud**: {completitud:.1f}% - Excelente calidad de datos
        - **Cobertura**: {df['año'].nunique()} años de historia
        - **Diversidad**: {df['número'].nunique():,} números únicos ({df['número'].nunique()/10000*100:.1f}% del espacio posible)
        
        ### 🎯 Implicaciones
        
        1. **Para jugadores**: No hay evidencia de patrones predecibles que puedan explotarse
        2. **Para analistas**: El dataset es robusto y adecuado para análisis estadístico
        3. **Para el sistema**: Los resultados sugieren un mecanismo de sorteo justo
        
        ### ⚠️ Limitaciones
        
        - El análisis es descriptivo, no predictivo
        - Los patrones históricos no garantizan resultados futuros
        - La aleatoriedad perfecta es imposible de probar definitivamente
        
        ### 💡 Recomendaciones
        
        1. Continuar monitoreando la distribución de números en el tiempo
        2. Realizar auditorías periódicas de aleatoriedad
        3. Mantener la transparencia en los procesos de sorteo
        4. Usar estos datos para educación sobre probabilidad y estadística
        """)
        
        st.info("""
        **Nota Importante**: Este análisis tiene fines educativos y estadísticos. 
        La lotería es un juego de azar y ningún análisis puede predecir resultados futuros.
        """)
    
    st.markdown("---")
    st.success("✅ Etapa 5 completada. Procede a la siguiente sección: Comunicación de Resultados.")

except Exception as e:
    st.error(f"❌ Error en la evaluación: {e}")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())
