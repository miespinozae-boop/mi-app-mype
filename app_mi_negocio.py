
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# NEXDATA — DASHBOARD
# =========================================================
st.set_page_config(
    page_title="NEXDATA | Inteligencia de Datos",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# PALETA EXACTA DEL MOCKUP
# -----------------------------
NAVY = "#0B1736"
NAVY_2 = "#142653"
PURPLE = "#4F46E5"
PURPLE_2 = "#6366F1"
BLUE = "#2388F5"
CYAN = "#08B7C8"
TEAL = "#08B39A"
GREEN = "#18B77A"
ORANGE = "#F6A43A"
RED = "#F25570"
PINK = "#F05D83"
BG = "#F5F8FD"
WHITE = "#FFFFFF"
TEXT = "#13203F"
MUTED = "#64748B"
BORDER = "#E1E8F3"
SOFT_BLUE = "#EEF4FF"

PRODUCT_COLORS = [
    PURPLE, TEAL, ORANGE, PINK, BLUE,
    "#6D5CE7", "#14B8A6", "#F59E0B", "#EC4899", "#3B82F6"
]

REQUIRED = [
    "Fecha", "Producto", "Categoria", "Canal_Venta",
    "Ventas_Soles", "Utilidad_Soles"
]

# =========================================================
# CSS — ESTILO DEL MOCKUP
# =========================================================
st.markdown(f"""
<style>
    html, body, [class*="css"] {{
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    .stApp {{
        background: {BG};
    }}

    /* SIDEBAR */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0A1735 0%, #101E43 100%);
        border: 0;
        min-width: 238px;
        max-width: 238px;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 18px;
    }}

    [data-testid="stSidebar"] * {{
        color: #EAF0FF;
    }}

    .brand-wrap {{
        padding: 0 10px 18px 10px;
    }}

    .brand {{
        display:flex;
        align-items:center;
        gap:11px;
    }}

    .brand-logo {{
        font-size:40px;
        font-weight:900;
        line-height:1;
        letter-spacing:-6px;
        color:#5146E5;
        text-shadow: 8px 0 0 #756BFF;
        width:48px;
    }}

    .brand-name {{
        font-size:22px;
        font-weight:800;
        letter-spacing:-.7px;
    }}

    .brand-name span {{
        color:#6574FF;
    }}

    .brand-tag {{
        font-size:11px;
        line-height:1.35;
        color:#D1DAF0 !important;
        margin:3px 0 0 59px;
        max-width:135px;
    }}

    .side-nav-title {{
        color:#7F8EB3 !important;
        font-size:10px;
        font-weight:800;
        letter-spacing:.8px;
        margin:8px 0 8px 3px;
    }}

    .side-info {{
        margin:18px 4px 0 4px;
        padding:18px 14px;
        border-radius:15px;
        border:1px solid rgba(255,255,255,.12);
        background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.035));
    }}

    .side-info-title {{
        font-size:12px;
        font-weight:800;
        color:white !important;
    }}

    .side-info-text {{
        font-size:10px;
        line-height:1.5;
        color:#C8D3EB !important;
        margin-top:5px;
    }}

    /* RADIO NAV */
    [data-testid="stSidebar"] div[role="radiogroup"] {{
        gap:5px;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label {{
        border-radius:10px;
        padding:9px 10px !important;
        margin:0 !important;
        transition:.15s;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background:rgba(99,102,241,.18);
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {{
        background:linear-gradient(90deg,#4B46D8,#3946A7);
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label p {{
        font-size:12px !important;
        font-weight:650 !important;
    }}

    /* MAIN */
    .topbar {{
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:14px;
    }}

    .welcome {{
        font-size:24px;
        font-weight:850;
        color:{TEXT};
        letter-spacing:-.8px;
    }}

    .welcome-sub {{
        color:#4D5F84;
        font-size:12px;
        margin-top:1px;
    }}

    .top-user {{
        display:flex;
        align-items:center;
        gap:9px;
    }}

    .date-chip {{
        border:1px solid {BORDER};
        background:white;
        border-radius:10px;
        padding:9px 13px;
        font-size:11px;
        color:{TEXT};
    }}

    .avatar {{
        width:36px;
        height:36px;
        border-radius:50%;
        background:{NAVY};
        color:white;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:11px;
        font-weight:800;
    }}

    .hero {{
        border:1px solid #D9E4FA;
        border-radius:14px;
        min-height:190px;
        padding:25px 30px;
        background:
            radial-gradient(circle at 70% 45%, rgba(115,125,255,.16), transparent 28%),
            linear-gradient(105deg,#F0F3FF 0%,#F7F9FF 48%,#EAF6FF 100%);
        position:relative;
        overflow:hidden;
        margin-bottom:17px;
    }}

    .hero-title {{
        font-size:26px;
        font-weight:850;
        line-height:1.13;
        color:{NAVY};
        letter-spacing:-.8px;
        max-width:410px;
    }}

    .hero-title span {{
        color:{PURPLE};
    }}

    .hero-text {{
        color:#4B608B;
        font-size:12px;
        line-height:1.55;
        max-width:480px;
        margin-top:10px;
    }}

    .hero-buttons {{
        margin-top:15px;
    }}

    .hero-button {{
        display:inline-block;
        padding:10px 19px;
        border-radius:999px;
        font-size:11px;
        font-weight:750;
        margin-right:8px;
    }}

    .hero-primary {{
        background:linear-gradient(90deg,#4C46E8,#6256F3);
        color:white !important;
        box-shadow:0 6px 16px rgba(79,70,229,.25);
    }}

    .hero-secondary {{
        border:1px solid #B8C6E2;
        color:{NAVY} !important;
        background:rgba(255,255,255,.5);
    }}

    .hero-art {{
        position:absolute;
        right:220px;
        top:32px;
        width:260px;
        height:125px;
    }}

    .laptop {{
        position:absolute;
        left:45px;
        top:8px;
        width:170px;
        height:98px;
        border:6px solid #354BC4;
        border-radius:8px;
        background:linear-gradient(135deg,#FFFFFF,#EAF0FF);
        box-shadow:0 12px 25px rgba(44,65,150,.15);
    }}

    .laptop-screen {{
        padding:14px 12px;
    }}

    .mini-line {{
        height:5px;
        width:58px;
        border-radius:5px;
        background:#9AA8FF;
        margin-bottom:10px;
    }}

    .mini-bars {{
        display:flex;
        align-items:end;
        gap:5px;
        height:44px;
    }}

    .mini-bars i {{
        display:block;
        width:13px;
        border-radius:2px 2px 0 0;
        background:{PURPLE};
    }}

    .mini-bars i:nth-child(1) {{height:18px}}
    .mini-bars i:nth-child(2) {{height:27px;background:{TEAL}}}
    .mini-bars i:nth-child(3) {{height:35px;background:{ORANGE}}}
    .mini-bars i:nth-child(4) {{height:42px;background:{BLUE}}}

    .laptop-base {{
        position:absolute;
        left:25px;
        top:101px;
        width:220px;
        height:9px;
        background:#6682E6;
        border-radius:0 0 10px 10px;
    }}

    .plant {{
        position:absolute;
        right:8px;
        bottom:6px;
        font-size:39px;
        opacity:.75;
    }}

    .hero-checks {{
        position:absolute;
        right:25px;
        top:31px;
        width:190px;
    }}

    .check {{
        color:#344B72;
        font-size:10px;
        margin:0 0 12px 0;
    }}

    .check b {{
        color:{PURPLE};
        margin-right:7px;
    }}

    /* KPI */
    .kpi {{
        background:white;
        border:1px solid {BORDER};
        border-radius:13px;
        min-height:126px;
        padding:15px 16px 10px 16px;
        box-shadow:0 4px 16px rgba(28,48,91,.035);
        position:relative;
        overflow:hidden;
    }}

    .kpi-top {{
        display:flex;
        align-items:center;
        gap:10px;
    }}

    .kpi-icon {{
        width:39px;
        height:39px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:17px;
        font-weight:800;
    }}

    .kpi-label {{
        font-size:10px;
        font-weight:700;
        color:{TEXT};
    }}

    .kpi-value {{
        font-size:22px;
        font-weight:850;
        color:{NAVY};
        margin:8px 0 4px 49px;
        letter-spacing:-.5px;
    }}

    .kpi-delta {{
        margin-left:49px;
        font-size:10px;
        font-weight:750;
        color:{GREEN};
    }}

    .kpi-note {{
        margin-left:49px;
        color:#73819A;
        font-size:9px;
    }}

    .spark {{
        position:absolute;
        right:13px;
        bottom:18px;
        width:75px;
        height:27px;
    }}

    /* CARDS */
    .card {{
        background:white;
        border:1px solid {BORDER};
        border-radius:12px;
        padding:14px 15px 10px 15px;
        box-shadow:0 4px 16px rgba(28,48,91,.03);
        margin-top:14px;
    }}

    .card-title {{
        color:{NAVY};
        font-size:14px;
        font-weight:820;
    }}

    .card-sub {{
        color:#71809B;
        font-size:10px;
        margin-top:3px;
        margin-bottom:6px;
    }}

    .alert-row {{
        display:flex;
        align-items:center;
        gap:10px;
        padding:9px 0;
        border-bottom:1px solid #EEF2F7;
    }}

    .alert-row:last-child {{
        border-bottom:0;
    }}

    .alert-dot {{
        width:30px;
        height:30px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:800;
        font-size:12px;
        flex-shrink:0;
    }}

    .alert-main {{
        flex:1;
    }}

    .alert-title {{
        color:{TEXT};
        font-size:10px;
        font-weight:760;
    }}

    .alert-desc {{
        color:#7A879E;
        font-size:9px;
        margin-top:2px;
    }}

    .status {{
        border-radius:999px;
        padding:4px 9px;
        font-size:8px;
        font-weight:800;
    }}

    .status-red {{ color:#C3324B; background:#FFF0F3; border:1px solid #FFD2DA; }}
    .status-orange {{ color:#A76500; background:#FFF7E8; border:1px solid #FFE0A8; }}
    .status-green {{ color:#087B52; background:#ECFBF5; border:1px solid #BDEFD9; }}

    .insight {{
        display:flex;
        align-items:center;
        gap:10px;
        padding:10px 0;
        border-bottom:1px solid #EEF2F7;
    }}

    .insight:last-child {{ border-bottom:0; }}

    .insight-icon {{
        width:30px;
        height:30px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:12px;
        font-weight:800;
        flex-shrink:0;
    }}

    .insight-title {{
        font-size:9px;
        color:{TEXT};
        font-weight:700;
    }}

    .insight-text {{
        font-size:8px;
        color:#7A879E;
        margin-top:2px;
        line-height:1.35;
    }}

    .sim-tabs {{
        display:flex;
        gap:5px;
        margin:8px 0;
    }}

    .sim-pill {{
        border:1px solid #DDE5F2;
        background:#FAFBFD;
        border-radius:999px;
        padding:6px 14px;
        font-size:8px;
        color:{TEXT};
    }}

    .sim-pill.active {{
        background:{PURPLE};
        color:white;
        border-color:{PURPLE};
    }}

    .sim-result {{
        background:linear-gradient(110deg,#F3F7FF,#EDF5FF);
        border-radius:9px;
        padding:11px;
        display:flex;
        justify-content:space-around;
        margin-top:8px;
    }}

    .sim-result div {{
        text-align:left;
        padding:0 10px;
        border-right:1px solid #DCE5F2;
    }}

    .sim-result div:last-child {{ border-right:0; }}

    .sim-label {{
        font-size:8px;
        color:#6D7D98;
    }}

    .sim-value {{
        font-size:13px;
        color:{NAVY};
        font-weight:820;
        margin-top:3px;
    }}

    .footer {{
        text-align:center;
        color:#98A4B8;
        font-size:9px;
        padding:22px 0 5px;
    }}

    /* Streamlit cleanup */
    #MainMenu, footer {{visibility:hidden;}}
    .block-container {{padding-top:18px; padding-bottom:10px;}}
    [data-testid="stHeader"] {{background:transparent;}}
    .stButton > button {{
        border-radius:9px;
        font-weight:700;
        border:1px solid #D8E1EF;
    }}
    div[data-testid="stMetric"] {{
        background:white;
        border:1px solid {BORDER};
        border-radius:12px;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATOS
# =========================================================
@st.cache_data
def read_demo():
    return pd.read_csv("dataset_mype_transacciones.csv")

def prepare(df):
    df = df.copy()
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Faltan columnas obligatorias: " + ", ".join(missing))
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df["Ventas_Soles"] = pd.to_numeric(df["Ventas_Soles"], errors="coerce").fillna(0)
    df["Utilidad_Soles"] = pd.to_numeric(df["Utilidad_Soles"], errors="coerce").fillna(0)
    for c in ["Producto", "Categoria", "Canal_Venta"]:
        df[c] = df[c].fillna("Sin especificar").astype(str)
    return df.dropna(subset=["Fecha"]).sort_values("Fecha").reset_index(drop=True)

try:
    df_base = prepare(read_demo())
except Exception as e:
    st.error("No se pudo cargar dataset_mype_transacciones.csv")
    st.code(str(e))
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
    <div class="brand-wrap">
        <div class="brand">
            <div class="brand-logo">N</div>
            <div class="brand-name">NEX<span>DATA</span></div>
        </div>
        <div class="brand-tag">Conecta tus datos con mejores decisiones.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="side-nav-title">NAVEGACIÓN</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navegación",
        [
            "Inicio",
            "Dashboard",
            "Análisis",
            "Rentabilidad",
            "Alertas y Decisiones",
            "Simulador",
            "Datos",
            "Configuración",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Datos del negocio")

    upload = st.file_uploader(
        "Cargar datos",
        type=["csv", "xlsx"],
        label_visibility="collapsed",
    )

    if upload:
        try:
            if upload.name.lower().endswith(".xlsx"):
                uploaded_df = pd.read_excel(upload)
            else:
                uploaded_df = pd.read_csv(upload)
            df = prepare(uploaded_df)
            st.success("Datos cargados")
        except Exception as e:
            st.error(f"Archivo no válido: {e}")
            df = df_base.copy()
    else:
        df = df_base.copy()

    st.markdown("""
    <div class="side-info">
        <div class="side-info-title">Tu negocio tiene datos.</div>
        <div class="side-info-text">
        NEXDATA transforma información en hallazgos, alertas y decisiones accionables.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FILTROS GLOBALES
# =========================================================
max_date = df["Fecha"].max()
min_date = df["Fecha"].min()

with st.sidebar:
    st.markdown("### Periodo")
    periodo = st.selectbox(
        "Periodo",
        ["Últimos 30 días", "Mes actual", "Mes anterior", "Todo el registro"],
        label_visibility="collapsed",
    )

if periodo == "Últimos 30 días":
    end = max_date
    start = max_date - pd.Timedelta(days=29)
elif periodo == "Mes actual":
    start = max_date.replace(day=1)
    end = max_date
elif periodo == "Mes anterior":
    end = max_date.replace(day=1) - pd.Timedelta(days=1)
    start = end.replace(day=1)
else:
    start, end = min_date, max_date

curr = df[(df["Fecha"] >= start) & (df["Fecha"] <= end)].copy()

if curr.empty:
    st.warning("No hay datos para el periodo seleccionado.")
    st.stop()

# =========================================================
# KPIs
# =========================================================
sales = curr["Ventas_Soles"].sum()
profit = curr["Utilidad_Soles"].sum()
margin = profit / sales * 100 if sales else 0
n_sales = len(curr)
ticket = sales / n_sales if n_sales else 0

previous_end = start - pd.Timedelta(days=1)
days = max((end - start).days + 1, 1)
previous_start = previous_end - pd.Timedelta(days=days - 1)
prev = df[(df["Fecha"] >= previous_start) & (df["Fecha"] <= previous_end)]

sales_prev = prev["Ventas_Soles"].sum()
profit_prev = prev["Utilidad_Soles"].sum()
margin_prev = profit_prev / sales_prev * 100 if sales_prev else 0
ticket_prev = sales_prev / len(prev) if len(prev) else 0

def pct(a, b):
    if b == 0:
        return np.nan
    return (a - b) / abs(b) * 100

d_sales = pct(sales, sales_prev)
d_profit = pct(profit, profit_prev)
d_margin = margin - margin_prev
d_ticket = pct(ticket, ticket_prev)

def money(x):
    return f"S/ {x:,.2f}"

# =========================================================
# TOPBAR
# =========================================================
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="welcome">¡Hola!</div>
        <div class="welcome-sub">Aquí tienes un resumen del rendimiento de tu negocio.</div>
    </div>
    <div class="top-user">
        <div class="date-chip">▣ &nbsp; {start.strftime("%d %b. %Y")} – {end.strftime("%d %b. %Y")} &nbsp;⌄</div>
        <div class="avatar">NE</div>
        <div style="font-size:11px;font-weight:750;color:{TEXT};">NEXDATA &nbsp;⌄</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================
# =========================================================
# HERO PRINCIPAL
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-title">
        Convierte tus datos<br>
        en <span>oportunidades</span>
    </div>

    <div class="hero-text">
        Analiza el rendimiento de tu negocio, identifica oportunidades
        de mejora y toma decisiones con confianza.
    </div>

    <div class="hero-buttons">
        <span class="hero-button hero-primary">
            Cargar datos
        </span>

        <span class="hero-button hero-secondary">
            ▶ Ver tutorial
        </span>
    </div>

    <!-- ILUSTRACIÓN -->
    <div class="hero-art">

        <div class="laptop">

            <div class="laptop-screen">

                <div class="mini-line"></div>

                <div class="mini-bars">
                    <i></i>
                    <i></i>
                    <i></i>
                    <i></i>
                </div>

            </div>

        </div>

        <div class="laptop-base"></div>

        <div class="plant">♧</div>

    </div>

    <!-- BENEFICIOS -->
    <div class="hero-checks">

        <div class="check">
            <b>✓</b> Análisis en tiempo real
        </div>

        <div class="check">
            <b>✓</b> Alertas automáticas
        </div>

        <div class="check">
            <b>✓</b> Recomendaciones personalizadas
        </div>

        <div class="check">
            <b>✓</b> Simulador de escenarios
        </div>

        <div class="check">
            <b>✓</b> Carga de tus propios datos
        </div>

    </div>

</div>
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)

# =========================================================
# KPI CARDS
# =========================================================
k1, k2, k3, k4 = st.columns(4)

def spark_svg(color):
    return f"""
    <svg class="spark" viewBox="0 0 90 30">
      <path d="M2 24 C12 24, 12 17, 22 18 S31 8, 40 13 S52 20, 60 10 S72 14, 88 2"
            fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>
    </svg>
    """

cards = [
    ("💰", "#DDF8F0", GREEN, "Ventas Totales", money(sales), d_sales, "vs. mes anterior"),
    ("▣", "#ECE8FF", PURPLE, "Utilidad Neta", money(profit), d_profit, "vs. mes anterior"),
    ("%", "#E1F1FF", BLUE, "Margen de Utilidad", f"{margin:.1f}%", d_margin, "vs. mes anterior"),
    ("🛒", "#FFE8ED", RED, "Ticket Promedio", money(ticket), d_ticket, "vs. mes anterior"),
]

for col, (icon, bg, color, label, value, delta, note) in zip([k1,k2,k3,k4], cards):
    delta_text = "—" if np.isnan(delta) else f"↑ {delta:.1f}%"
    if label == "Margen de Utilidad":
        delta_text = "↑ " + f"{delta:.1f}%" if delta >= 0 else "↓ " + f"{abs(delta):.1f}%"
    with col:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-top">
                <div class="kpi-icon" style="background:{bg};color:{color};">{icon}</div>
                <div class="kpi-label">{label}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta" style="color:{GREEN if delta >= 0 else RED};">{delta_text}</div>
            <div class="kpi-note">{note}</div>
            {spark_svg(color)}
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# DASHBOARD PRINCIPAL
# =========================================================
def product_table():
    return curr.groupby("Producto")["Ventas_Soles"].sum().sort_values(ascending=False).reset_index()

def category_table():
    return curr.groupby("Categoria")["Ventas_Soles"].sum().sort_values(ascending=False).reset_index()

prod = product_table()
cat = category_table()
channel = curr.groupby("Canal_Venta")["Ventas_Soles"].sum().sort_values(ascending=False).reset_index()

if page in ["Inicio", "Dashboard"]:

    left, middle, right = st.columns([1.45, 1.12, .85])

    # Productos
    with left:
        st.markdown("""
        <div class="card">
            <div class="card-title">Ventas por Producto</div>
            <div class="card-sub">Top 5 productos con mayor volumen de ventas</div>
        """, unsafe_allow_html=True)

        p = prod.head(5).sort_values("Ventas_Soles", ascending=True)
        fig = px.bar(
            p, x="Ventas_Soles", y="Producto",
            orientation="h", color="Producto",
            color_discrete_sequence=PRODUCT_COLORS,
            text="Ventas_Soles"
        )
        fig.update_traces(
            texttemplate="S/ %{text:,.0f}",
            textposition="outside",
            cliponaxis=False
        )
        fig.update_layout(
            height=255, showlegend=False,
            margin=dict(l=0,r=30,t=8,b=5),
            paper_bgcolor="white", plot_bgcolor="white",
            font=dict(size=9,color=TEXT),
            xaxis=dict(showgrid=True,gridcolor="#EEF2F7",title=None),
            yaxis=dict(showgrid=False,title=None)
        )
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Categorías
    with middle:
        st.markdown("""
        <div class="card">
            <div class="card-title">Ventas por Categoría</div>
            <div class="card-sub">Distribución de ingresos por categoría</div>
        """, unsafe_allow_html=True)

        fig = px.pie(
            cat, names="Categoria", values="Ventas_Soles",
            hole=.58, color_discrete_sequence=PRODUCT_COLORS
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate="%{label}<br>S/ %{value:,.2f}<extra></extra>"
        )
        fig.update_layout(
            height=255, showlegend=True,
            legend=dict(font=dict(size=8), orientation="v", x=1.0, y=.5),
            margin=dict(l=0,r=75,t=8,b=0),
            paper_bgcolor="white",
            font=dict(size=9,color=TEXT),
            annotations=[dict(
                text=f"<b>Total</b><br>S/ {sales:,.0f}",
                x=.5,y=.5,showarrow=False,
                font=dict(size=11,color=NAVY)
            )]
        )
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Canales
    with right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Canales de Venta</div>
            <div class="card-sub">Rendimiento por canal</div>
        """, unsafe_allow_html=True)

        total_channel = channel["Ventas_Soles"].sum() or 1
        channel_colors = [PURPLE, TEAL, ORANGE, PINK, "#94A3B8"]

        for i,row in channel.head(5).iterrows():
            share = row["Ventas_Soles"] / total_channel * 100
            color = channel_colors[i % len(channel_colors)]
            st.markdown(f"""
            <div style="margin:11px 0;">
                <div style="display:flex;justify-content:space-between;
                font-size:9px;color:{TEXT};font-weight:650;">
                    <span>{row["Canal_Venta"]}</span><span>{share:.0f}%</span>
                </div>
                <div style="height:7px;background:#EDF1F7;border-radius:8px;margin-top:5px;">
                    <div style="height:7px;width:{share}%;background:{color};
                    border-radius:8px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Evolución
    st.markdown("""
    <div class="card">
        <div class="card-title">Evolución de Ventas y Utilidad</div>
        <div class="card-sub">Comportamiento durante el periodo seleccionado</div>
    """, unsafe_allow_html=True)

    daily = curr.groupby(curr["Fecha"].dt.date)[["Ventas_Soles","Utilidad_Soles"]].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(daily.index), y=daily["Ventas_Soles"],
        mode="lines", name="Ventas",
        line=dict(color=PURPLE,width=3)
    ))
    fig.add_trace(go.Scatter(
        x=list(daily.index), y=daily["Utilidad_Soles"],
        mode="lines", name="Utilidad",
        line=dict(color=TEAL,width=3)
    ))
    fig.update_layout(
        height=260, margin=dict(l=5,r=5,t=5,b=5),
        paper_bgcolor="white",plot_bgcolor="white",
        font=dict(size=9,color=TEXT),
        legend=dict(orientation="h",y=1.08,x=0),
        xaxis=dict(showgrid=False,title=None),
        yaxis=dict(showgrid=True,gridcolor="#EEF2F7",title=None),
        hovermode="x unified"
    )
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ANÁLISIS
# =========================================================
if page == "Análisis":
    st.markdown('<div class="card"><div class="card-title">Análisis del negocio</div>'
                '<div class="card-sub">Indicadores para entender el comportamiento de tus ventas.</div></div>',
                unsafe_allow_html=True)

    a,b,c = st.columns(3)
    a.metric("Ventas",money(sales))
    b.metric("Utilidad",money(profit))
    c.metric("Margen",f"{margin:.1f}%")

    st.markdown('<div class="card"><div class="card-title">Ventas por producto</div></div>',unsafe_allow_html=True)
    fig = px.bar(prod.head(10),x="Producto",y="Ventas_Soles",color="Producto",
                 color_discrete_sequence=PRODUCT_COLORS,text="Ventas_Soles")
    fig.update_traces(texttemplate="S/ %{text:,.0f}",textposition="outside")
    fig.update_layout(height=400,showlegend=False,paper_bgcolor="white",plot_bgcolor="white",
                      margin=dict(l=10,r=10,t=15,b=80))
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

