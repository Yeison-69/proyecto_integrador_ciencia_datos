def validar_columnas(df):
    columnas_requeridas = ["fecha", "número", "serie", "premio_mayor_millones", "ciudad"]
    faltantes = [c for c in columnas_requeridas if c not in df.columns]

    return faltantes
