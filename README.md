# Dashboard climático de la región Puno

Dashboard interactivo para el análisis de las condiciones climáticas en las provincias de la región Puno durante el periodo 2020-2025.

## Descripción

La región Puno presenta condiciones climáticas variables debido a su ubicación geográfica, altitud y diversidad territorial. Las bajas temperaturas, heladas y precipitaciones pueden afectar las actividades agrícolas, ganaderas y sociales.

Este proyecto transforma datos climáticos diarios en indicadores y visualizaciones interactivas que permiten identificar patrones, comparar provincias y analizar eventos relevantes.

## Integrantes

- Jhon Alex Centeno Ccorimanya
- Christian Aderly Ticona Marquez

## Fuente de datos

Los datos fueron obtenidos mediante la API de NASA POWER:

https://power.larc.nasa.gov/

Periodo analizado: 2020-2025.

Los registros representan las condiciones climáticas estimadas para las coordenadas de las capitales de las 13 provincias de la región Puno.

## Variables analizadas

- Temperatura media.
- Temperatura máxima.
- Temperatura mínima.
- Precipitación.
- Humedad relativa.
- Velocidad del viento.
- Radiación solar.
- Amplitud térmica.
- Presencia de heladas.
- Provincia, capital, fecha y estación climática.

## Funcionalidades

- Indicadores climáticos dinámicos.
- Filtro por rango de fechas.
- Filtro por provincia.
- Filtro por año.
- Filtro por estación climática.
- Selector de variable.
- Gráfico de líneas.
- Gráfico de barras.
- Histograma.
- Diagrama de caja.
- Gráfico de dispersión.
- Mapa de calor de correlaciones.
- Mapa geográfico interactivo.
- Interpretación de resultados.
- Descarga de datos filtrados en CSV.

## Tecnologías

- Python.
- Pandas.
- Plotly.
- Streamlit.
- NumPy.

## Estructura del proyecto

```text
dashboard-visualizacion/
├── app.py
├── data/
│   ├── datos_originales_nasa_power.csv
│   └── datos_limpios_clima_puno_2020_2025.csv
├── notebooks/
│   └── procesamiento.ipynb
├── pages/
├── assets/
├── informe/
├── requirements.txt
└── README.md