# =========================================================
# RENTABILIDAD
# =========================================================
if page == "Rentabilidad":
    profitability = curr.groupby("Producto")[["Ventas_Soles","Utilidad_Soles"]].sum()
    profitability["Margen"] = np.where(
        profitability["Ventas_Soles"] > 0,
        profitability["Utilidad_Soles"] / profitability["Ventas_Soles"] * 100,
        0
    )
    profitability = profitability.sort_values("Margen",ascending=False).reset_index()

    st.markdown('<div class="card"><div class="card-title">Rentabilidad por Producto</div>'
                '<div class="card-sub">Productos con mejor y menor margen.</div></div>',
                unsafe_allow_html=True)

    fig = px.bar(profitability.head(10),x="Producto",y="Margen",color="Producto",
                 color_discrete_sequence=PRODUCT_COLORS,text="Margen")
    fig.update_traces(texttemplate="%{text:.1f}%",textposition="outside")
    fig.update_layout(height=400,showlegend=False,paper_bgcolor="white",plot_bgcolor="white",
                      yaxis_title="Margen (%)",xaxis_title=None)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    st.dataframe(
        profitability.style.format({
            "Ventas_Soles":"S/ {:,.2f}",
            "Utilidad_Soles":"S/ {:,.2f}",
            "Margen":"{:.1f}%"
        }),
        use_container_width=True
    )

