import os
import pandas as pd

def cargar_datos_loteria():
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

    # Cargar CSV
    df = pd.read_csv(ruta)
    return df
