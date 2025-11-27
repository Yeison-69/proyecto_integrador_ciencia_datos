import os
import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos_loteria():
    """
    Carga los datos de la lotería con parsing de fechas y features derivadas.
    Usa caché de Streamlit para mejor rendimiento.
    
    Returns:
        pd.DataFrame: DataFrame con los datos procesados
    """
    # Nombre esperado
    filename = "premio_mayor_loteria_medellin.csv"

    # Ruta principal
    ruta = os.path.join("data", filename)

    # Si NO existe, intentar buscarlo dentro de /data/
    if not os.path.exists(ruta):
        posibles = os.listdir("data")
        print("Archivos encontrados en /data/:", posibles)

        # Buscar coincidencias IGNORANDO may/minus
        for file in posibles:
            if file.lower() == filename.lower():
                ruta = os.path.join("data", file)
                break

    # Si aún no existe → ERROR
    if not os.path.exists(ruta):
        raise FileNotFoundError(
            f"No se encontró el archivo en: {ruta}\n"
            f"Archivos disponibles: {os.listdir('data')}"
        )

    # Cargar CSV con parsing de fechas
    df = pd.read_csv(ruta)
    
    # Renombrar columnas a minúsculas para consistencia
    df.columns = df.columns.str.lower().str.strip()
    
    # Convertir fecha a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    
    # Eliminar filas con fechas inválidas
    df = df.dropna(subset=['fecha'])
    
    # Convertir columnas numéricas
    df['sorteo'] = pd.to_numeric(df['sorteo'], errors='coerce')
    df['número'] = pd.to_numeric(df['número'], errors='coerce')
    df['serie'] = pd.to_numeric(df['serie'], errors='coerce')
    
    # Eliminar la columna sin nombre si existe
    if 'unnamed: 4' in df.columns:
        df = df.drop(columns=['unnamed: 4'])
    
    # Eliminar filas con valores nulos en columnas clave
    df = df.dropna(subset=['sorteo', 'número', 'serie'])
    
    # Convertir a enteros
    df['sorteo'] = df['sorteo'].astype(int)
    df['número'] = df['número'].astype(int)
    df['serie'] = df['serie'].astype(int)
    
    # Ordenar por fecha
    df = df.sort_values('fecha').reset_index(drop=True)
    
    # Extraer features temporales
    df = extraer_features_temporales(df)
    
    # Agregar features adicionales
    df = agregar_features_analisis(df)
    
    return df

def extraer_features_temporales(df):
    """
    Extrae features temporales de la columna fecha.
    
    Args:
        df: DataFrame con columna 'fecha'
    
    Returns:
        DataFrame con features adicionales
    """
    if 'fecha' in df.columns:
        df['año'] = df['fecha'].dt.year
        df['mes'] = df['fecha'].dt.month
        df['mes_nombre'] = df['fecha'].dt.month_name()
        df['dia_semana'] = df['fecha'].dt.dayofweek
        df['dia_semana_nombre'] = df['fecha'].dt.day_name()
        df['trimestre'] = df['fecha'].dt.quarter
        df['semana_año'] = df['fecha'].dt.isocalendar().week
        df['dia_año'] = df['fecha'].dt.dayofyear
    
    return df

def agregar_features_analisis(df):
    """
    Agrega features útiles para análisis.
    
    Args:
        df: DataFrame con datos de lotería
    
    Returns:
        DataFrame con features adicionales
    """
    # Dígitos del número
    df['primer_digito'] = df['número'].astype(str).str[0].astype(int)
    df['ultimo_digito'] = df['número'] % 10
    df['suma_digitos'] = df['número'].astype(str).apply(lambda x: sum(int(d) for d in x))
    
    # Categorías de número
    df['rango_numero'] = pd.cut(df['número'], bins=[0, 2500, 5000, 7500, 10000], 
                                  labels=['0-2500', '2500-5000', '5000-7500', '7500-10000'])
    
    # Categorías de serie
    df['rango_serie'] = pd.cut(df['serie'], bins=[0, 100, 200, 300, 1000], 
                                 labels=['0-100', '100-200', '200-300', '300+'])
    
    # Número par/impar
    df['numero_par'] = (df['número'] % 2 == 0).astype(int)
    
    return df

def obtener_metadata_dataset():
    """
    Retorna metadata del dataset.
    
    Returns:
        dict: Diccionario con información del dataset
    """
    return {
        "nombre": "Sorteos de la Lotería de Medellín",
        "fuente": "Datos históricos de sorteos 2007-2025",
        "periodo": "2007-2025",
        "frecuencia": "Semanal (aproximadamente 1-2 sorteos por semana)",
        "variables": {
            "fecha": "Fecha del sorteo",
            "sorteo": "Número consecutivo del sorteo",
            "número": "Número ganador (4 dígitos, 0-9999)",
            "serie": "Serie del billete ganador"
        },
        "calidad": "Datos históricos completos",
        "sensibilidad": "Datos públicos, no sensibles",
        "registros_totales": "976 sorteos",
        "años_cobertura": "18 años de historia"
    }


