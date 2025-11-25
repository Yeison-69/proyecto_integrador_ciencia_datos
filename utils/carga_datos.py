import pandas as pd
import os

def cargar_datos_limpios():
    """
    Carga el archivo datos_limpios.csv desde la carpeta data/
    """
    ruta = os.path.join("data", "datos_limpios.csv")

    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo en: {ruta}")

    df = pd.read_csv(ruta)
    return df
