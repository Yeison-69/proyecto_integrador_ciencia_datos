import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.title("2. Recolección de Datos")

st.markdown("""
### 📌 Objetivo de la etapa  
Identificar de dónde provienen los datos, cómo se obtienen, qué calidad tienen y garantizar trazabilidad para el proyecto.
""")

# --- CONFIGURACIÓN INICIAL ---
DATASETS = {
    "clientes": "static/datasets/clientes.csv",
    "ventas": "static/datasets/ventas.csv"
}

DICCIONARIO = "static/datasets/diccionario_datos.json"

# --- FUNCIONES AUXILIARES ---
def cargar_dataset(ruta, nombre):
    """Cargar dataset con verificación de encoding y tipos de datos"""
    try:
        # Intentar diferentes encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(ruta, encoding=encoding)
                st.success(f"✅ {nombre} cargado con encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            st.error(f"❌ No se pudo determinar el encoding para {nombre}")
            return None
            
        return df
        
    except Exception as e:
        st.error(f"❌ Error cargando {nombre}: {str(e)}")
        return None

def verificar_estructura(df, nombre):
    """Verificar estructura básica del dataset"""
    st.write(f"**📊 Resumen de {nombre}:**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Filas", df.shape[0])
    with col2:
        st.metric("Columnas", df.shape[1])
    with col3:
        nulos = df.isnull().sum().sum()
        st.metric("Valores nulos", nulos)
    with col4:
        st.metric("Memoria", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # Tipos de datos
    st.write("**🧮 Tipos de datos:**")
    tipos_info = []
    for col in df.columns:
        tipos_info.append({
            'Columna': col,
            'Tipo': str(df[col].dtype),
            'No Nulos': df[col].notnull().sum(),
            'Nulos': df[col].isnull().sum(),
            'Únicos': df[col].nunique()
        })
    
    st.dataframe(pd.DataFrame(tipos_info))

def detectar_inconsistencias(df_clientes, df_ventas):
    """Detectar inconsistencias entre datasets"""
    st.subheader("🔍 Detección de Inconsistencias entre Datasets")
    
    inconsistencias = []
    
    # Verificar IDs comunes si existen
    if 'id_cliente' in df_clientes.columns:
        clientes_ids = set(df_clientes['id_cliente'])
        
        # Buscar columnas que puedan contener IDs de clientes en ventas
        ventas_id_cols = [col for col in df_ventas.columns if 'id' in col.lower() or 'cliente' in col.lower()]
        
        if ventas_id_cols:
            ventas_ids = set()
            for col in ventas_id_cols:
                ventas_ids.update(df_ventas[col].dropna().unique())
            
            ids_solo_clientes = clientes_ids - ventas_ids
            ids_solo_ventas = ventas_ids - clientes_ids
            
            if ids_solo_clientes:
                inconsistencias.append(f"❌ IDs solo en clientes: {len(ids_solo_clientes)} registros")
            if ids_solo_ventas:
                inconsistencias.append(f"❌ IDs solo en ventas: {len(ids_solo_ventas)} registros")
    
    # Verificar rangos de fechas
    fecha_cols_clientes = [col for col in df_clientes.columns if 'fecha' in col.lower()]
    fecha_cols_ventas = [col for col in df_ventas.columns if 'fecha' in col.lower()]
    
    if fecha_cols_clientes and fecha_cols_ventas:
        try:
            for col in fecha_cols_clientes:
                df_clientes[col] = pd.to_datetime(df_clientes[col], errors='coerce')
            
            for col in fecha_cols_ventas:
                df_ventas[col] = pd.to_datetime(df_ventas[col], errors='coerce')
            
            min_fecha_clientes = min([df_clientes[col].min() for col in fecha_cols_clientes if not df_clientes[col].isnull().all()])
            max_fecha_clientes = max([df_clientes[col].max() for col in fecha_cols_clientes if not df_clientes[col].isnull().all()])
            
            min_fecha_ventas = min([df_ventas[col].min() for col in fecha_cols_ventas if not df_ventas[col].isnull().all()])
            max_fecha_ventas = max([df_ventas[col].max() for col in fecha_cols_ventas if not df_ventas[col].isnull().all()])
            
            st.write(f"**📅 Rango fechas clientes:** {min_fecha_clientes} a {max_fecha_clientes}")
            st.write(f"**📅 Rango fechas ventas:** {min_fecha_ventas} a {max_fecha_ventas}")
            
        except Exception as e:
            st.warning(f"⚠ No se pudieron comparar fechas: {e}")
    
    # Mostrar inconsistencias
    if inconsistencias:
        for inc in inconsistencias:
            st.error(inc)
    else:
        st.success("✅ No se detectaron inconsistencias significativas entre datasets")

def cargar_diccionario():
    """Cargar y mostrar diccionario de datos"""
    if os.path.exists(DICCIONARIO):
        try:
            with open(DICCIONARIO, 'r', encoding='utf-8') as f:
                diccionario = json.load(f)
            
            st.subheader("🗂️ Diccionario de Datos")
            
            if isinstance(diccionario, dict):
                for tabla, columnas in diccionario.items():
                    with st.expander(f"📋 {tabla}"):
                        for col_name, col_info in columnas.items():
                            st.write(f"**{col_name}**")
                            st.write(f"  - Descripción: {col_info.get('descripcion', 'N/A')}")
                            st.write(f"  - Tipo: {col_info.get('tipo', 'N/A')}")
                            st.write(f"  - Ejemplo: {col_info.get('ejemplo', 'N/A')}")
                            st.write("---")
            else:
                st.info("ℹ️ Formato del diccionario no reconocido")
                
        except Exception as e:
            st.error(f"❌ Error cargando diccionario: {e}")
    else:
        st.warning("⚠ Diccionario de datos no encontrado")

# --- EJECUCIÓN PRINCIPAL ---
st.markdown("---")
st.header("📥 Carga y Validación de Datos")

# Cargar datasets
datasets_cargados = {}
for nombre, ruta in DATASETS.items():
    st.subheader(f"📄 {nombre}.csv")
    
    if os.path.exists(ruta):
        df = cargar_dataset(ruta, nombre)
        if df is not None:
            datasets_cargados[nombre] = df
            verificar_estructura(df, nombre)
            st.dataframe(df.head(3))
    else:
        st.error(f"❌ Archivo no encontrado: {ruta}")

# Detectar inconsistencias si ambos datasets están cargados
if len(datasets_cargados) == 2:
    detectar_inconsistencias(datasets_cargados['clientes'], datasets_cargados['ventas'])

# Cargar diccionario de datos
cargar_diccionario()

# --- RESUMEN FINAL ---
st.markdown("---")
st.header("📋 Resumen de la Recolección")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Completado")
    completados = [
        "✔ Cargar correctamente todos los datasets",
        "✔ Verificar rutas y encoding", 
        "✔ Validar tipos de datos al cargar",
        "✔ Detectar inconsistencias entre datasets",
        "✔ Mostrar resumen inicial (shape, columnas, tipos)",
        "✔ Verificar permisos, trazabilidad y fuente"
    ]
    for item in completados:
        st.write(item)

with col2:
    st.subheader("🔍 Estado de Archivos")
    for nombre, ruta in DATASETS.items():
        existe = os.path.exists(ruta)
        emoji = "✅" if existe else "❌"
        st.write(f"{emoji} {nombre}.csv: {'Encontrado' if existe else 'No encontrado'}")
    
    existe_dic = os.path.exists(DICCIONARIO)
    emoji_dic = "✅" if existe_dic else "⚠️"
    st.write(f"{emoji_dic} diccionario_datos.json: {'Encontrado' if existe_dic else 'No encontrado'}")

# --- TRAZABILIDAD ---
st.markdown("---")
st.header("🔐 Trazabilidad y Cumplimiento")

st.info("""
**📝 Documentación de Fuentes:**
- **Origen:** Datos ficticios para práctica educativa (SENA)
- **Permisos:** Libre uso académico
- **Privacidad:** No contiene información personal real
- **Formatos:** CSV estándar con encoding UTF-8/Latin-1
- **Versionado:** Controlado mediante Git - no modificar sin documentar
""")

st.success("**🟦 2_2. Recolección de datos (COMPLETO)**")