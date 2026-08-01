# Dashboard climático de la región Puno

Dashboard interactivo para el análisis de las condiciones climáticas de las provincias de la región Puno durante el periodo 2020-2025.

## Descripción

La región Puno presenta condiciones climáticas variables debido a su ubicación geográfica, altitud y diversidad territorial. Las bajas temperaturas, las heladas y las precipitaciones pueden afectar las actividades agrícolas, ganaderas y sociales.

Este proyecto transforma datos climáticos diarios en indicadores y visualizaciones interactivas que permiten identificar patrones, comparar provincias y analizar eventos relevantes.

## Integrantes

- Jhon Alex Centeno Ccorimanya.
- Christian Aderly Ticona Marquez.

## Fuente de datos

Los datos fueron obtenidos mediante la API de [NASA POWER](https://power.larc.nasa.gov/).

- Periodo analizado: 2020-2025.
- Cobertura territorial: capitales de las 13 provincias de la región Puno.
- Frecuencia de los registros: diaria.

## Variables analizadas

- Temperatura media, máxima y mínima.
- Precipitación.
- Humedad relativa.
- Velocidad del viento.
- Radiación solar.
- Amplitud térmica.
- Presencia de heladas.
- Provincia, capital, fecha y estación climática.

## Funcionalidades

- Indicadores climáticos dinámicos.
- Filtros globales por rango de fechas, provincia y estación climática.
- Selector local de la variable mostrada en el histograma.
- Gráficos de líneas, barras, distribución, caja y dispersión.
- Mapa de calor de correlaciones.
- Mapa geográfico interactivo.
- Comparación de indicadores entre provincias.
- Interpretaciones automáticas de los resultados.
- Descarga de datos filtrados en formato CSV.
- Diseño adaptable a los temas claro y oscuro de Streamlit.

## Tecnologías utilizadas

- Python.
- Pandas.
- Plotly.
- Streamlit.
- NumPy.

## Estructura del proyecto

```text
dashboard-visualizacion/
├── .gitignore
├── app.py
├── data/
│   ├── datos_originales_nasa_power.csv
│   └── datos_limpios_clima_puno_2020_2025.csv
├── notebooks/
│   └── procesamiento.ipynb
├── requirements.txt
└── README.md
```

## Requisitos previos

Antes de ejecutar el proyecto, se necesita:

- Python 3.11 o una versión posterior.
- Git, si se desea clonar el repositorio.
- Una conexión a Internet durante la instalación de las dependencias.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Alexpiper28/dashboard_climatico_puno.git
cd dashboard_climatico_puno
```

También se puede descargar el repositorio como archivo ZIP desde GitHub y extraerlo en una carpeta.

### 2. Crear un entorno virtual

En Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Cuando el entorno esté activo, la terminal mostrará `(.venv)` al inicio de la línea.

### 3. Instalar las dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Ejecutar el dashboard

```bash
python -m streamlit run app.py
```

El dashboard se abrirá automáticamente en el navegador. Si no ocurre, ingresar a:

```text
http://localhost:8501
```

Para detener la aplicación, presionar `Ctrl + C` en la terminal.

## Solución de problemas frecuentes

### El comando `streamlit` no se reconoce

Ejecutar Streamlit mediante Python:

```bash
python -m streamlit run app.py
```

Esta forma no requiere agregar `streamlit.exe` al PATH de Windows.

### El comando `source` no se reconoce

`source` solamente funciona en Git Bash. Si se utiliza CMD, activar el entorno con:

```cmd
.venv\Scripts\activate
```

Si la terminal ya muestra `(.venv)`, el entorno se encuentra activo y no es necesario activarlo nuevamente.

### No se encuentra el archivo de datos

Comprobar que el siguiente archivo exista y conserve exactamente esta ubicación:

```text
data/datos_limpios_clima_puno_2020_2025.csv
```

## Uso del dashboard

1. Seleccionar el periodo, las provincias y las estaciones climáticas desde la barra lateral.
2. Consultar los principales indicadores en la vista de resumen ejecutivo.
3. Abrir **Análisis detallado** para explorar distribuciones, relaciones y valores atípicos.
4. Utilizar **Variable del histograma** para cambiar únicamente la distribución mostrada en esa sección.
5. Abrir **Mapa y territorio** para comparar geográficamente las provincias.
6. Descargar los registros filtrados desde la sección de datos y metodología.

## Principales hallazgos

- Se analizaron 28 496 registros climáticos correspondientes a las 13 provincias de Puno.
- La temperatura media regional fue de 8.23 °C.
- San Román presentó la mayor temperatura media, con 9.83 °C.
- Carabaya registró la menor temperatura media, con 4.96 °C, y la mayor precipitación acumulada, con 7 650.23 mm.
- Se identificaron 5 811 registros con helada, equivalentes al 20.4 % del dataset.
- Lampa presentó la mayor frecuencia de heladas, con 1 172 registros.
- El año 2024 presentó la mayor temperatura media anual, mientras que 2023 registró la mayor precipitación diaria promedio.

## Enlaces del proyecto

- Dashboard publicado: https://dashboard-climatico-puno.streamlit.app/

- Repositorio: https://github.com/Alexpiper28/dashboard_climatico_puno

## Licencia y uso académico

Proyecto desarrollado con fines académicos para el curso de Visualización de Datos de la Universidad Nacional del Altiplano.
