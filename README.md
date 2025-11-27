# Proyecto Integrador de Ciencia de Datos - Lotería de Medellín

Análisis completo de 18 años de historia de sorteos de la Lotería de Medellín (2007-2025) con visualizaciones interactivas e inteligencia artificial.

## 🎯 Descripción

Este proyecto aplica metodologías de ciencia de datos (CRISP-DM) para analizar **976 sorteos** históricos, identificando patrones en números ganadores, series y tendencias temporales mediante:

- **Análisis Exploratorio de Datos (EDA)** exhaustivo
- **Visualizaciones Interactivas** con Plotly
- **Pruebas Estadísticas** de uniformidad, normalidad e independencia
- **Inteligencia Artificial** con Google Gemini para análisis asistido

## 📊 Dataset

- **Registros**: 976 sorteos
- **Periodo**: 2007-2025 (18 años)
- **Variables**: Fecha, Sorteo, Número (0-9999), Serie
- **Calidad**: 100% completitud, sin valores faltantes

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

```bash
cd proyecto_integrador_ciencia_datos
```

2. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

3. **Configurar API de Gemini (Opcional)**

Para usar la funcionalidad de IA, crea el archivo `.streamlit/secrets.toml`:

```toml
[gemini]
api_key = "TU_API_KEY_AQUI"
```

Obtén tu API key en: https://makersuite.google.com/app/apikey

4. **Ejecutar la aplicación**

```bash
streamlit run Inicio.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
proyecto_integrador_ciencia_datos/
├── Inicio.py                          # Página principal
├── pages/                             # Páginas de la aplicación
│   ├── 1_1 Definición del problema y objetivos.py
│   ├── 2_2 Recolección de datos.py
│   ├── 3_3 Exploración inicial y comprensión de los datos.py
│   ├── 4_4 Limpieza y preparación de datos.py
│   ├── 5_5 Evaluación e interpretación de resultados.py
│   ├── 6_6 Comunicación de resultados (Storytelling & Visualización).py
│   └── 7_7 Apliacación IA Generativa.py
├── utils/                             # Utilidades y funciones helper
│   ├── carga_datos.py                # Carga y procesamiento de datos
│   ├── graficos.py                   # Visualizaciones con Plotly
│   ├── eda_helpers.py                # Funciones de análisis exploratorio
│   ├── ai_helpers.py                 # Integración con Gemini
│   └── validaciones.py               # Validaciones de datos
├── data/                              # Datos del proyecto
│   └── premio_mayor_loteria_medellin.csv
├── .streamlit/                        # Configuración de Streamlit
│   ├── config.toml                   # Configuración general
│   └── secrets.toml.example          # Template para secrets
├── requirements.txt                   # Dependencias del proyecto
└── README.md                          # Este archivo
```

## 🎨 Características Principales

### 1. Análisis Exploratorio Completo
- Estadísticas descriptivas detalladas
- Distribuciones de números y series
- Análisis temporal (años, meses, días de semana)
- Detección de outliers
- Análisis de frecuencias

### 2. Visualizaciones Interactivas (15+)
- Distribución de números ganadores
- Evolución temporal de sorteos
- Frecuencia por día de semana
- Top números y series más frecuentes
- Mapas de calor mes-año
- Box plots por año
- Scatter plots número-serie
- Y más...

### 3. Pruebas Estadísticas
- Test Chi-cuadrado (uniformidad)
- Test Shapiro-Wilk (normalidad)
- Análisis de autocorrelación
- Pruebas de independencia

### 4. IA Generativa con Gemini
- **Q&A**: Pregunta sobre los datos y obtén respuestas contextuales
- **Insights Automáticos**: Generación de hallazgos clave
- **Reportes Narrativos**: Creación de reportes ejecutivos
- **Sugerencias**: Análisis adicionales recomendados
- **Explicaciones**: Interpretación de métricas complejas

### 5. Dashboard Interactivo
- Filtros por año, rango de números y series
- Visualizaciones dinámicas
- Exploración personalizada de datos

## 📖 Guía de Uso

### Navegación

La aplicación está organizada en 7 secciones siguiendo la metodología CRISP-DM:

1. **Definición del Problema**: Objetivos, KPIs y alcance
2. **Recolección de Datos**: Fuentes, metadata y calidad
3. **Exploración de Datos**: EDA con 5 tabs de análisis
4. **Limpieza y Preparación**: Validación y feature engineering
5. **Evaluación**: Métricas, pruebas estadísticas e insights
6. **Comunicación**: Storytelling y dashboard interactivo
7. **IA Generativa**: Asistente inteligente con Gemini

### Ejemplos de Uso

#### Explorar Distribución de Números
1. Ve a la página 3 (Exploración de Datos)
2. Selecciona el tab "Análisis de Números"
3. Interactúa con los gráficos (zoom, pan, hover)

#### Generar Insights con IA
1. Ve a la página 7 (IA Generativa)
2. Selecciona el tab "Insights Automáticos"
3. Haz clic en "Generar Insights"
4. Espera la respuesta de Gemini

#### Filtrar Datos en el Dashboard
1. Ve a la página 6 (Comunicación de Resultados)
2. Desplázate hasta "Dashboard Interactivo"
3. Usa los filtros de año, número y serie
4. Observa cómo cambian las visualizaciones

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación
- **Streamlit**: Framework para aplicaciones web
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manipulación de datos
- **NumPy**: Computación numérica
- **SciPy**: Análisis estadístico
- **Google Generative AI**: Integración con Gemini

## 📊 Hallazgos Principales

- **976 sorteos** analizados en 18 años
- **Distribución aproximadamente uniforme** de números
- **No se detectaron patrones predecibles** explotables
- **Pares e impares** aproximadamente 50-50
- **Independencia** entre sorteos consecutivos
- **Diversidad alta**: 60%+ del espacio de números utilizado

## ⚠️ Limitaciones

- Análisis descriptivo, no predictivo
- No incluye información de premios monetarios
- Los patrones históricos no garantizan resultados futuros
- La lotería es un juego de azar puro

## 🤝 Contribuciones

Este es un proyecto académico. Las sugerencias y mejoras son bienvenidas.

## 📄 Licencia

Proyecto educativo - Datos públicos de la Lotería de Medellín

## 👥 Autor

Proyecto Integrador de Ciencia de Datos

## 🔗 Enlaces Útiles

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Google Gemini API](https://ai.google.dev/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

**Nota Importante**: Este proyecto tiene fines educativos y estadísticos. La lotería es un juego de azar y ningún análisis puede predecir resultados futuros. Juega responsablemente.