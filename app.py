from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Dashboard climático de Puno",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

RUTA_BASE = Path(__file__).parent
RUTA_DATOS = (
    RUTA_BASE
    / "data"
    / "datos_limpios_clima_puno_2020_2025.csv"
)

# Agrega aquí a los demás integrantes
INTEGRANTES = "Jhon Alex Centeno Ccorimanya, Christian Aderly Ticona Marquez"

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(120, 120, 120, 0.25);
        border-radius: 12px;
        padding: 16px;
    }

    .encabezado {
        padding: 20px 24px;
        border-radius: 16px;
        background: linear-gradient(120deg, #0B4F6C, #187795);
        color: white;
        margin-bottom: 20px;
    }

    .encabezado h1 {
        margin: 0;
        color: white;
    }

    .encabezado p {
        margin: 8px 0 0;
        color: #E6F4F8;
    }

    .resultado {
        border-left: 5px solid #187795;
        padding: 12px 16px;
        background-color: rgba(24, 119, 149, 0.08);
        border-radius: 5px;
        margin-top: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CARGA DE DATOS
# =========================================================

@st.cache_data
def cargar_datos():
    datos = pd.read_csv(
        RUTA_DATOS,
        parse_dates=["fecha"]
    )
    return datos


df = cargar_datos()


# =========================================================
# VARIABLES DISPONIBLES
# =========================================================

VARIABLES = {
    "Temperatura media": "temperatura_media_c",
    "Temperatura máxima": "temperatura_maxima_c",
    "Temperatura mínima": "temperatura_minima_c",
    "Precipitación": "precipitacion_mm",
    "Humedad relativa": "humedad_relativa_pct",
    "Velocidad del viento": "velocidad_viento_ms",
    "Radiación solar": "radiacion_solar_kwh_m2"
}

UNIDADES = {
    "temperatura_media_c": "°C",
    "temperatura_maxima_c": "°C",
    "temperatura_minima_c": "°C",
    "precipitacion_mm": "mm",
    "humedad_relativa_pct": "%",
    "velocidad_viento_ms": "m/s",
    "radiacion_solar_kwh_m2": "kWh/m²/día"
}


# =========================================================
# FILTROS
# =========================================================

st.sidebar.title("🔎 Filtros de análisis")

rango_fechas = st.sidebar.date_input(
    "Rango de fechas",
    value=(
        df["fecha"].min().date(),
        df["fecha"].max().date()
    ),
    min_value=df["fecha"].min().date(),
    max_value=df["fecha"].max().date()
)

provincias_disponibles = sorted(df["provincia"].unique())

provincias = st.sidebar.multiselect(
    "Provincias",
    options=provincias_disponibles,
    default=provincias_disponibles
)

anios_disponibles = sorted(df["anio"].unique())

anios = st.sidebar.multiselect(
    "Años",
    options=anios_disponibles,
    default=anios_disponibles
)

orden_estaciones = [
    "Verano",
    "Otoño",
    "Invierno",
    "Primavera"
]

estaciones_disponibles = [
    estacion
    for estacion in orden_estaciones
    if estacion in df["estacion"].unique()
]

estaciones = st.sidebar.multiselect(
    "Estaciones climáticas",
    options=estaciones_disponibles,
    default=estaciones_disponibles
)

variable_seleccionada = st.sidebar.selectbox(
    "Variable para analizar",
    options=list(VARIABLES.keys())
)

variable = VARIABLES[variable_seleccionada]
unidad = UNIDADES[variable]

if not provincias or not anios or not estaciones:
    st.warning(
        "Selecciona al menos una provincia, un año y una estación."
    )
    st.stop()

if len(rango_fechas) == 2:
    fecha_inicio = pd.Timestamp(rango_fechas[0])
    fecha_fin = pd.Timestamp(rango_fechas[1])
else:
    fecha_inicio = df["fecha"].min()
    fecha_fin = df["fecha"].max()

df_filtrado = df[
    (df["fecha"] >= fecha_inicio)
    & (df["fecha"] <= fecha_fin)
    & (df["provincia"].isin(provincias))
    & (df["anio"].isin(anios))
    & (df["estacion"].isin(estaciones))
].copy()

if df_filtrado.empty:
    st.error("Los filtros seleccionados no devolvieron registros.")
    st.stop()

st.sidebar.divider()

st.sidebar.markdown(
    f"""
    **Registros seleccionados:** {len(df_filtrado):,}

    **Periodo:**  
    {fecha_inicio.strftime("%d/%m/%Y")} - 
    {fecha_fin.strftime("%d/%m/%Y")}
    """
)


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    f"""
    <div class="encabezado">
        <h1>🌦️ Dashboard climático de la región Puno</h1>
        <p>
            Análisis interactivo de las condiciones climáticas
            de las 13 provincias durante el periodo 2020-2025.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"Integrantes: {INTEGRANTES} · "
    f"Fuente: NASA POWER · "
    f"Actualización del dashboard: "
    f"{datetime.now().strftime('%d/%m/%Y')}"
)


# =========================================================
# KPI
# =========================================================

temperatura_media = df_filtrado["temperatura_media_c"].mean()
precipitacion_acumulada = df_filtrado["precipitacion_mm"].sum()
humedad_media = df_filtrado["humedad_relativa_pct"].mean()
registros_helada = (
    df_filtrado["dia_con_helada"] == "Sí"
).sum()
viento_maximo = df_filtrado["velocidad_viento_ms"].max()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric(
    "🌡️ Temperatura media",
    f"{temperatura_media:.2f} °C"
)

kpi2.metric(
    "🌧️ Precipitación acumulada",
    f"{precipitacion_acumulada:,.2f} mm"
)

kpi3.metric(
    "💧 Humedad media",
    f"{humedad_media:.2f} %"
)

kpi4.metric(
    "❄️ Registros con helada",
    f"{registros_helada:,}"
)

kpi5.metric(
    "💨 Viento máximo",
    f"{viento_maximo:.2f} m/s"
)


# =========================================================
# PESTAÑAS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vista general",
    "📈 Análisis descriptivo",
    "🔗 Relaciones",
    "🗺️ Mapa geográfico",
    "📝 Conclusiones"
])


# =========================================================
# TAB 1: VISTA GENERAL
# =========================================================

with tab1:

    st.subheader("Evolución y comparación climática")

    temperatura_mensual = (
        df_filtrado
        .assign(
            periodo=df_filtrado["fecha"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )
        .groupby(
            ["periodo", "provincia"],
            as_index=False
        )
        .agg(
            temperatura_media=(
                "temperatura_media_c",
                "mean"
            )
        )
    )

    fig_lineas = px.line(
        temperatura_mensual,
        x="periodo",
        y="temperatura_media",
        color="provincia",
        markers=True,
        title="Evolución mensual de la temperatura media",
        labels={
            "periodo": "Fecha",
            "temperatura_media": "Temperatura media (°C)",
            "provincia": "Provincia"
        }
    )

    fig_lineas.update_layout(
        template="plotly_white",
        hovermode="x unified",
        legend_title_text="Provincia"
    )

    st.plotly_chart(
        fig_lineas,
        use_container_width=True
    )

    precipitacion_provincia = (
        df_filtrado
        .groupby("provincia", as_index=False)
        .agg(
            precipitacion_acumulada=(
                "precipitacion_mm",
                "sum"
            )
        )
        .sort_values(
            "precipitacion_acumulada",
            ascending=True
        )
    )

    fig_barras = px.bar(
        precipitacion_provincia,
        x="precipitacion_acumulada",
        y="provincia",
        orientation="h",
        color="precipitacion_acumulada",
        color_continuous_scale="Blues",
        title="Precipitación acumulada por provincia",
        labels={
            "precipitacion_acumulada":
                "Precipitación acumulada (mm)",
            "provincia": "Provincia"
        }
    )

    fig_barras.update_layout(
        template="plotly_white",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_barras,
        use_container_width=True
    )

    provincia_lluviosa = precipitacion_provincia.iloc[-1]

    st.markdown(
        f"""
        <div class="resultado">
        <strong>Hallazgo:</strong>
        La provincia con mayor precipitación acumulada
        para los filtros seleccionados es
        <strong>{provincia_lluviosa["provincia"]}</strong>,
        con aproximadamente
        <strong>
        {provincia_lluviosa["precipitacion_acumulada"]:,.2f} mm
        </strong>.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TAB 2: ANÁLISIS DESCRIPTIVO
# =========================================================

with tab2:

    st.subheader("Distribución de variables climáticas")

    columna1, columna2 = st.columns(2)

    with columna1:

        fig_histograma = px.histogram(
            df_filtrado,
            x=variable,
            nbins=40,
            marginal="rug",
            title=f"Distribución: {variable_seleccionada}",
            labels={
                variable:
                    f"{variable_seleccionada} ({unidad})"
            },
            color_discrete_sequence=["#187795"]
        )

        fig_histograma.update_layout(
            template="plotly_white",
            showlegend=False
        )

        st.plotly_chart(
            fig_histograma,
            use_container_width=True
        )

    with columna2:

        fig_caja = px.box(
            df_filtrado,
            x="provincia",
            y="temperatura_minima_c",
            color="provincia",
            points="outliers",
            title="Temperaturas mínimas por provincia",
            labels={
                "provincia": "Provincia",
                "temperatura_minima_c":
                    "Temperatura mínima (°C)"
            }
        )

        fig_caja.add_hline(
            y=0,
            line_dash="dash",
            line_color="red",
            annotation_text="Umbral de helada"
        )

        fig_caja.update_layout(
            template="plotly_white",
            showlegend=False,
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig_caja,
            use_container_width=True
        )

    resumen_provincia = (
        df_filtrado
        .groupby("provincia", as_index=False)
        .agg(
            temperatura_media=(
                "temperatura_media_c",
                "mean"
            ),
            temperatura_minima=(
                "temperatura_minima_c",
                "min"
            ),
            temperatura_maxima=(
                "temperatura_maxima_c",
                "max"
            ),
            precipitacion_total=(
                "precipitacion_mm",
                "sum"
            ),
            humedad_media=(
                "humedad_relativa_pct",
                "mean"
            ),
            registros_helada=(
                "dia_con_helada",
                lambda x: (x == "Sí").sum()
            )
        )
    )

    resumen_provincia = resumen_provincia.round(2)

    st.subheader("Resumen estadístico por provincia")

    st.dataframe(
        resumen_provincia,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 3: RELACIONES Y CORRELACIÓN
# =========================================================

with tab3:

    st.subheader("Relaciones entre variables climáticas")

    relacion_mensual = (
        df_filtrado
        .assign(
            periodo=df_filtrado["fecha"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )
        .groupby(
            ["periodo", "provincia"],
            as_index=False
        )
        .agg(
            humedad_media=(
                "humedad_relativa_pct",
                "mean"
            ),
            precipitacion_media=(
                "precipitacion_mm",
                "mean"
            ),
            radiacion_media=(
                "radiacion_solar_kwh_m2",
                "mean"
            )
        )
    )

    fig_dispersion = px.scatter(
        relacion_mensual,
        x="humedad_media",
        y="precipitacion_media",
        color="provincia",
        size="radiacion_media",
        hover_data=["periodo"],
        title="Relación entre humedad y precipitación",
        labels={
            "humedad_media": "Humedad relativa (%)",
            "precipitacion_media":
                "Precipitación media (mm)",
            "radiacion_media":
                "Radiación solar",
            "provincia": "Provincia"
        }
    )

    fig_dispersion.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_dispersion,
        use_container_width=True
    )

    columnas_correlacion = [
        "temperatura_media_c",
        "temperatura_maxima_c",
        "temperatura_minima_c",
        "precipitacion_mm",
        "humedad_relativa_pct",
        "velocidad_viento_ms",
        "radiacion_solar_kwh_m2"
    ]

    nombres_cortos = {
        "temperatura_media_c": "Temp. media",
        "temperatura_maxima_c": "Temp. máxima",
        "temperatura_minima_c": "Temp. mínima",
        "precipitacion_mm": "Precipitación",
        "humedad_relativa_pct": "Humedad",
        "velocidad_viento_ms": "Viento",
        "radiacion_solar_kwh_m2": "Radiación"
    }

    columnas_validas = [
        columna
        for columna in columnas_correlacion
        if df_filtrado[columna].nunique() > 1
    ]

    if len(columnas_validas) >= 2:

        correlacion = (
            df_filtrado[columnas_validas]
            .corr()
            .rename(
                index=nombres_cortos,
                columns=nombres_cortos
            )
        )

        fig_calor = px.imshow(
            correlacion,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Mapa de calor de correlaciones"
        )

        fig_calor.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_calor,
            use_container_width=True
        )

    else:
        st.info(
            "Selecciona un periodo más amplio para calcular "
            "las correlaciones."
        )


# =========================================================
# TAB 4: MAPA GEOGRÁFICO
# =========================================================

with tab4:

    st.subheader("Distribución geográfica")

    mapa_provincias = (
        df_filtrado
        .groupby(
            [
                "provincia",
                "capital",
                "latitud",
                "longitud"
            ],
            as_index=False
        )
        .agg(
            temperatura_media=(
                "temperatura_media_c",
                "mean"
            ),
            precipitacion_media=(
                "precipitacion_mm",
                "mean"
            ),
            humedad_media=(
                "humedad_relativa_pct",
                "mean"
            ),
            registros_helada=(
                "dia_con_helada",
                lambda x: (x == "Sí").sum()
            )
        )
    )

    mapa_provincias["tamano"] = (
        mapa_provincias["precipitacion_media"]
        .clip(lower=0.15)
    )

    fig_mapa = px.scatter_geo(
        mapa_provincias,
        lat="latitud",
        lon="longitud",
        size="tamano",
        color="temperatura_media",
        hover_name="provincia",
        hover_data={
            "capital": True,
            "temperatura_media": ":.2f",
            "precipitacion_media": ":.2f",
            "humedad_media": ":.2f",
            "registros_helada": True,
            "tamano": False,
            "latitud": False,
            "longitud": False
        },
        color_continuous_scale="Turbo",
        size_max=35,
        projection="mercator",
        title=(
            "Distribución geográfica de las "
            "condiciones climáticas"
        )
    )

    fig_mapa.update_geos(
        lataxis_range=[-17.2, -13.5],
        lonaxis_range=[-71.2, -68.4],
        showland=True,
        landcolor="#F1F5F9",
        showocean=True,
        oceancolor="#DCEFFD",
        showlakes=True,
        lakecolor="#B9E3F5",
        showcountries=True,
        countrycolor="#475569",
        showsubunits=True,
        subunitcolor="#94A3B8",
        showcoastlines=True,
        coastlinecolor="#64748B"
    )

    fig_mapa.update_layout(
        template="plotly_white",
        height=650,
        margin={"r": 20, "t": 60, "l": 20, "b": 20},
        coloraxis_colorbar={
            "title": "Temperatura<br>media (°C)"
        }
    )

    st.plotly_chart(
        fig_mapa,
        use_container_width=True
    )

    st.info(
        "El color representa la temperatura media y el "
        "tamaño de los puntos representa la precipitación "
        "media de cada capital provincial."
    )


# =========================================================
# TAB 5: CONCLUSIONES Y DESCARGA
# =========================================================

with tab5:

    st.subheader("Hallazgos de los datos seleccionados")

    resumen_hallazgos = (
        df_filtrado
        .groupby("provincia", as_index=False)
        .agg(
            temperatura_media=(
                "temperatura_media_c",
                "mean"
            ),
            precipitacion_total=(
                "precipitacion_mm",
                "sum"
            ),
            heladas=(
                "dia_con_helada",
                lambda x: (x == "Sí").sum()
            )
        )
    )

    provincia_mas_lluviosa = resumen_hallazgos.loc[
        resumen_hallazgos["precipitacion_total"].idxmax()
    ]

    provincia_mas_fria = resumen_hallazgos.loc[
        resumen_hallazgos["temperatura_media"].idxmin()
    ]

    provincia_mas_heladas = resumen_hallazgos.loc[
        resumen_hallazgos["heladas"].idxmax()
    ]

    st.markdown(
        f"""
        1. La temperatura media de los registros seleccionados
        fue de **{temperatura_media:.2f} °C**.

        2. **{provincia_mas_lluviosa["provincia"]}** presentó
        la mayor precipitación acumulada, con
        **{provincia_mas_lluviosa["precipitacion_total"]:,.2f} mm**.

        3. **{provincia_mas_fria["provincia"]}** presentó la
        menor temperatura promedio, con
        **{provincia_mas_fria["temperatura_media"]:.2f} °C**.

        4. **{provincia_mas_heladas["provincia"]}** registró
        la mayor cantidad de observaciones con helada:
        **{int(provincia_mas_heladas["heladas"]):,}**.

        5. Los filtros permiten comprobar que las condiciones
        climáticas cambian según la provincia, el periodo y la
        estación del año.
        """
    )

    st.subheader("Recomendaciones")

    st.markdown(
        """
        - Priorizar medidas preventivas en provincias con mayor
          frecuencia de heladas.
        - Utilizar la información climática para planificar
          actividades agrícolas y ganaderas.
        - Contrastar los eventos extremos con información
          observada por SENAMHI.
        - Ampliar el periodo analizado para realizar estudios
          climáticos de largo plazo.
        """
    )

    st.subheader("Limitaciones")

    st.markdown(
        """
        Los datos de NASA POWER son estimaciones obtenidas mediante
        cuadrículas geográficas. Cada provincia está representada
        por las coordenadas de su capital, por lo que los resultados
        no describen necesariamente toda su extensión territorial.
        """
    )

    st.subheader("Descarga de información")

    csv_filtrado = df_filtrado.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Descargar datos filtrados en CSV",
        data=csv_filtrado,
        file_name="datos_climaticos_puno_filtrados.csv",
        mime="text/csv"
    )

    with st.expander("Ver datos filtrados"):

        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True
        )

    st.markdown(
        """
        **Fuente de datos:**  
        [NASA POWER – Prediction Of Worldwide Energy Resources]
        (https://power.larc.nasa.gov/)
        """
    )