# =========================================================
# ALERTAS
# =========================================================
if page == "Alertas y Decisiones":
    st.markdown('<div class="card"><div class="card-title">Alertas y Decisiones</div>'
                '<div class="card-sub">Revisa los puntos clave que requieren tu atención.</div>',
                unsafe_allow_html=True)

    prod_profit = curr.groupby("Producto")[["Ventas_Soles","Utilidad_Soles"]].sum()
    prod_profit["Margen"] = np.where(
        prod_profit["Ventas_Soles"] > 0,
        prod_profit["Utilidad_Soles"]/prod_profit["Ventas_Soles"]*100,0
    )

    rows = []

    if not prod_profit.empty:
        low = prod_profit.sort_values("Margen").iloc[0]
        low_name = prod_profit.sort_values("Margen").index[0]
        if low["Margen"] < 20:
            rows.append(("!", "Bajo margen en producto", f"{low_name} tiene un margen de {low['Margen']:.1f}%. Considera revisar precio o costo.", "Atención", "red"))

        top = prod.sort_values("Ventas_Soles",ascending=False).iloc[0]
        rows.append(("✓","Buen desempeño en producto estrella",
                     f'{top["Producto"]} concentra S/ {top["Ventas_Soles"]:,.2f} en ventas.',"Positivo","green"))

    if sales_prev > 0 and sales < sales_prev:
        rows.append(("↓","Caída en ventas",
                     f"Las ventas disminuyeron {abs(d_sales):.1f}% frente al periodo anterior.","Oportunidad","orange"))
    else:
        rows.append(("↑","Crecimiento de ventas",
                     f"Las ventas crecieron {d_sales:.1f}% frente al periodo anterior.","Positivo","green"))

    for icon,title,desc,status,kind in rows:
        bg = "#FFF0F3" if kind=="red" else "#FFF7E8" if kind=="orange" else "#ECFBF5"
        fg = RED if kind=="red" else ORANGE if kind=="orange" else GREEN
        st.markdown(f"""
        <div class="alert-row">
            <div class="alert-dot" style="background:{bg};color:{fg};">{icon}</div>
            <div class="alert-main">
                <div class="alert-title">{title}</div>
                <div class="alert-desc">{desc}</div>
            </div>
            <span class="status status-{kind}">{status}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>",unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">¿Qué me dicen mis datos?</div>'
                '<div class="card-sub">Insights y recomendaciones personalizadas.</div>',
                unsafe_allow_html=True)

    top_product = prod.iloc[0]["Producto"] if not prod.empty else "—"
    top_product_sales = prod.iloc[0]["Ventas_Soles"] if not prod.empty else 0
    top_share = top_product_sales / sales * 100 if sales else 0

    insights = [
        ("◆", PURPLE, f"El producto {top_product} representa el {top_share:.1f}% de tus ventas.",
         "Es tu producto estrella. Considera proteger su stock."),
        ("↗", TEAL, "Analiza los canales con mayor crecimiento.",
         "Prioriza inversión en los canales que generan mayor retorno."),
        ("%", BLUE, f"El margen actual es {margin:.1f}%.",
         "Mantén el control de costos para proteger la rentabilidad."),
    ]

    for icon,color,title,desc in insights:
        st.markdown(f"""
        <div class="insight">
            <div class="insight-icon" style="background:{color}18;color:{color};">{icon}</div>
            <div>
                <div class="insight-title">{title}</div>
                <div class="insight-text">{desc}</div>
            </div>
            <div style="margin-left:auto;color:{color};font-size:15px;">›</div>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("</div>",unsafe_allow_html=True)

# =========================================================
# SIMULADOR
# =========================================================
if page == "Simulador":
    st.markdown('<div class="card"><div class="card-title">Simulador de Decisiones</div>'
                '<div class="card-sub">Evalúa escenarios y ve el impacto en tu negocio.</div></div>',
                unsafe_allow_html=True)

    s1,s2 = st.columns([1,1])

    with s1:
        st.markdown("### Variables")
        price_change = st.slider("Precio (%)",-30,30,0)
        quantity_change = st.slider("Cantidad vendida (%)",-50,100,0)
    with s2:
        st.markdown("### Costos y demanda")
        cost_change = st.slider("Costos (%)",-30,30,0)
        demand_change = st.slider("Demanda (%)",-20,20,0)

    demand_factor = (1+quantity_change/100)*(1+demand_change/100)
    simulated_sales = sales*(1+price_change/100)*demand_factor
    simulated_profit = (
        profit
        + sales*(demand_factor-1)*(margin/100)
        + sales*(price_change/100)*demand_factor
        - sales*demand_factor*(cost_change/100)
    )
    simulated_margin = simulated_profit/simulated_sales*100 if simulated_sales else 0

    r1,r2,r3 = st.columns(3)
    r1.metric("Ventas proyectadas",money(simulated_sales))
    r2.metric("Utilidad proyectada",money(simulated_profit))
    r3.metric("Margen proyectado",f"{simulated_margin:.1f}%")

    if simulated_profit > profit:
        st.success("El escenario simulado mejora la utilidad.")
    elif simulated_profit < profit:
        st.warning("El escenario simulado reduce la utilidad.")
    else:
        st.info("El escenario mantiene la utilidad.")

# =========================================================
# DATOS
# =========================================================
if page == "Datos":
    st.markdown('<div class="card"><div class="card-title">Datos del negocio</div>'
                '<div class="card-sub">Consulta y edita los registros utilizados por NEXDATA.</div>',
                unsafe_allow_html=True)
    edited = st.data_editor(df,use_container_width=True,num_rows="dynamic",hide_index=True)
    st.download_button(
        "Descargar datos actualizados",
        edited.to_csv(index=False).encode("utf-8"),
        "datos_nexdata.csv",
        "text/csv"
    )
    st.markdown("</div>",unsafe_allow_html=True)

# =========================================================
# INICIO / CONFIGURACIÓN
# =========================================================
if page == "Inicio":
    st.markdown('<div class="card"><div class="card-title">Bienvenido a NEXDATA</div>'
                '<div class="card-sub">Tu centro de inteligencia para convertir datos en decisiones.</div></div>',
                unsafe_allow_html=True)

if page == "Configuración":
    st.markdown('<div class="card"><div class="card-title">Configuración</div>'
                '<div class="card-sub">Preferencias generales de tu panel.</div></div>',
                unsafe_allow_html=True)
    st.info("La configuración avanzada puede incorporarse en la siguiente versión.")

st.markdown(
    '<div class="footer">NEXDATA · Inteligencia de Datos · Gestión por Resultados 2026</div>',
    unsafe_allow_html=True
)
