from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


# =========================================================
# CONFIGURACION GENERAL
# =========================================================

st.set_page_config(
    page_title="Clima Puno | Panel ejecutivo",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "datos_limpios_clima_puno_2020_2025.csv"

INTEGRANTES = "Jhon Alex Centeno Ccorimanya · Christian Aderly Ticona Marquez"
FUENTE_URL = "https://power.larc.nasa.gov/"

VARIABLES = {
    "Temperatura media": "temperatura_media_c",
    "Temperatura maxima": "temperatura_maxima_c",
    "Temperatura minima": "temperatura_minima_c",
    "Precipitacion": "precipitacion_mm",
    "Humedad relativa": "humedad_relativa_pct",
    "Velocidad del viento": "velocidad_viento_ms",
    "Radiacion solar": "radiacion_solar_kwh_m2",
}

UNIDADES = {
    "temperatura_media_c": "°C",
    "temperatura_maxima_c": "°C",
    "temperatura_minima_c": "°C",
    "precipitacion_mm": "mm",
    "humedad_relativa_pct": "%",
    "velocidad_viento_ms": "m/s",
    "radiacion_solar_kwh_m2": "kWh/m²/dia",
}

MESES = {
    1: "Ene",
    2: "Feb",
    3: "Mar",
    4: "Abr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dic",
}

COLORES = {
    "azul": "#1677FF",
    "celeste": "#28B8D5",
    "verde": "#15A36D",
    "amarillo": "#F5A524",
    "rojo": "#E5484D",
    "morado": "#7C5CFC",
    "tinta": "#172B4D",
    "gris": "#64748B",
}

# Iconos vectoriales de estilo Lucide. Se incluyen como SVG para evitar
# dependencias externas y mantener nitidez en cualquier resolucion.
ICONOS_SECCION = {
    "indicadores": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="m13 2-9 12h7l-1 8 10-13h-7z"/>
        </svg>
    """,
    "lideres": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M8 21h8"/><path d="M12 17v4"/>
            <path d="M7 4h10v4a5 5 0 0 1-10 0z"/>
            <path d="M7 6H4v1a4 4 0 0 0 4 4"/>
            <path d="M17 6h3v1a4 4 0 0 1-4 4"/>
        </svg>
    """,
    "resumen": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 19V9"/><path d="M10 19V5"/>
            <path d="M16 19v-7"/><path d="M22 19V3"/>
            <path d="M2 21h20"/>
        </svg>
    """,
    "analisis": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="11" cy="11" r="7"/>
            <path d="m20 20-4-4"/><path d="M8 12l2-2 2 2 3-4"/>
        </svg>
    """,
    "mapa": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3z"/>
            <path d="M9 3v15"/><path d="M15 6v15"/>
        </svg>
    """,
    "datos": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 3v12"/><path d="m7 10 5 5 5-5"/>
            <path d="M5 21h14a2 2 0 0 0 2-2v-3"/>
            <path d="M3 16v3a2 2 0 0 0 2 2"/>
        </svg>
    """,
}


# =========================================================
# ESTILO VISUAL
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --azul: #1677FF;
        --azul-oscuro: #123B69;
        --celeste: #28B8D5;
        --tinta: #172B4D;
        --gris: #64748B;
        --borde: rgba(100, 116, 139, 0.20);
    }

    .block-container {
        max-width: 1580px;
        padding-top: 1.15rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid var(--borde);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.3rem;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px;
        margin: 0 0 14px;
        border-radius: 16px;
        color: white;
        background: linear-gradient(135deg, #0B3C6F, #1677FF 62%, #28B8D5);
        box-shadow: 0 10px 24px rgba(22,119,255,.20);
    }

    .sidebar-brand-icon {
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        border-radius: 13px;
        background: rgba(255,255,255,.16);
        border: 1px solid rgba(255,255,255,.25);
    }

    .sidebar-brand-icon svg {
        width: 23px;
        height: 23px;
        stroke: white;
    }

    .sidebar-brand-title {
        font-size: 1rem;
        font-weight: 850;
        line-height: 1.15;
    }

    .sidebar-brand-subtitle {
        margin-top: 3px;
        color: rgba(255,255,255,.78);
        font-size: .72rem;
    }

    .filter-heading {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 4px 0 10px;
        color: inherit;
        font-size: .84rem;
        font-weight: 800;
        letter-spacing: .04em;
        text-transform: uppercase;
    }

    .filter-heading svg {
        width: 17px;
        height: 17px;
        stroke: var(--primary-color);
    }

    .filter-scope {
        margin: -2px 0 14px;
        padding: 10px 11px;
        border: 1px solid color-mix(in srgb, var(--primary-color) 24%, transparent);
        border-radius: 11px;
        color: var(--text-color);
        background: color-mix(
            in srgb,
            var(--secondary-background-color) 86%,
            var(--primary-color) 14%
        );
        font-size: .72rem;
        line-height: 1.4;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="input"] > div,
    [data-testid="stSidebar"] [data-testid="stDateInput"] input {
        border-radius: 12px !important;
        border-color: color-mix(in srgb, var(--text-color) 18%, transparent) !important;
        color: var(--text-color) !important;
        background: var(--secondary-background-color) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] {
        border-radius: 8px !important;
        border: 1px solid color-mix(in srgb, var(--primary-color) 42%, transparent) !important;
        color: var(--text-color) !important;
        background: var(--secondary-background-color) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] span,
    [data-testid="stSidebar"] [data-baseweb="tag"] svg {
        color: var(--text-color) !important;
        fill: var(--text-color) !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: var(--text-color);
    }

    [data-testid="stSidebar"] .stButton > button {
        min-height: 42px;
        border-radius: 12px;
        border: 1px solid rgba(22,119,255,.30);
        color: #1677FF;
        font-weight: 760;
        background: rgba(22,119,255,.07);
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        color: white;
        border-color: #1677FF;
        background: #1677FF;
    }

    .filter-summary {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-top: 8px;
    }

    .filter-summary-item {
        padding: 10px;
        border: 1px solid color-mix(in srgb, var(--text-color) 16%, transparent);
        border-radius: 11px;
        color: var(--text-color);
        background: var(--secondary-background-color);
    }

    .filter-summary-label {
        color: var(--gris);
        font-size: .65rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: .04em;
    }

    .filter-summary-value {
        margin-top: 2px;
        font-size: .88rem;
        font-weight: 800;
        color: var(--text-color);
    }

    .local-control-note {
        min-height: 68px;
        margin-top: 27px;
        padding: 11px 14px;
        display: flex;
        align-items: center;
        border: 1px solid color-mix(in srgb, var(--primary-color) 25%, transparent);
        border-radius: 12px;
        color: var(--text-color);
        background: color-mix(
            in srgb,
            var(--secondary-background-color) 90%,
            var(--primary-color) 10%
        );
        font-size: .78rem;
        line-height: 1.45;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 25px 30px;
        border-radius: 22px;
        color: white;
        background:
            radial-gradient(circle at 90% 15%, rgba(255,255,255,.24), transparent 23%),
            linear-gradient(125deg, #0B3C6F 0%, #1261A0 48%, #19A7CE 100%);
        box-shadow: 0 14px 34px rgba(10, 65, 120, 0.20);
        margin-bottom: 14px;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        border: 38px solid rgba(255,255,255,.10);
        border-radius: 50%;
        right: -85px;
        bottom: -135px;
    }

    .hero-kicker {
        display: inline-block;
        padding: 5px 11px;
        border-radius: 999px;
        background: rgba(255,255,255,.16);
        font-size: .76rem;
        font-weight: 750;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .hero h1 {
        color: white !important;
        margin: 0;
        font-size: clamp(1.7rem, 3vw, 2.65rem);
        letter-spacing: -.035em;
    }

    .hero p {
        color: #E8F7FF;
        margin: 8px 0 0;
        max-width: 850px;
        font-size: 1rem;
    }

    .meta-line {
        display: flex;
        flex-wrap: wrap;
        gap: 8px 18px;
        color: var(--gris);
        font-size: .83rem;
        margin: 0 2px 18px;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: 12px;
        width: 100%;
        min-width: 0;
        padding: 11px 14px;
        margin: 10px 0 16px;
        border: 1px solid rgba(22,119,255,.15);
        border-radius: 15px;
        background: linear-gradient(90deg, rgba(22,119,255,.10), rgba(40,184,213,.035));
        box-shadow: inset 4px 0 0 #1677FF;
    }

    .section-icon {
        display: grid;
        place-items: center;
        width: 39px;
        height: 39px;
        flex: 0 0 39px;
        border: 1px solid rgba(22,119,255,.17);
        border-radius: 12px;
        color: #1677FF;
        background: rgba(255,255,255,.82);
        box-shadow: 0 5px 13px rgba(22,119,255,.11);
    }

    .section-icon svg {
        width: 21px;
        height: 21px;
        stroke: currentColor;
        stroke-width: 2;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .section-heading {
        color: inherit;
        font-size: 1.13rem;
        font-weight: 830;
        letter-spacing: -.02em;
        line-height: 1.25;
        white-space: nowrap;
        word-break: normal;
        overflow-wrap: normal;
        min-width: 0;
    }

    .kpi-card {
        position: relative;
        min-height: 154px;
        padding: 18px;
        border: 1px solid var(--borde);
        border-radius: 18px;
        background: linear-gradient(155deg, rgba(255,255,255,.10), rgba(100,116,139,.045));
        box-shadow: 0 8px 24px rgba(15, 23, 42, .07);
        overflow: hidden;
    }

    .kpi-card::after {
        content: "";
        position: absolute;
        width: 68px;
        height: 68px;
        border-radius: 50%;
        right: -24px;
        top: -24px;
        background: var(--accent-soft);
    }

    .kpi-icon {
        display: grid;
        place-items: center;
        width: 43px;
        height: 43px;
        border-radius: 13px;
        background: var(--accent-soft);
        font-size: 1.42rem;
        margin-bottom: 12px;
    }

    .kpi-label {
        color: var(--gris);
        font-size: .78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .04em;
    }

    .kpi-value {
        color: inherit;
        font-size: clamp(1.35rem, 2vw, 1.85rem);
        line-height: 1.15;
        font-weight: 800;
        margin-top: 3px;
        letter-spacing: -.03em;
    }

    .kpi-note {
        color: var(--gris);
        font-size: .76rem;
        margin-top: 6px;
    }

    .leader-card {
        min-height: 142px;
        border-radius: 18px;
        padding: 17px 18px;
        color: white;
        background: var(--leader-bg);
        box-shadow: 0 10px 24px rgba(15,23,42,.12);
    }

    .leader-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
    }

    .leader-icon {
        font-size: 2rem;
        filter: drop-shadow(0 3px 7px rgba(0,0,0,.14));
    }

    .leader-tag {
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .07em;
        text-transform: uppercase;
        opacity: .85;
    }

    .leader-name {
        font-size: 1.18rem;
        font-weight: 800;
        margin-top: 13px;
        line-height: 1.12;
    }

    .leader-value {
        font-size: .84rem;
        margin-top: 5px;
        opacity: .88;
    }

    .insight-box {
        border: 1px solid rgba(22,119,255,.20);
        border-left: 5px solid #1677FF;
        background: rgba(22,119,255,.07);
        border-radius: 14px;
        padding: 15px 17px;
        margin: 8px 0 16px;
        line-height: 1.55;
    }

    .risk-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        color: white;
        background: var(--risk-color);
        font-size: .74rem;
        font-weight: 800;
        letter-spacing: .03em;
    }

    .chart-note {
        min-height: 58px;
        padding: 10px 13px;
        border-radius: 11px;
        background: rgba(100,116,139,.08);
        color: var(--gris);
        font-size: .80rem;
        line-height: 1.45;
        margin-top: -8px;
        margin-bottom: 12px;
    }

    .method-card {
        border: 1px solid var(--borde);
        border-radius: 16px;
        padding: 17px;
        min-height: 150px;
        background: rgba(100,116,139,.045);
    }

    .method-card strong {
        display: block;
        margin-bottom: 7px;
        font-size: 1rem;
    }

    .small-muted {
        color: var(--gris);
        font-size: .80rem;
    }

    div[data-testid="stPlotlyChart"] {
        border: 1px solid var(--borde);
        border-radius: 17px;
        overflow: hidden;
        box-shadow: 0 7px 20px rgba(15,23,42,.055);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        padding: 5px;
        border-radius: 13px;
        background: rgba(100,116,139,.08);
    }

    .stTabs [data-baseweb="tab"] {
        height: 43px;
        border-radius: 10px;
        padding: 0 17px;
        font-weight: 700;
    }

    @media (max-width: 900px) {
        .hero { padding: 21px; }
        .kpi-card, .leader-card { min-height: auto; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================


@st.cache_data
def cargar_datos(path: Path) -> pd.DataFrame:
    datos = pd.read_csv(path, parse_dates=["fecha"])
    datos["anio"] = datos["anio"].astype(int)
    return datos


def formato_numero(valor: float, decimales: int = 1) -> str:
    return f"{valor:,.{decimales}f}"


def kpi_card(icono: str, titulo: str, valor: str, nota: str, color: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent-soft:{color}22;">
            <div class="kpi-icon">{icono}</div>
            <div class="kpi-label">{titulo}</div>
            <div class="kpi-value">{valor}</div>
            <div class="kpi-note">{nota}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def leader_card(icono: str, etiqueta: str, nombre: str, valor: str, fondo: str) -> None:
    st.markdown(
        f"""
        <div class="leader-card" style="--leader-bg:{fondo};">
            <div class="leader-top">
                <span class="leader-tag">{etiqueta}</span>
                <span class="leader-icon">{icono}</span>
            </div>
            <div class="leader-name">{nombre}</div>
            <div class="leader-value">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def titulo_seccion(icono: str, titulo: str) -> None:
    icono_svg = ICONOS_SECCION[icono]
    st.markdown(
        f"""
        <div class="section-title">
            <div class="section-icon">{icono_svg}</div>
            <div class="section-heading">{titulo}</div>
        </div>
        """,
        unsafe_allow_html=True,
        width="stretch",
    )


def estilo_figura(fig, altura: int = 360, leyenda: bool = True):
    fig.update_layout(
        template="plotly_white",
        height=altura,
        margin=dict(l=24, r=20, t=58, b=34),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, Arial, sans-serif", color=COLORES["tinta"]),
        title=dict(font=dict(size=16, color=COLORES["tinta"]), x=0.03, xanchor="left"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text="",
        ),
        showlegend=leyenda,
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    fig.update_xaxes(showgrid=False, linecolor="#E2E8F0", tickfont=dict(size=11))
    fig.update_yaxes(gridcolor="#EDF2F7", zeroline=False, tickfont=dict(size=11))
    return fig


def porcentaje_cambio(actual: float, referencia: float) -> float:
    if referencia == 0 or pd.isna(referencia):
        return 0.0
    return ((actual - referencia) / abs(referencia)) * 100


def resetear_filtros() -> None:
    st.session_state["f_provincias"] = provincias_disponibles
    st.session_state["f_estaciones"] = estaciones_disponibles
    st.session_state["f_fechas"] = (fecha_minima, fecha_maxima)
    st.session_state["f_variable"] = list(VARIABLES.keys())[0]


# =========================================================
# DATOS Y FILTROS
# =========================================================

if not DATA_PATH.exists():
    st.error(
        "No se encontro el dataset. Verifica que exista el archivo "
        "data/datos_limpios_clima_puno_2020_2025.csv junto a app.py."
    )
    st.stop()

df = cargar_datos(DATA_PATH)

provincias_disponibles = sorted(df["provincia"].unique().tolist())
orden_estaciones = ["Verano", "Otoño", "Invierno", "Primavera"]
estaciones_disponibles = [
    estacion for estacion in orden_estaciones if estacion in df["estacion"].unique()
]
fecha_minima = df["fecha"].min().date()
fecha_maxima = df["fecha"].max().date()

if "f_fechas" not in st.session_state:
    st.session_state["f_fechas"] = (fecha_minima, fecha_maxima)
if "f_provincias" not in st.session_state:
    st.session_state["f_provincias"] = provincias_disponibles
if "f_estaciones" not in st.session_state:
    st.session_state["f_estaciones"] = estaciones_disponibles
if "f_variable" not in st.session_state:
    st.session_state["f_variable"] = list(VARIABLES.keys())[0]

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M4 14.5A4.5 4.5 0 0 1 8.5 10a5.5 5.5 0 0 1 10.2 2.8A3.8 3.8 0 1 1 19 20H7a4 4 0 0 1-3-5.5z"/>
                <path d="M8 4v2"/><path d="M4.2 6.2l1.4 1.4"/>
                <path d="M12 6.2 10.6 7.6"/>
            </svg>
        </div>
        <div>
            <div class="sidebar-brand-title">Clima Puno</div>
            <div class="sidebar-brand-subtitle">Panel ejecutivo · 2020-2025</div>
        </div>
    </div>
    <div class="filter-heading">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M4 21v-7"/><path d="M4 10V3"/><path d="M12 21v-9"/>
            <path d="M12 8V3"/><path d="M20 21v-5"/><path d="M20 12V3"/>
            <path d="M1 14h6"/><path d="M9 8h6"/><path d="M17 16h6"/>
        </svg>
        Filtros de analisis
    </div>
    <div class="filter-scope">
        <strong>Filtros globales:</strong> el periodo, las provincias y la estacion
        actualizan todas las vistas del dashboard.
    </div>
    """,
    unsafe_allow_html=True,
    width="stretch",
)

rango_fechas = st.sidebar.date_input(
    "Periodo de analisis",
    min_value=fecha_minima,
    max_value=fecha_maxima,
    key="f_fechas",
)

provincias = st.sidebar.multiselect(
    "Provincias",
    options=provincias_disponibles,
    key="f_provincias",
)

estaciones = st.sidebar.multiselect(
    "Estacion climatica",
    options=estaciones_disponibles,
    key="f_estaciones",
)

st.sidebar.button(
    "Restablecer filtros",
    width="stretch",
    on_click=resetear_filtros,
    icon=":material/restart_alt:",
)

if not provincias or not estaciones:
    st.warning("Selecciona al menos una provincia y una estacion climatica.")
    st.stop()

if isinstance(rango_fechas, (tuple, list)) and len(rango_fechas) == 2:
    fecha_inicio = pd.Timestamp(rango_fechas[0])
    fecha_fin = pd.Timestamp(rango_fechas[1])
else:
    fecha_inicio = pd.Timestamp(fecha_minima)
    fecha_fin = pd.Timestamp(fecha_maxima)

df_filtrado = df[
    df["fecha"].between(fecha_inicio, fecha_fin)
    & df["provincia"].isin(provincias)
    & df["estacion"].isin(estaciones)
].copy()

if df_filtrado.empty:
    st.error("La combinacion de filtros no contiene registros. Amplia el periodo o la seleccion.")
    st.stop()

st.sidebar.divider()
st.sidebar.markdown(
    f"""
    <div class="filter-summary">
        <div class="filter-summary-item">
            <div class="filter-summary-label">Registros</div>
            <div class="filter-summary-value">{len(df_filtrado):,}</div>
        </div>
        <div class="filter-summary-item">
            <div class="filter-summary-label">Provincias</div>
            <div class="filter-summary-value">{len(provincias)} de {len(provincias_disponibles)}</div>
        </div>
    </div>
    <div class="small-muted" style="margin-top:10px;">
        Periodo: {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}
    </div>
    """,
    unsafe_allow_html=True,
    width="stretch",
)
st.sidebar.link_button(
    "Consultar fuente NASA POWER",
    FUENTE_URL,
    width="stretch",
    icon=":material/open_in_new:",
)


# =========================================================
# CALCULOS PRINCIPALES
# =========================================================

resumen_provincia = (
    df_filtrado.groupby("provincia", as_index=False)
    .agg(
        temperatura_media=("temperatura_media_c", "mean"),
        temperatura_maxima=("temperatura_maxima_c", "max"),
        temperatura_minima=("temperatura_minima_c", "min"),
        precipitacion_total=("precipitacion_mm", "sum"),
        precipitacion_media=("precipitacion_mm", "mean"),
        humedad_media=("humedad_relativa_pct", "mean"),
        viento_maximo=("velocidad_viento_ms", "max"),
        radiacion_media=("radiacion_solar_kwh_m2", "mean"),
        registros_helada=("dia_con_helada", lambda x: int((x == "Sí").sum())),
        registros=("fecha", "size"),
    )
)
resumen_provincia["porcentaje_helada"] = (
    resumen_provincia["registros_helada"] / resumen_provincia["registros"] * 100
)

provincia_calida = resumen_provincia.loc[resumen_provincia["temperatura_media"].idxmax()]
provincia_fria = resumen_provincia.loc[resumen_provincia["temperatura_media"].idxmin()]
provincia_lluviosa = resumen_provincia.loc[resumen_provincia["precipitacion_total"].idxmax()]
provincia_heladas = resumen_provincia.loc[resumen_provincia["registros_helada"].idxmax()]

evento_extremo = df_filtrado.loc[df_filtrado["precipitacion_mm"].idxmax()]

temperatura_media = df_filtrado["temperatura_media_c"].mean()
precipitacion_media = df_filtrado["precipitacion_mm"].mean()
humedad_media = df_filtrado["humedad_relativa_pct"].mean()
registros_helada = int((df_filtrado["dia_con_helada"] == "Sí").sum())
porcentaje_helada = registros_helada / len(df_filtrado) * 100
viento_maximo = df_filtrado["velocidad_viento_ms"].max()
radiacion_media = df_filtrado["radiacion_solar_kwh_m2"].mean()

historico_temp = df["temperatura_media_c"].mean()
historico_precip = df["precipitacion_mm"].mean()
historico_humedad = df["humedad_relativa_pct"].mean()

delta_temp = temperatura_media - historico_temp
delta_precip = porcentaje_cambio(precipitacion_media, historico_precip)
delta_humedad = humedad_media - historico_humedad

if porcentaje_helada >= 30:
    nivel_helada, color_riesgo = "Alta exposicion", COLORES["rojo"]
elif porcentaje_helada >= 10:
    nivel_helada, color_riesgo = "Exposicion moderada", COLORES["amarillo"]
else:
    nivel_helada, color_riesgo = "Baja exposicion", COLORES["verde"]


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Observatorio climatico regional</div>
        <h1>Clima de la region Puno</h1>
        <p>
            Panel ejecutivo para comparar temperatura, precipitacion, humedad,
            viento, radiacion solar y presencia de heladas en las capitales provinciales.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="meta-line">
        <span>📅 {fecha_inicio.strftime('%d %b %Y')} - {fecha_fin.strftime('%d %b %Y')}</span>
        <span>📍 {len(provincias)} de {len(provincias_disponibles)} provincias</span>
        <span>🗂️ {len(df_filtrado):,} registros</span>
        <span>🛰️ NASA POWER</span>
        <span>🔄 Actualizado {datetime.now().strftime('%d/%m/%Y')}</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# KPI Y LIDERES
# =========================================================

titulo_seccion("indicadores", "Indicadores esenciales")

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    kpi_card(
        "🌡️",
        "Temperatura media",
        f"{temperatura_media:.1f} °C",
        f"{delta_temp:+.1f} °C frente al promedio 2020-2025",
        COLORES["rojo"],
    )
with k2:
    kpi_card(
        "🌧️",
        "Precipitacion diaria",
        f"{precipitacion_media:.2f} mm",
        f"{delta_precip:+.1f}% frente al promedio historico",
        COLORES["azul"],
    )
with k3:
    kpi_card(
        "💧",
        "Humedad media",
        f"{humedad_media:.1f}%",
        f"{delta_humedad:+.1f} puntos frente al historico",
        COLORES["celeste"],
    )
with k4:
    kpi_card(
        "❄️",
        "Registros con helada",
        f"{registros_helada:,}",
        f"{porcentaje_helada:.1f}% de las observaciones filtradas",
        COLORES["morado"],
    )
with k5:
    kpi_card(
        "💨",
        "Viento maximo",
        f"{viento_maximo:.1f} m/s",
        "Mayor valor observado en el periodo",
        COLORES["verde"],
    )
with k6:
    kpi_card(
        "☀️",
        "Radiacion media",
        f"{radiacion_media:.1f}",
        "kWh/m²/dia en las capitales seleccionadas",
        COLORES["amarillo"],
    )

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
titulo_seccion("lideres", "Provincias que lideran los indicadores")

l1, l2, l3, l4 = st.columns(4)
with l1:
    leader_card(
        "🔥",
        "Mayor temperatura media",
        str(provincia_calida["provincia"]),
        f"{provincia_calida['temperatura_media']:.2f} °C",
        "linear-gradient(135deg,#F97316,#E5484D)",
    )
with l2:
    leader_card(
        "🧊",
        "Menor temperatura media",
        str(provincia_fria["provincia"]),
        f"{provincia_fria['temperatura_media']:.2f} °C",
        "linear-gradient(135deg,#2563EB,#28B8D5)",
    )
with l3:
    leader_card(
        "🌧️",
        "Mayor precipitacion",
        str(provincia_lluviosa["provincia"]),
        f"{provincia_lluviosa['precipitacion_total']:,.1f} mm acumulados",
        "linear-gradient(135deg,#0E7490,#1677FF)",
    )
with l4:
    leader_card(
        "❄️",
        "Mayor presencia de heladas",
        str(provincia_heladas["provincia"]),
        f"{int(provincia_heladas['registros_helada']):,} registros ({provincia_heladas['porcentaje_helada']:.1f}%)",
        "linear-gradient(135deg,#6D5BD0,#3B82F6)",
    )

st.markdown(
    f"""
    <div class="insight-box">
        <strong>Lectura rapida.</strong>
        <strong>{provincia_calida['provincia']}</strong> presenta la mayor temperatura media,
        mientras que <strong>{provincia_fria['provincia']}</strong> registra el promedio mas frio.
        La mayor precipitacion acumulada corresponde a <strong>{provincia_lluviosa['provincia']}</strong>
        y la mayor frecuencia de heladas a <strong>{provincia_heladas['provincia']}</strong>.
        <span class="risk-pill" style="--risk-color:{color_riesgo};">{nivel_helada}</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# VISTAS DEL DASHBOARD
# =========================================================

tab_resumen, tab_detalle, tab_mapa, tab_datos = st.tabs(
    [
        "▦ Resumen ejecutivo",
        "⌁ Analisis detallado",
        "◎ Mapa y territorio",
        "↓ Datos y metodologia",
    ]
)


with tab_resumen:
    titulo_seccion("resumen", "Panorama climatico en una sola vista")

    # Tendencia mensual general
    mensual = (
        df_filtrado.assign(periodo=df_filtrado["fecha"].dt.to_period("M").dt.to_timestamp())
        .groupby("periodo", as_index=False)
        .agg(
            temperatura_media=("temperatura_media_c", "mean"),
            temperatura_maxima=("temperatura_maxima_c", "mean"),
            temperatura_minima=("temperatura_minima_c", "mean"),
            precipitacion_media=("precipitacion_mm", "mean"),
        )
    )

    fig_tendencia = go.Figure()
    fig_tendencia.add_trace(
        go.Scatter(
            x=mensual["periodo"],
            y=mensual["temperatura_maxima"],
            name="Maxima",
            line=dict(color="#F59E0B", width=1.7),
            hovertemplate="Maxima: %{y:.1f} °C<extra></extra>",
        )
    )
    fig_tendencia.add_trace(
        go.Scatter(
            x=mensual["periodo"],
            y=mensual["temperatura_media"],
            name="Media",
            line=dict(color="#E5484D", width=3),
            hovertemplate="Media: %{y:.1f} °C<extra></extra>",
        )
    )
    fig_tendencia.add_trace(
        go.Scatter(
            x=mensual["periodo"],
            y=mensual["temperatura_minima"],
            name="Minima",
            line=dict(color="#1677FF", width=1.7),
            hovertemplate="Minima: %{y:.1f} °C<extra></extra>",
        )
    )
    fig_tendencia.update_layout(title="Evolucion mensual de la temperatura")
    estilo_figura(fig_tendencia, altura=365)
    fig_tendencia.update_yaxes(title="Temperatura (°C)")

    # Patron mensual de precipitacion
    patron_mensual = (
        df_filtrado.groupby("mes_num", as_index=False)
        .agg(precipitacion_media=("precipitacion_mm", "mean"))
        .sort_values("mes_num")
    )
    patron_mensual["mes"] = patron_mensual["mes_num"].map(MESES)

    fig_estacional = px.bar(
        patron_mensual,
        x="mes",
        y="precipitacion_media",
        color="precipitacion_media",
        color_continuous_scale=["#DDF4FF", "#1677FF", "#0B3C6F"],
        title="Patron mensual de precipitacion",
        labels={"mes": "Mes", "precipitacion_media": "Precipitacion media (mm)"},
    )
    fig_estacional.update_traces(
        hovertemplate="%{x}: %{y:.2f} mm<extra></extra>",
        marker_line_width=0,
    )
    estilo_figura(fig_estacional, altura=365, leyenda=False)
    fig_estacional.update_layout(coloraxis_showscale=False)

    fila1_izq, fila1_der = st.columns([1.75, 1])
    with fila1_izq:
        st.plotly_chart(fig_tendencia, width="stretch")
        st.markdown(
            "<div class='chart-note'>La distancia entre las curvas maxima y minima muestra la amplitud termica. Los descensos mas marcados permiten reconocer la temporada fria.</div>",
            unsafe_allow_html=True,
        )
    with fila1_der:
        st.plotly_chart(fig_estacional, width="stretch")
        mes_lluvioso = patron_mensual.loc[patron_mensual["precipitacion_media"].idxmax()]
        st.markdown(
            f"<div class='chart-note'><strong>{mes_lluvioso['mes']}</strong> presenta la mayor precipitacion diaria media ({mes_lluvioso['precipitacion_media']:.2f} mm) dentro de la seleccion.</div>",
            unsafe_allow_html=True,
        )

    # Rankings provinciales
    ranking_temp = resumen_provincia.sort_values("temperatura_media", ascending=True)
    fig_ranking_temp = px.bar(
        ranking_temp,
        x="temperatura_media",
        y="provincia",
        orientation="h",
        color="temperatura_media",
        color_continuous_scale=["#1677FF", "#F8C146", "#E5484D"],
        title="Ranking de temperatura media",
        labels={"temperatura_media": "Temperatura media (°C)", "provincia": ""},
        text="temperatura_media",
    )
    fig_ranking_temp.update_traces(
        texttemplate="%{text:.1f}°",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:.2f} °C<extra></extra>",
    )
    estilo_figura(fig_ranking_temp, altura=430, leyenda=False)
    fig_ranking_temp.update_layout(coloraxis_showscale=False)

    ranking_helada = resumen_provincia.sort_values("registros_helada", ascending=True)
    fig_heladas = px.bar(
        ranking_helada,
        x="registros_helada",
        y="provincia",
        orientation="h",
        color="porcentaje_helada",
        color_continuous_scale=["#DDEAFE", "#7C5CFC", "#4338CA"],
        title="Ranking de registros con helada",
        labels={"registros_helada": "Registros con helada", "provincia": ""},
        text="registros_helada",
    )
    fig_heladas.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:,} registros<extra></extra>",
    )
    estilo_figura(fig_heladas, altura=430, leyenda=False)
    fig_heladas.update_layout(coloraxis_showscale=False)

    fila2_izq, fila2_der = st.columns(2)
    with fila2_izq:
        st.plotly_chart(fig_ranking_temp, width="stretch")
        st.markdown(
            f"<div class='chart-note'><strong>{provincia_calida['provincia']}</strong> encabeza el promedio termico; <strong>{provincia_fria['provincia']}</strong> ocupa el extremo mas frio.</div>",
            unsafe_allow_html=True,
        )
    with fila2_der:
        st.plotly_chart(fig_heladas, width="stretch")
        st.markdown(
            f"<div class='chart-note'><strong>{provincia_heladas['provincia']}</strong> concentra el mayor numero de observaciones bajo el umbral de 0 °C.</div>",
            unsafe_allow_html=True,
        )


with tab_detalle:
    titulo_seccion("analisis", "Distribuciones, relaciones y valores atipicos")

    control_variable, explicacion_control = st.columns([1, 2])
    with control_variable:
        variable_seleccionada = st.selectbox(
            "Variable del histograma",
            options=list(VARIABLES.keys()),
            key="f_variable",
            help="Modifica unicamente el histograma de esta seccion.",
        )
    with explicacion_control:
        st.markdown(
            """
            <div class="local-control-note">
                <span><strong>Control de esta vista.</strong> Esta variable modifica solo el
                histograma inferior. Los filtros de la barra lateral actualizan todo el dashboard.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    variable = VARIABLES[variable_seleccionada]
    unidad = UNIDADES[variable]

    # Histograma de variable seleccionada
    fig_histograma = px.histogram(
        df_filtrado,
        x=variable,
        nbins=42,
        color_discrete_sequence=[COLORES["azul"]],
        title=f"Distribucion de {variable_seleccionada.lower()}",
        labels={variable: f"{variable_seleccionada} ({unidad})", "count": "Registros"},
    )
    fig_histograma.add_vline(
        x=df_filtrado[variable].mean(),
        line_dash="dash",
        line_color=COLORES["rojo"],
        annotation_text=f"Promedio {df_filtrado[variable].mean():.2f}",
        annotation_position="top right",
    )
    estilo_figura(fig_histograma, altura=360, leyenda=False)

    # Boxplot de temperatura minima
    fig_caja = px.box(
        df_filtrado,
        x="provincia",
        y="temperatura_minima_c",
        color="provincia",
        points="outliers",
        title="Variacion de temperaturas minimas",
        labels={"provincia": "Provincia", "temperatura_minima_c": "Temperatura minima (°C)"},
    )
    fig_caja.add_hline(
        y=0,
        line_dash="dash",
        line_color=COLORES["rojo"],
        annotation_text="Umbral de helada",
    )
    estilo_figura(fig_caja, altura=360, leyenda=False)
    fig_caja.update_xaxes(tickangle=-35)

    d1, d2 = st.columns(2)
    with d1:
        st.plotly_chart(fig_histograma, width="stretch")
        st.markdown(
            f"<div class='chart-note'>La linea roja marca el promedio de <strong>{variable_seleccionada.lower()}</strong>. Los extremos ayudan a identificar episodios poco frecuentes.</div>",
            unsafe_allow_html=True,
        )
    with d2:
        st.plotly_chart(fig_caja, width="stretch")
        st.markdown(
            "<div class='chart-note'>La linea de 0 °C permite comparar rapidamente que provincias presentan mayor exposicion a heladas.</div>",
            unsafe_allow_html=True,
        )

    # Relacion mensual y correlacion
    relacion = (
        df_filtrado.assign(periodo=df_filtrado["fecha"].dt.to_period("M").dt.to_timestamp())
        .groupby(["periodo", "provincia"], as_index=False)
        .agg(
            humedad_media=("humedad_relativa_pct", "mean"),
            precipitacion_media=("precipitacion_mm", "mean"),
            temperatura_media=("temperatura_media_c", "mean"),
            radiacion_media=("radiacion_solar_kwh_m2", "mean"),
        )
    )

    fig_dispersion = px.scatter(
        relacion,
        x="humedad_media",
        y="precipitacion_media",
        color="temperatura_media",
        size="radiacion_media",
        hover_name="provincia",
        hover_data={"periodo": True, "temperatura_media": ":.1f", "radiacion_media": ":.1f"},
        color_continuous_scale="Turbo",
        title="Humedad y precipitacion por provincia-mes",
        labels={
            "humedad_media": "Humedad relativa (%)",
            "precipitacion_media": "Precipitacion media (mm)",
            "temperatura_media": "Temperatura (°C)",
        },
    )
    estilo_figura(fig_dispersion, altura=420)

    columnas_corr = [
        "temperatura_media_c",
        "temperatura_maxima_c",
        "temperatura_minima_c",
        "precipitacion_mm",
        "humedad_relativa_pct",
        "velocidad_viento_ms",
        "radiacion_solar_kwh_m2",
    ]
    nombres_corr = {
        "temperatura_media_c": "Temp. media",
        "temperatura_maxima_c": "Temp. maxima",
        "temperatura_minima_c": "Temp. minima",
        "precipitacion_mm": "Precipitacion",
        "humedad_relativa_pct": "Humedad",
        "velocidad_viento_ms": "Viento",
        "radiacion_solar_kwh_m2": "Radiacion",
    }
    columnas_validas = [c for c in columnas_corr if df_filtrado[c].nunique() > 1]

    if len(columnas_validas) >= 2:
        correlacion = df_filtrado[columnas_validas].corr().rename(
            index=nombres_corr,
            columns=nombres_corr,
        )
        fig_correlacion = px.imshow(
            correlacion,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Matriz de correlacion climatica",
        )
        estilo_figura(fig_correlacion, altura=420, leyenda=False)
        fig_correlacion.update_layout(coloraxis_colorbar=dict(title="Correlacion"))
    else:
        fig_correlacion = None

    d3, d4 = st.columns(2)
    with d3:
        st.plotly_chart(fig_dispersion, width="stretch")
        st.markdown(
            "<div class='chart-note'>Cada burbuja resume una provincia y un mes. La posicion muestra humedad y lluvia; el color, temperatura; y el tamaño, radiacion solar.</div>",
            unsafe_allow_html=True,
        )
    with d4:
        if fig_correlacion is not None:
            st.plotly_chart(fig_correlacion, width="stretch")
            st.markdown(
                "<div class='chart-note'>Valores cercanos a 1 o -1 indican relaciones mas fuertes; valores proximos a 0 representan relaciones debiles.</div>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Amplia el periodo para calcular correlaciones entre variables.")

    st.warning(
        f"Evento extremo visible: {evento_extremo['precipitacion_mm']:.2f} mm de precipitacion "
        f"en {evento_extremo['provincia']} el {evento_extremo['fecha'].strftime('%d/%m/%Y')}. "
        "Debe contrastarse con registros de SENAMHI antes de interpretarlo como evento confirmado."
    )


with tab_mapa:
    titulo_seccion("mapa", "Distribucion territorial de los indicadores")

    mapa = (
        df_filtrado.groupby(["provincia", "capital", "latitud", "longitud"], as_index=False)
        .agg(
            temperatura_media=("temperatura_media_c", "mean"),
            precipitacion_media=("precipitacion_mm", "mean"),
            humedad_media=("humedad_relativa_pct", "mean"),
            heladas=("dia_con_helada", lambda x: int((x == "Sí").sum())),
        )
    )
    mapa["tamano"] = mapa["precipitacion_media"].clip(lower=0.16)

    fig_mapa = px.scatter_geo(
        mapa,
        lat="latitud",
        lon="longitud",
        size="tamano",
        color="temperatura_media",
        hover_name="provincia",
        hover_data={
            "capital": True,
            "temperatura_media": ":.2f",
            "precipitacion_media": ":.2f",
            "humedad_media": ":.1f",
            "heladas": True,
            "tamano": False,
            "latitud": False,
            "longitud": False,
        },
        color_continuous_scale="Turbo",
        size_max=42,
        projection="mercator",
        title="Capitales provinciales: temperatura y precipitacion media",
        labels={"temperatura_media": "Temperatura (°C)"},
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
        coastlinecolor="#64748B",
    )
    estilo_figura(fig_mapa, altura=650)
    fig_mapa.update_layout(coloraxis_colorbar=dict(title="Temp.<br>media °C"))
    st.plotly_chart(fig_mapa, width="stretch")

    st.markdown(
        """
        <div class="insight-box">
            <strong>Como leer el mapa:</strong> el color de cada circulo representa la temperatura
            media y su tamaño representa la precipitacion diaria media. Al colocar el cursor se
            muestran humedad y registros de helada. Los puntos corresponden a capitales provinciales,
            no a toda la superficie de cada provincia.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Comparacion provincial")
    tabla_mapa = resumen_provincia[
        [
            "provincia",
            "temperatura_media",
            "precipitacion_media",
            "humedad_media",
            "registros_helada",
            "porcentaje_helada",
        ]
    ].copy()
    tabla_mapa.columns = [
        "Provincia",
        "Temperatura media (°C)",
        "Precipitacion media (mm)",
        "Humedad media (%)",
        "Registros con helada",
        "Heladas (%)",
    ]
    st.dataframe(
        tabla_mapa.round(2),
        width="stretch",
        hide_index=True,
    )


with tab_datos:
    titulo_seccion("datos", "Datos, descarga y trazabilidad")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            """
            <div class="method-card">
                <strong>🛰️ Fuente verificable</strong>
                NASA POWER, datos diarios de meteorologia y energia solar para las coordenadas
                de las capitales provinciales.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="method-card">
                <strong>🧹 Preparacion</strong>
                Integracion de 13 consultas, normalizacion de nombres, conversion de fechas,
                validacion de rangos y creacion de variables derivadas.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="method-card">
                <strong>⚠️ Limitacion</strong>
                NASA POWER trabaja con cuadriculas. Una capital provincial es un punto de
                referencia y no representa toda la diversidad territorial de la provincia.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Resumen de la seleccion")
    resumen_seleccion = pd.DataFrame(
        {
            "Indicador": [
                "Registros",
                "Provincias",
                "Fecha inicial",
                "Fecha final",
                "Variable seleccionada",
                "Registros con helada",
            ],
            "Valor": [
                f"{len(df_filtrado):,}",
                str(len(provincias)),
                fecha_inicio.strftime("%d/%m/%Y"),
                fecha_fin.strftime("%d/%m/%Y"),
                variable_seleccionada,
                f"{registros_helada:,}",
            ],
        }
    )
    st.dataframe(resumen_seleccion, width="stretch", hide_index=True)

    csv_filtrado = df_filtrado.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇ Descargar datos filtrados en CSV",
        data=csv_filtrado,
        file_name="datos_climaticos_puno_filtrados.csv",
        mime="text/csv",
        width="stretch",
    )

    with st.expander("Ver registros filtrados"):
        st.dataframe(df_filtrado, width="stretch", hide_index=True)

    st.markdown(
        f"""
        <div class="small-muted">
            <strong>Integrantes:</strong> {INTEGRANTES}<br>
            <strong>Fuente:</strong> <a href="{FUENTE_URL}" target="_blank">NASA POWER</a><br>
            <strong>Periodo original:</strong> 2020-2025 · <strong>Frecuencia:</strong> diaria ·
            <strong>Unidad geografica:</strong> capital provincial.
        </div>
        """,
        unsafe_allow_html=True,
    )
