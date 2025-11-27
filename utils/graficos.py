import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def grafico_sorteos_tiempo(df):
    """
    Gráfico de línea mostrando la frecuencia de sorteos en el tiempo.
    """
    # Contar sorteos por mes
    sorteos_mes = df.groupby([df['fecha'].dt.to_period('M')]).size().reset_index()
    sorteos_mes.columns = ['mes', 'cantidad']
    sorteos_mes['mes'] = sorteos_mes['mes'].dt.to_timestamp()
    
    fig = px.line(
        sorteos_mes,
        x='mes',
        y='cantidad',
        title='Frecuencia de Sorteos por Mes',
        labels={'cantidad': 'Número de Sorteos', 'mes': 'Mes'},
        markers=True
    )
    
    fig.update_layout(height=500)
    return fig

def grafico_distribucion_numeros(df):
    """
    Histograma de la distribución de números ganadores.
    """
    fig = px.histogram(
        df,
        x='número',
        nbins=50,
        title='Distribución de Números Ganadores',
        labels={'número': 'Número Ganador', 'count': 'Frecuencia'},
        color_discrete_sequence=['#636EFA']
    )
    
    fig.update_layout(
        showlegend=False,
        height=500
    )
    
    return fig

def grafico_distribucion_series(df):
    """
    Histograma de la distribución de series.
    """
    fig = px.histogram(
        df,
        x='serie',
        nbins=50,
        title='Distribución de Series Ganadoras',
        labels={'serie': 'Serie', 'count': 'Frecuencia'},
        color_discrete_sequence=['#EF553B']
    )
    
    fig.update_layout(
        showlegend=False,
        height=500
    )
    
    return fig

def grafico_numeros_por_año(df):
    """
    Box plot de números ganadores por año.
    """
    fig = px.box(
        df,
        x='año',
        y='número',
        title='Distribución de Números Ganadores por Año',
        labels={'número': 'Número Ganador', 'año': 'Año'},
        color='año',
        points='all'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False
    )
    
    return fig

def grafico_series_por_año(df):
    """
    Box plot de series por año.
    """
    fig = px.box(
        df,
        x='año',
        y='serie',
        title='Distribución de Series por Año',
        labels={'serie': 'Serie', 'año': 'Año'},
        color='año',
        points='outliers'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False
    )
    
    return fig

def grafico_heatmap_mes_año(df):
    """
    Mapa de calor mostrando cantidad de sorteos por mes y año.
    """
    pivot_data = df.pivot_table(
        values='sorteo',
        index='año',
        columns='mes',
        aggfunc='count',
        fill_value=0
    )
    
    # Nombres de meses
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
             'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    fig = px.imshow(
        pivot_data,
        title='Cantidad de Sorteos por Mes y Año',
        labels=dict(x="Mes", y="Año", color="Sorteos"),
        color_continuous_scale='Blues',
        aspect='auto',
        x=[meses[i-1] for i in pivot_data.columns]
    )
    
    fig.update_layout(height=600)
    
    return fig

def grafico_frecuencia_digitos(df, posicion='primer'):
    """
    Gráfico de barras de frecuencia de dígitos.
    
    Args:
        df: DataFrame
        posicion: 'primer' o 'ultimo'
    """
    columna = 'primer_digito' if posicion == 'primer' else 'ultimo_digito'
    
    if columna not in df.columns:
        return None
    
    frecuencias = df[columna].value_counts().sort_index().reset_index()
    frecuencias.columns = ['digito', 'frecuencia']
    
    titulo = f'Frecuencia del {"Primer" if posicion == "primer" else "Último"} Dígito'
    
    fig = px.bar(
        frecuencias,
        x='digito',
        y='frecuencia',
        title=titulo,
        labels={'frecuencia': 'Frecuencia', 'digito': 'Dígito'},
        color='frecuencia',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=500, showlegend=False)
    
    return fig

def grafico_scatter_numero_serie(df):
    """
    Gráfico de dispersión entre número y serie.
    """
    # Tomar una muestra si hay muchos datos
    df_sample = df.sample(min(500, len(df)))
    
    fig = px.scatter(
        df_sample,
        x='número',
        y='serie',
        title='Relación entre Número y Serie',
        labels={'número': 'Número Ganador', 'serie': 'Serie'},
        color='año',
        hover_data={'fecha': True, 'sorteo': True},
        opacity=0.6
    )
    
    fig.update_layout(height=500)
    
    return fig

