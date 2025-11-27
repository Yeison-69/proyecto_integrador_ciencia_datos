import streamlit as st
import google.generativeai as genai
import pandas as pd

def inicializar_gemini():
    """
    Inicializa el cliente de Gemini API usando la clave de secrets.
    
    Returns:
        genai.GenerativeModel: Modelo configurado o None si falla
    """
    try:
        # Obtener API key de secrets
        api_key = st.secrets.get("gemini", {}).get("api_key")
        
        if not api_key:
            st.error("⚠️ No se encontró la API key de Gemini en secrets.toml")
            st.info("Configura tu API key en `.streamlit/secrets.toml`")
            return None
        
        # Configurar Gemini
        genai.configure(api_key=api_key)
        
        # Crear modelo
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        return model
    
    except Exception as e:
        st.error(f"Error al inicializar Gemini: {e}")
        return None

def generar_prompt_contexto(df, pregunta_usuario):
    """
    Genera un prompt con contexto del dataset para Gemini.
    
    Args:
        df: DataFrame con los datos
        pregunta_usuario: Pregunta del usuario
    
    Returns:
        str: Prompt completo con contexto
    """
    # Resumen del dataset
    resumen = f"""
Contexto del Dataset - Lotería de Medellín:
- Total de registros: {len(df)}
- Periodo: {df['fecha'].min()} a {df['fecha'].max()}
- Ciudades: {', '.join(df['ciudad'].unique())}
- Premio promedio: {df['premio_mayor_millones'].mean():.2f} millones
- Premio mínimo: {df['premio_mayor_millones'].min()} millones
- Premio máximo: {df['premio_mayor_millones'].max()} millones

Columnas disponibles:
- fecha: Fecha del sorteo
- número: Número ganador (4 dígitos)
- serie: Serie del billete
- premio_mayor_millones: Monto del premio en millones
- ciudad: Ciudad donde se vendió el billete ganador

Primeras filas del dataset:
{df.head(3).to_string()}

Pregunta del usuario: {pregunta_usuario}

Por favor, responde de manera clara y concisa, usando los datos proporcionados.
"""
    
    return resumen

def obtener_insights(model, df):
    """
    Genera insights automáticos sobre el dataset.
    
    Args:
        model: Modelo de Gemini
        df: DataFrame
    
    Returns:
        str: Insights generados
    """
    if model is None:
        return "No se pudo generar insights. Verifica la configuración de Gemini."
    
    prompt = f"""
Analiza el siguiente dataset de la Lotería de Medellín y genera 5 insights clave:

Estadísticas:
- Total sorteos: {len(df)}
- Periodo: {df['fecha'].min()} a {df['fecha'].max()}
- Premio promedio: {df['premio_mayor_millones'].mean():.2f} millones
- Desviación estándar: {df['premio_mayor_millones'].std():.2f} millones
- Ciudad con más premios: {df['ciudad'].mode()[0]} ({df[df['ciudad'] == df['ciudad'].mode()[0]].shape[0]} premios)

Distribución por ciudad:
{df.groupby('ciudad')['premio_mayor_millones'].agg(['count', 'mean']).to_string()}

Genera insights accionables y relevantes en formato de lista numerada.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar insights: {e}"

def responder_pregunta(model, df, pregunta):
    """
    Responde preguntas sobre el dataset usando Gemini.
    
    Args:
        model: Modelo de Gemini
        df: DataFrame
        pregunta: Pregunta del usuario
    
    Returns:
        str: Respuesta generada
    """
    if model is None:
        return "No se pudo procesar la pregunta. Verifica la configuración de Gemini."
    
    prompt = generar_prompt_contexto(df, pregunta)
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al procesar la pregunta: {e}"

def generar_reporte_narrativo(model, df):
    """
    Genera un reporte narrativo completo del análisis.
    
    Args:
        model: Modelo de Gemini
        df: DataFrame
    
    Returns:
        str: Reporte en formato narrativo
    """
    if model is None:
        return "No se pudo generar el reporte. Verifica la configuración de Gemini."
    
    prompt = f"""
Crea un reporte ejecutivo narrativo sobre el análisis de la Lotería de Medellín.

Datos clave:
- Periodo analizado: {df['fecha'].min()} a {df['fecha'].max()}
- Total de sorteos: {len(df)}
- Premio promedio: {df['premio_mayor_millones'].mean():.2f} millones
- Rango de premios: {df['premio_mayor_millones'].min()} - {df['premio_mayor_millones'].max()} millones

Distribución por ciudad (top 5):
{df['ciudad'].value_counts().head(5).to_string()}

El reporte debe incluir:
1. Resumen ejecutivo
2. Hallazgos principales
3. Patrones identificados
4. Recomendaciones

Usa un tono profesional y conciso.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar reporte: {e}"

def sugerir_analisis(model, df):
    """
    Sugiere análisis adicionales basados en los datos.
    
    Args:
        model: Modelo de Gemini
        df: DataFrame
    
    Returns:
        str: Sugerencias de análisis
    """
    if model is None:
        return "No se pudieron generar sugerencias. Verifica la configuración de Gemini."
    
    prompt = f"""
Basándote en este dataset de lotería con las siguientes características:
- {len(df)} registros
- Columnas: fecha, número, serie, premio_mayor_millones, ciudad
- Periodo: {df['fecha'].min()} a {df['fecha'].max()}

Sugiere 5 análisis adicionales que podrían ser valiosos para entender mejor los datos.
Sé específico sobre qué analizar y por qué sería útil.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar sugerencias: {e}"

def explicar_metrica(model, metrica_nombre, metrica_valor, contexto=""):
    """
    Explica una métrica en términos simples.
    
    Args:
        model: Modelo de Gemini
        metrica_nombre: Nombre de la métrica
        metrica_valor: Valor de la métrica
        contexto: Contexto adicional
    
    Returns:
        str: Explicación de la métrica
    """
    if model is None:
        return "No se pudo explicar la métrica. Verifica la configuración de Gemini."
    
    prompt = f"""
Explica en términos simples y claros qué significa la siguiente métrica:

Métrica: {metrica_nombre}
Valor: {metrica_valor}
Contexto: {contexto}

Proporciona:
1. Qué mide esta métrica
2. Cómo interpretar el valor
3. Qué implica para el negocio/análisis
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al explicar métrica: {e}"
