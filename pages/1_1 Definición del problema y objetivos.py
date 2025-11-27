import streamlit as st

st.title("📌 1. Definición del Problema y Objetivos")

st.markdown("""
## 🎯 Contexto del Negocio

La Lotería de Medellín realiza sorteos semanales desde hace más de 18 años, generando una rica base de datos histórica 
con **976 sorteos** desde 2007 hasta 2025. Cada sorteo genera un número ganador (0-9999) y una serie específica.

Entender los patrones históricos puede proporcionar insights valiosos para:

- Análisis de frecuencias y distribuciones de números y series
- Identificación de tendencias temporales
- Comprensión de la aleatoriedad y patrones estadísticos
- Validación de la equidad del sistema de sorteos
- Generación de conocimiento basado en datos
""")

st.markdown("---")

st.markdown("""
## 🎯 Definición del Problema

**Planteamiento:**

> "Queremos **analizar 18 años de historia de sorteos de la Lotería de Medellín** (976 sorteos desde 2007 hasta 2025)
> para **identificar patrones estadísticos en números ganadores y series**, **analizar tendencias temporales** y
> **generar insights mediante visualizaciones interactivas e inteligencia artificial**."

### Preguntas de Investigación:

1. ¿Cuál es la distribución de números ganadores? ¿Es uniforme o hay sesgos?
2. ¿Existen números o series que aparecen con mayor frecuencia?
3. ¿Hay patrones temporales (por año, mes, día de semana)?
4. ¿Los primeros y últimos dígitos tienen distribución uniforme?
5. ¿Cuál es la evolución de la frecuencia de sorteos a lo largo del tiempo?
6. ¿Los números pares e impares tienen la misma probabilidad?
""")

st.markdown("---")

st.markdown("""
## 📏 KPIs (Indicadores Clave de Desempeño)

Los siguientes KPIs son **SMART** (Específicos, Medibles, Alcanzables, Relevantes, con Tiempo):

| KPI | Descripción | Umbral de Éxito |
|-----|-------------|-----------------|
| **Cobertura Temporal** | Años de datos analizados | 18+ años (2007-2025) |
| **Completitud de Datos** | % de registros válidos | >95% sin valores faltantes |
| **Uniformidad de Distribución** | Chi-cuadrado para números | p-value > 0.05 (distribución uniforme) |
| **Frecuencia de Sorteos** | Sorteos promedio por año | ~50-55 sorteos/año |
| **Diversidad de Números** | Números únicos ganadores | >500 números diferentes |
| **Diversidad de Series** | Series únicas ganadoras | >300 series diferentes |
""")

st.markdown("---")

st.markdown("""
## 👥 Stakeholders

### Principales Interesados:

1. **Equipo Académico**
   - Estudiantes y profesores
   - Decisión: Validar metodología y rigor estadístico

2. **Analistas de Datos**
   - Profesionales interesados en análisis de loterías
   - Decisión: Adoptar técnicas y visualizaciones

3. **Público General**
   - Jugadores y curiosos
   - Decisión: Entender mejor el funcionamiento histórico

### Criterios de Éxito:

- ✅ Análisis estadísticamente riguroso
- ✅ Visualizaciones claras e interactivas
- ✅ Insights basados en datos reales
- ✅ Código reproducible y documentado
- ✅ Transparencia en limitaciones
""")

st.markdown("---")

st.markdown("""
## 🎯 Alcance del Proyecto

### ✅ Qué SÍ incluye (In-Scope):

- Análisis de 976 sorteos históricos (2007-2025)
- Estadísticas descriptivas de números y series
- Análisis de frecuencias y distribuciones
- Visualizaciones interactivas con Plotly
- Análisis temporal (años, meses, días de semana)
- Identificación de patrones estadísticos
- Pruebas de uniformidad y aleatoriedad
- Asistente de IA para análisis y Q&A
- Dashboard interactivo completo

### ❌ Qué NO incluye (Out-of-Scope):

- **Predicción de números futuros ganadores**
- **Sistemas para "ganar" la lotería**
- Análisis de probabilidades individuales de ganar
- Recomendaciones de números para jugar
- Garantías o promesas de resultados
- Análisis de premios monetarios (no disponibles en el dataset)

### 📋 Supuestos:

- Los datos históricos son precisos y oficiales
- Los sorteos son aleatorios e independientes
- No hay cambios significativos en el mecanismo de sorteo
- Los datos son representativos del comportamiento general

### ⚠️ Restricciones:

- Datos limitados a números y series (no hay montos de premios)
- Análisis descriptivo, no predictivo
- No se puede garantizar la aleatoriedad perfecta
- Proyecto académico con fines educativos

### ⚖️ Consideraciones Éticas:

> **IMPORTANTE**: Este análisis es puramente estadístico y educativo. 
> La lotería es un juego de azar y ningún análisis histórico puede predecir resultados futuros.
> Juega responsablemente.
""")

st.markdown("---")

st.markdown("""
## ✅ Checklist de Completitud

- ✅ Problema definido claramente
- ✅ Preguntas de investigación identificadas
- ✅ KPIs SMART definidos con umbrales
- ✅ Stakeholders identificados
- ✅ Criterios de éxito establecidos
- ✅ Alcance (in/out) delimitado
- ✅ Supuestos y restricciones documentados
- ✅ Consideraciones éticas incluidas
""")

st.success("✅ Etapa 1 completada. Procede a la siguiente sección: Recolección de Datos.")