def grafico_tendencia_sorteos(df):
    """
    Gráfico de tendencia de sorteos acumulados en el tiempo.
    """
    df_sorted = df.sort_values('fecha').copy()
    df_sorted['sorteos_acumulados'] = range(1, len(df_sorted) + 1)
    
    fig = px.line(
        df_sorted,
        x='fecha',
        y='sorteos_acumulados',
        title='Sorteos Acumulados en el Tiempo',
        labels={'sorteos_acumulados': 'Sorteos Acumulados', 'fecha': 'Fecha'}
    )
    
    fig.update_layout(height=500)
    
    return fig

def grafico_numeros_pares_impares(df):
    """
    Gráfico de pie mostrando proporción de números pares vs impares.
    """
    if 'numero_par' not in df.columns:
        return None
    
    conteo = df['numero_par'].value_counts().reset_index()
    conteo.columns = ['tipo', 'cantidad']
    conteo['tipo'] = conteo['tipo'].map({1: 'Par', 0: 'Impar'})
    
    fig = px.pie(
        conteo,
        values='cantidad',
        names='tipo',
        title='Distribución de Números Pares vs Impares',
        color_discrete_sequence=['#00CC96', '#AB63FA']
    )
    
    fig.update_layout(height=500)
    
    return fig

def grafico_top_numeros(df, top_n=20):
    """
    Gráfico de los números más frecuentes.
    """
    top_numeros = df['número'].value_counts().head(top_n).reset_index()
    top_numeros.columns = ['número', 'frecuencia']
    
    fig = px.bar(
        top_numeros,
        x='número',
        y='frecuencia',
        title=f'Top {top_n} Números Más Frecuentes',
        labels={'frecuencia': 'Frecuencia', 'número': 'Número'},
        color='frecuencia',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=500, showlegend=False)
    
    return fig

def grafico_top_series(df, top_n=20):
    """
    Gráfico de las series más frecuentes.
    """
    top_series = df['serie'].value_counts().head(top_n).reset_index()
    top_series.columns = ['serie', 'frecuencia']
    
    fig = px.bar(
        top_series,
        x='serie',
        y='frecuencia',
        title=f'Top {top_n} Series Más Frecuentes',
        labels={'frecuencia': 'Frecuencia', 'serie': 'Serie'},
        color='frecuencia',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(height=500, showlegend=False)
    
    return fig

def grafico_sorteos_por_dia_semana(df):
    """
    Gráfico de barras de sorteos por día de la semana.
    """
    if 'dia_semana_nombre' not in df.columns:
        return None
    
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    conteo = df['dia_semana_nombre'].value_counts().reindex(dias_orden, fill_value=0).reset_index()
    conteo.columns = ['dia', 'cantidad']
    conteo['dia'] = dias_es
    
    fig = px.bar(
        conteo,
        x='dia',
        y='cantidad',
        title='Sorteos por Día de la Semana',
        labels={'cantidad': 'Cantidad de Sorteos', 'dia': 'Día'},
        color='cantidad',
        color_continuous_scale='Sunset'
    )
    
    fig.update_layout(height=500, showlegend=False)
    
    return fig

def grafico_evolucion_por_año(df):
    """
    Gráfico de líneas mostrando evolución de sorteos por año.
    """
    sorteos_año = df.groupby('año').size().reset_index()
    sorteos_año.columns = ['año', 'cantidad']
    
    fig = px.line(
        sorteos_año,
        x='año',
        y='cantidad',
        title='Evolución de Sorteos por Año',
        labels={'cantidad': 'Cantidad de Sorteos', 'año': 'Año'},
        markers=True
    )
    
    # Agregar línea de promedio
    promedio = sorteos_año['cantidad'].mean()
    fig.add_hline(
        y=promedio,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Promedio: {promedio:.1f}",
        annotation_position="right"
    )
    
    fig.update_layout(height=500)
    
    return fig
