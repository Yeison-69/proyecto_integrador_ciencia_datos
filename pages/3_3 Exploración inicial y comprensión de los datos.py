import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# Configuración de la página
st.set_page_config(page_title="EDA Completo", layout="wide")
st.title("📊 Exploración Inicial y Comprensión de los Datos")

# --- 1. Cargar el archivo ---
st.subheader("Cargar archivo CSV")
uploaded_file = st.file_uploader("Sube el archivo clientes.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # --- 2. Convertir fechas correctamente ---
    fecha_cols = ["fecha_alta", "fecha_ultima_compra"]
    for col in fecha_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    st.success("Archivo cargado correctamente ✔️")

    # --- 3. VISTA PREVIA DE DATOS ---
    st.header("👀 Vista Previa de Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Primeros registros (head)")
        st.dataframe(df.head(10))
    
    with col2:
        st.subheader("Últimos registros (tail)")
        st.dataframe(df.tail(10))

    # --- 4. RESUMEN DEL DATASET ---
    st.header("📋 Resumen del Dataset")
    
    # Métricas clave
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total de registros", len(df))
    with col2:
        st.metric("Columnas", df.shape[1])
    with col3:
        missing_values = df.isnull().sum().sum()
        st.metric("Valores faltantes", missing_values)
    with col4:
        duplicados = df.duplicated().sum()
        st.metric("Registros duplicados", duplicados)
    with col5:
        st.metric("Memoria usada", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

    # Tipos de datos
    st.subheader("🧮 Tipos de Datos por Columna")
    tipos_datos = []
    for columna in df.columns:
        tipo = str(df[columna].dtype)
        no_nulos = df[columna].notnull().sum()
        nulos = df[columna].isnull().sum()
        valores_unicos = df[columna].nunique()
        
        tipos_datos.append({
            'Columna': columna,
            'Tipo': tipo,
            'No Nulos': f"{no_nulos} ({no_nulos/len(df)*100:.1f}%)",
            'Nulos': f"{nulos} ({nulos/len(df)*100:.1f}%)",
            'Valores Únicos': valores_unicos
        })
    
    tipos_df = pd.DataFrame(tipos_datos)
    st.dataframe(tipos_df, use_container_width=True)

    # --- 5. ANÁLISIS DE VALORES FALTANTES Y DUPLICADOS ---
    st.header("🔍 Calidad de Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Valores Nulos por Columna")
        if df.isnull().sum().sum() > 0:
            nulos_por_columna = df.isnull().sum()
            nulos_por_columna = nulos_por_columna[nulos_por_columna > 0]
            fig, ax = plt.subplots(figsize=(10, 6))
            nulos_por_columna.plot(kind='bar', ax=ax, color='red')
            plt.title('Valores Nulos por Columna')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.success("✅ No hay valores nulos en el dataset")
    
    with col2:
        st.subheader("Registros Duplicados")
        if duplicados > 0:
            st.error(f"❌ Se encontraron {duplicados} registros duplicados")
            st.dataframe(df[df.duplicated(keep=False)].head())
        else:
            st.success("✅ No hay registros duplicados")

    # --- 6. ANÁLISIS DE VARIABLES NUMÉRICAS ---
    st.header("📈 Análisis de Variables Numéricas")
    
    # Estadísticas descriptivas
    st.subheader("Estadísticas Descriptivas")
    columnas_numericas = df.select_dtypes(include=[np.number]).columns
    if len(columnas_numericas) > 0:
        st.dataframe(df[columnas_numericas].describe())
        
        # Histogramas
        st.subheader("Histogramas de Variables Numéricas")
        cols_per_row = 3
        columnas_por_fila = [columnas_numericas[i:i+cols_per_row] for i in range(0, len(columnas_numericas), cols_per_row)]
        
        for fila in columnas_por_fila:
            cols = st.columns(len(fila))
            for i, col_name in enumerate(fila):
                with cols[i]:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    df[col_name].hist(bins=20, ax=ax)
                    ax.set_title(f'Histograma de {col_name}')
                    st.pyplot(fig)
        
        # Boxplots para outliers
        st.subheader("📦 Detección de Valores Atípicos (Boxplots)")
        for fila in columnas_por_fila:
            cols = st.columns(len(fila))
            for i, col_name in enumerate(fila):
                with cols[i]:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    df.boxplot(column=col_name, ax=ax)
                    ax.set_title(f'Boxplot de {col_name}')
                    st.pyplot(fig)
        
        # Análisis de outliers específico
        st.subheader("🔎 Resumen de Valores Atípicos")
        outliers_info = []
        for col in columnas_numericas:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            
            outliers_info.append({
                'Columna': col,
                'Total Outliers': len(outliers),
                'Porcentaje': f"{(len(outliers)/len(df))*100:.2f}%",
                'Rango Normal': f"[{lower_bound:.2f}, {upper_bound:.2f}]"
            })
        
        st.dataframe(pd.DataFrame(outliers_info))

    # --- 7. ANÁLISIS DE VARIABLES CATEGÓRICAS ---
    st.header("🏷️ Análisis de Variables Categóricas")
    
    columnas_categoricas = df.select_dtypes(include=['object']).columns
    if len(columnas_categoricas) > 0:
        st.subheader("Estadísticas Categóricas")
        
        for col in columnas_categoricas:
            with st.expander(f"{col} ({df[col].nunique()} categorías)"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Categorías únicas", df[col].nunique())
                    st.metric("Moda", df[col].mode().iloc[0] if not df[col].mode().empty else "N/A")
                with col2:
                    st.write("**Valores únicos:**", list(df[col].unique()))
                
                # Gráfico de barras
                st.write("**Distribución:**")
                fig, ax = plt.subplots(figsize=(10, 6))
                df[col].value_counts().plot(kind='bar', ax=ax)
                plt.title(f'Distribución de {col}')
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
                # Tabla de frecuencias
                st.write("**Frecuencias:**")
                frecuencias = df[col].value_counts().reset_index()
                frecuencias.columns = ['Valor', 'Frecuencia']
                frecuencias['Porcentaje'] = (frecuencias['Frecuencia'] / len(df)) * 100
                st.dataframe(frecuencias)

    # --- 8. ANÁLISIS DE CORRELACIONES ---
    st.header("🔗 Análisis de Correlaciones")
    
    if len(columnas_numericas) > 1:
        # Matriz de correlación
        st.subheader("Matriz de Correlación")
        corr_matrix = df[columnas_numericas].corr()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Tabla de Correlaciones:**")
            # Crear heatmap básico con matplotlib
            fig, ax = plt.subplots(figsize=(10, 8))
            im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            
            # Mostrar valores en las celdas
            for i in range(len(corr_matrix.columns)):
                for j in range(len(corr_matrix.columns)):
                    text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                 ha="center", va="center", color="black", fontsize=10)
            
            ax.set_xticks(range(len(corr_matrix.columns)))
            ax.set_yticks(range(len(corr_matrix.columns)))
            ax.set_xticklabels(corr_matrix.columns, rotation=45)
            ax.set_yticklabels(corr_matrix.columns)
            ax.set_title('Matriz de Correlación')
            plt.colorbar(im, ax=ax)
            st.pyplot(fig)
        
        with col2:
            st.write("**Correlaciones Numéricas:**")
            st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm', vmin=-1, vmax=1))
        
        # Scatter plots para correlaciones fuertes
        st.subheader("📊 Scatter Plots - Relaciones entre Variables")
        
        # Encontrar las correlaciones más fuertes
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'Var1': corr_matrix.columns[i],
                    'Var2': corr_matrix.columns[j],
                    'Correlacion': abs(corr_matrix.iloc[i, j])
                })
        
        corr_df = pd.DataFrame(corr_pairs)
        top_correlations = corr_df.nlargest(3, 'Correlacion')
        
        for _, pair in top_correlations.iterrows():
            if pair['Correlacion'] > 0.3:  # Solo mostrar correlaciones significativas
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.scatter(df[pair['Var1']], df[pair['Var2']], alpha=0.6)
                ax.set_xlabel(pair['Var1'])
                ax.set_ylabel(pair['Var2'])
                ax.set_title(f"{pair['Var1']} vs {pair['Var2']} (corr: {pair['Correlacion']:.2f})")
                st.pyplot(fig)

    # --- 9. ANÁLISIS TEMPORAL ---
    st.header("⏰ Análisis Temporal")
    
    columnas_fecha = df.select_dtypes(include=['datetime64']).columns
    if len(columnas_fecha) > 0:
        for col_fecha in columnas_fecha:
            st.subheader(f"Análisis de {col_fecha}")
            
            # Resumen de fechas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Fecha mínima", df[col_fecha].min())
            with col2:
                st.metric("Fecha máxima", df[col_fecha].max())
            with col3:
                st.metric("Rango total", f"{(df[col_fecha].max() - df[col_fecha].min()).days} días")

    # --- 10. RESUMEN FINAL DE HALLAZGOS ---
    st.header("📝 Resumen Final de Hallazgos del EDA")
    
    with st.expander("🔍 Resumen Ejecutivo", expanded=True):
        st.subheader("✅ Puntos Fuertes")
        if missing_values == 0:
            st.write("• No hay valores nulos en el dataset")
        if duplicados == 0:
            st.write("• No hay registros duplicados")
        if len(columnas_numericas) > 0:
            st.write(f"• {len(columnas_numericas)} variables numéricas para análisis")
        if len(columnas_categoricas) > 0:
            st.write(f"• {len(columnas_categoricas)} variables categóricas para segmentación")
        
        st.subheader("⚠️ Áreas de Atención")
        if missing_values > 0:
            st.write(f"• Existen {missing_values} valores nulos que requieren tratamiento")
        if duplicados > 0:
            st.write(f"• Existen {duplicados} registros duplicados que deben eliminarse")
        
        # CORRECCIÓN: Manejar correctamente los porcentajes con decimales
        outliers_significativos = False
        if 'outliers_info' in locals() and outliers_info:
            for info in outliers_info:
                # Convertir el string del porcentaje a float correctamente
                porcentaje_str = info['Porcentaje'].replace('%', '')
                try:
                    if float(porcentaje_str) > 5:
                        outliers_significativos = True
                        break
                except ValueError:
                    continue
        
        if outliers_significativos:
            st.write("• Se detectaron valores atípicos que pueden afectar los modelos")
        
        st.subheader("🎯 Recomendaciones")
        st.write("• Considerar imputación para valores nulos si es necesario")
        st.write("• Evaluar el impacto de los outliers en los análisis")
        st.write("• Aprovechar las variables categóricas para segmentación de clientes")
        st.write("• Utilizar las correlaciones identificadas para feature engineering")

else:
    st.info("⏳ Esperando que subas el archivo CSV…")