import pandas as pd
import numpy as np
from scipy import stats

def resumen_dataset(df):
    """
    Retorna un resumen completo del dataset.
    """
    return {
        "Filas": df.shape[0],
        "Columnas": df.shape[1],
        "Nulos por columna": df.isnull().sum().to_dict(),
        "Tipos de datos": df.dtypes.astype(str).to_dict(),
        "Estadísticas numéricas": df.describe().to_dict()
    }

def analisis_outliers(df, columna):
    """
    Detecta outliers usando el método IQR (Rango Intercuartílico).
    
    Args:
        df: DataFrame
        columna: Nombre de la columna a analizar
    
    Returns:
        dict: Información sobre outliers
    """
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers = df[(df[columna] < limite_inferior) | (df[columna] > limite_superior)]
    
    return {
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "cantidad_outliers": len(outliers),
        "porcentaje_outliers": (len(outliers) / len(df)) * 100,
        "outliers": outliers.to_dict('records')
    }

def analisis_tendencias(df, columna_fecha, columna_valor):
    """
    Analiza tendencias temporales en los datos.
    
    Args:
        df: DataFrame
        columna_fecha: Nombre de la columna de fecha
        columna_valor: Nombre de la columna de valor
    
    Returns:
        dict: Información sobre tendencias
    """
    df_sorted = df.sort_values(columna_fecha)
    
    # Calcular promedio móvil
    df_sorted['promedio_movil_7'] = df_sorted[columna_valor].rolling(window=7, min_periods=1).mean()
    
    # Calcular tendencia lineal
    x = np.arange(len(df_sorted))
    y = df_sorted[columna_valor].values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    return {
        "tendencia": "creciente" if slope > 0 else "decreciente",
        "pendiente": slope,
        "r_cuadrado": r_value**2,
        "p_valor": p_value,
        "significativa": p_value < 0.05
    }

def estadisticas_por_grupo(df, columna_grupo, columna_valor):
    """
    Calcula estadísticas agrupadas.
    
    Args:
        df: DataFrame
        columna_grupo: Columna para agrupar
        columna_valor: Columna de valores a analizar
    
    Returns:
        DataFrame: Estadísticas por grupo
    """
    stats_grupo = df.groupby(columna_grupo)[columna_valor].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max')
    ]).round(2)
    
    return stats_grupo.reset_index()

def analisis_frecuencias(df, columna):
    """
    Analiza la frecuencia de valores en una columna.
    
    Args:
        df: DataFrame
        columna: Nombre de la columna
    
    Returns:
        DataFrame: Tabla de frecuencias
    """
    frecuencias = df[columna].value_counts().reset_index()
    frecuencias.columns = [columna, 'frecuencia']
    frecuencias['porcentaje'] = (frecuencias['frecuencia'] / len(df) * 100).round(2)
    
    return frecuencias

def detectar_valores_faltantes(df):
    """
    Analiza valores faltantes en el dataset.
    
    Returns:
        DataFrame: Información sobre valores faltantes
    """
    faltantes = pd.DataFrame({
        'columna': df.columns,
        'cantidad_faltantes': df.isnull().sum().values,
        'porcentaje_faltantes': (df.isnull().sum() / len(df) * 100).round(2).values
    })
    
    return faltantes[faltantes['cantidad_faltantes'] > 0]

def analisis_correlacion(df, umbral=0.5):
    """
    Encuentra correlaciones significativas entre variables numéricas.
    
    Args:
        df: DataFrame
        umbral: Umbral mínimo de correlación (absoluto)
    
    Returns:
        DataFrame: Pares de variables con correlación significativa
    """
    # Seleccionar solo columnas numéricas
    df_num = df.select_dtypes(include=[np.number])
    
    # Calcular matriz de correlación
    corr_matrix = df_num.corr()
    
    # Encontrar correlaciones significativas
    correlaciones = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) >= umbral:
                correlaciones.append({
                    'variable_1': corr_matrix.columns[i],
                    'variable_2': corr_matrix.columns[j],
                    'correlacion': round(corr_matrix.iloc[i, j], 3)
                })
    
    return pd.DataFrame(correlaciones)

