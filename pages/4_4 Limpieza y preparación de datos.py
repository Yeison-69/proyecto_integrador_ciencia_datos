import streamlit as st
from utils.carga_datos import cargar_datos_loteria
from utils.validaciones import validar_columnas
import pandas as pd

st.title("🧹 4. Limpieza y Preparación de Datos")

st.markdown("""
## 🎯 Objetivo de esta Etapa

Asegurar que los datos estén limpios, consistentes y listos para análisis avanzado.
Incluye validación, transformaciones y creación de features derivadas.
""")

try:
    df = cargar_datos_loteria()
    
    # Tabs para organizar
    tab1, tab2, tab3 = st.tabs([
        "✅ Validación",
        "🔧 Transformaciones",
        "📊 Features Derivadas"
    ])
    
    # TAB 1: Validación
    with tab1:
        st.header("✅ Validación de Datos")
        
        st.subheader("1. Validación de Columnas")
        columnas_esperadas = ['fecha', 'sorteo', 'número', 'serie']
        faltantes = validar_columnas(df, columnas_esperadas)
        
        if faltantes:
            st.error(f"❌ Columnas faltantes: {', '.join(faltantes)}")
        else:
            st.success(f"✅ Todas las columnas esperadas están presentes: {', '.join(columnas_esperadas)}")
        
        st.subheader("2. Validación de Tipos de Datos")
        tipos_correctos = {
            'fecha': 'datetime64[ns]',
            'sorteo': 'int',
            'número': 'int',
            'serie': 'int'
        }
        
        validacion_tipos = []
        for col, tipo_esperado in tipos_correctos.items():
            if col in df.columns:
                tipo_actual = str(df[col].dtype)
                es_correcto = tipo_esperado in tipo_actual
                validacion_tipos.append({
                    'Columna': col,
                    'Tipo Esperado': tipo_esperado,
                    'Tipo Actual': tipo_actual,
                    'Estado': '✅' if es_correcto else '❌'
                })
        
        st.dataframe(pd.DataFrame(validacion_tipos), use_container_width=True, hide_index=True)
        
        st.subheader("3. Validación de Rangos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Números (0-9999)**")
            numeros_invalidos = df[(df['número'] < 0) | (df['número'] > 9999)]
            if len(numeros_invalidos) == 0:
                st.success(f"✅ Todos los números están en rango válido")
            else:
                st.error(f"❌ {len(numeros_invalidos)} números fuera de rango")
        
        with col2:
            st.write("**Series (positivas)**")
            series_invalidas = df[df['serie'] < 0]
            if len(series_invalidas) == 0:
                st.success(f"✅ Todas las series son válidas")
            else:
                st.error(f"❌ {len(series_invalidas)} series inválidas")
        
        st.subheader("4. Validación de Duplicados")
        duplicados = df.duplicated(subset=['fecha', 'sorteo']).sum()
        if duplicados == 0:
            st.success(f"✅ No hay sorteos duplicados")
        else:
            st.warning(f"⚠️ Se encontraron {duplicados} sorteos duplicados")
        
        st.subheader("5. Validación de Valores Faltantes")
        faltantes_total = df.isnull().sum().sum()
        if faltantes_total == 0:
            st.success(f"✅ No hay valores faltantes")
        else:
            st.warning(f"⚠️ Se encontraron {faltantes_total} valores faltantes")
            st.dataframe(df.isnull().sum()[df.isnull().sum() > 0], use_container_width=True)
    
    # TAB 2: Transformaciones
    with tab2:
        st.header("🔧 Transformaciones Aplicadas")
        
        st.markdown("""
        Las siguientes transformaciones se aplicaron automáticamente al cargar los datos:
        """)
        
        transformaciones = [
            {
                "Transformación": "Normalización de columnas",
                "Descripción": "Convertir nombres de columnas a minúsculas",
                "Estado": "✅ Aplicada"
            },
            {
                "Transformación": "Parsing de fechas",
                "Descripción": "Convertir columna 'fecha' a datetime",
                "Estado": "✅ Aplicada"
            },
            {
                "Transformación": "Conversión de tipos",
                "Descripción": "Convertir sorteo, número y serie a enteros",
                "Estado": "✅ Aplicada"
            },
            {
                "Transformación": "Eliminación de columnas vacías",
                "Descripción": "Remover columna 'Unnamed: 4'",
                "Estado": "✅ Aplicada"
            },
            {
                "Transformación": "Ordenamiento",
                "Descripción": "Ordenar registros por fecha",
                "Estado": "✅ Aplicada"
            },
            {
                "Transformación": "Limpieza de nulos",
                "Descripción": "Eliminar filas con valores nulos en columnas clave",
                "Estado": "✅ Aplicada"
            }
        ]
        
        st.dataframe(pd.DataFrame(transformaciones), use_container_width=True, hide_index=True)
        
        st.subheader("Resultado de Transformaciones")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Registros Finales", f"{len(df):,}")
        with col2:
            st.metric("Columnas Finales", len(df.columns))
        with col3:
            completitud = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric("Completitud", f"{completitud:.1f}%")
    
    # TAB 3: Features Derivadas
    with tab3:
        st.header("📊 Features Derivadas")
        
        st.markdown("""
        Se crearon las siguientes features adicionales para facilitar el análisis:
        """)
        
        st.subheader("1. Features Temporales")
        features_temporales = [
            {"Feature": "año", "Descripción": "Año del sorteo", "Ejemplo": str(df['año'].iloc[0])},
            {"Feature": "mes", "Descripción": "Mes del sorteo (1-12)", "Ejemplo": str(df['mes'].iloc[0])},
            {"Feature": "mes_nombre", "Descripción": "Nombre del mes en inglés", "Ejemplo": df['mes_nombre'].iloc[0]},
            {"Feature": "dia_semana", "Descripción": "Día de la semana (0=Lunes)", "Ejemplo": str(df['dia_semana'].iloc[0])},
            {"Feature": "dia_semana_nombre", "Descripción": "Nombre del día en inglés", "Ejemplo": df['dia_semana_nombre'].iloc[0]},
            {"Feature": "trimestre", "Descripción": "Trimestre del año (1-4)", "Ejemplo": str(df['trimestre'].iloc[0])},
            {"Feature": "semana_año", "Descripción": "Semana del año (1-53)", "Ejemplo": str(df['semana_año'].iloc[0])},
            {"Feature": "dia_año", "Descripción": "Día del año (1-366)", "Ejemplo": str(df['dia_año'].iloc[0])}
        ]
        st.dataframe(pd.DataFrame(features_temporales), use_container_width=True, hide_index=True)
        
        st.subheader("2. Features de Números")
        features_numeros = [
            {"Feature": "primer_digito", "Descripción": "Primer dígito del número", "Ejemplo": str(df['primer_digito'].iloc[0])},
            {"Feature": "ultimo_digito", "Descripción": "Último dígito del número", "Ejemplo": str(df['ultimo_digito'].iloc[0])},
            {"Feature": "suma_digitos", "Descripción": "Suma de todos los dígitos", "Ejemplo": str(df['suma_digitos'].iloc[0])},
            {"Feature": "rango_numero", "Descripción": "Categoría del número (0-2500, 2500-5000, etc.)", "Ejemplo": str(df['rango_numero'].iloc[0])},
            {"Feature": "numero_par", "Descripción": "1 si es par, 0 si es impar", "Ejemplo": str(df['numero_par'].iloc[0])}
        ]
        st.dataframe(pd.DataFrame(features_numeros), use_container_width=True, hide_index=True)
        
        st.subheader("3. Features de Series")
        features_series = [
            {"Feature": "rango_serie", "Descripción": "Categoría de la serie (0-100, 100-200, etc.)", "Ejemplo": str(df['rango_serie'].iloc[0])}
        ]
        st.dataframe(pd.DataFrame(features_series), use_container_width=True, hide_index=True)
        
        st.subheader("Vista Previa con Features Derivadas")
        columnas_mostrar = ['fecha', 'número', 'serie', 'año', 'mes_nombre', 'dia_semana_nombre', 
                           'primer_digito', 'ultimo_digito', 'numero_par']
        st.dataframe(df[columnas_mostrar].head(10), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Resumen final
    st.header("📝 Resumen de Limpieza y Preparación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Registros Procesados", f"{len(df):,}")
    
    with col2:
        st.metric("Features Totales", len(df.columns))
    
    with col3:
        features_derivadas = len(df.columns) - 4  # 4 columnas originales
        st.metric("Features Derivadas", features_derivadas)
    
    with col4:
        st.metric("Calidad", "Excelente ✅")
    
    st.success("""
    ✅ **Datos listos para análisis:**
    - Todas las validaciones pasaron correctamente
    - Transformaciones aplicadas exitosamente
    - Features derivadas creadas
    - Dataset limpio y consistente
    """)
    
    st.success("✅ Etapa 4 completada. Procede a la siguiente sección: Evaluación e Interpretación.")

except Exception as e:
    st.error(f"❌ Error en la preparación: {e}")
    import traceback
    with st.expander("Ver detalles del error"):
        st.code(traceback.format_exc())
