import pandas as pd

def resumen_dataset(df):
    return {
        "Filas": df.shape[0],
        "Columnas": df.shape[1],
        "Nulos por columna": df.isnull().sum().to_dict(),
        "Tipos de datos": df.dtypes.astype(str).to_dict(),
        "Estadísticas numéricas": df.describe().to_dict()
    }
