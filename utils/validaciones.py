def validar_columnas(df, columnas_requeridas=None):
    """
    Valida que las columnas requeridas estén presentes en el DataFrame.
    
    Args:
        df: DataFrame a validar
        columnas_requeridas: Lista de columnas que deben estar presentes.
                           Si es None, usa las columnas por defecto.
    
    Returns:
        Lista de columnas faltantes
    """
    if columnas_requeridas is None:
        columnas_requeridas = ["fecha", "número", "serie", "sorteo"]
    
    faltantes = [c for c in columnas_requeridas if c not in df.columns]
    
    return faltantes
