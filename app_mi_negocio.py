
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="NEXDATA | Inteligencia de Datos",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

REQUIRED_COLUMNS = [
    "Fecha",
    "Producto",
    "Categoria",
    "Canal_Venta",
    "Ventas_Soles",
    "Utilidad_Soles",
]

# =========================================================
# PALETA NEXDATA
# =========================================================
NAVY = "#0B1736"
NAVY_2 = "#132451"
PURPLE = "#5B4BE7"
BLUE = "#2388F5"
TEAL = "#08B39A"
ORANGE = "#F6A43A"
PINK = "#F05D83"
GREEN = "#17B26A"
TEXT = "#172554"
MUTED = "#64748B"
BORDER = "#E5EAF3"
BG = "#F6F8FC"

PRODUCT_COLORS = [
    PURPLE, TEAL, ORANGE, PINK, BLUE, GREEN,
    "#7C5CFC", "#14B8A6", "#F97316", "#EC4899"
]

# =========================================================
# ESTILOS
# =========================================================
st.markdown(
    f"""
    <style>
        html, body, [class*="css"] {{
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}

        .stApp {{
            background: {BG};
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {NAVY} 0%, #101E46 100%);
            border-right: none;
        }}

        [data-testid="stSidebar"] * {{
            color: #EAF0FF !important;
        }}

        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stFileUploader label {{
            color: #B9C7E8 !important;
            font-size: 12px;
            font-weight: 600;
        }}

        .brand {{
            padding: 10px 8px 24px 8px;
        }}

        .brand-mark {{
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, #5B4BE7, #2388F5);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 20px;
            margin-right: 10px;
            vertical-align: middle;
        }}

        .brand-name {{
            display: inline-block;
            vertical-align: middle;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}

        .brand-name span {{
            color: #6D7CFF;
        }}

        .brand-tagline {{
            color: #B9C7E8;
            font-size: 11px;
            line-height: 1.45;
            margin: 10px 0 0 52px;
            max-width: 150px;
        }}

        .sidebar-card {{
            margin: 24px 4px 8px 4px;
            padding: 18px;
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 16px;
            background: rgba(255,255,255,.06);
        }}

        .sidebar-card-title {{
            font-size: 12px;
            font-weight: 800;
            color: #FFFFFF !important;
            margin-bottom: 6px;
        }}

        .sidebar-card-text {{
            font-size: 11px;
            line-height: 1.5;
            color: #B9C7E8 !important;
        }}

        .page-title {{
            font-size: 30px;
            font-weight: 800;
            color: {TEXT};
            letter-spacing: -1px;
            margin-bottom: 2px;
        }}

        .page-subtitle {{
            color: {MUTED};
            font-size: 14px;
            margin-bottom: 20px;
        }}

        .hero {{
            background: linear-gradient(105deg, #EEF1FF 0%, #F6F9FF 55%, #EAF5FF 100%);
            border: 1px solid #DCE5FA;
            border-radius: 18px;
            padding: 26px 30px;
            margin-bottom: 20px;
            min-height: 170px;
        }}

        .hero-title {{
            font-size: 27px;
            font-weight: 800;
            color: {NAVY};
            letter-spacing: -0.7px;
            margin-bottom: 8px;
        }}

        .hero-title span {{
            color: {PURPLE};
        }}

        .hero-text {{
            color: #43557C;
            font-size: 13px;
            line-height: 1.55;
            max-width: 620px;
        }}

        .hero-pills {{
            margin-top: 16px;
        }}

        .hero-pill {{
            display: inline-block;
            background: white;
            border: 1px solid #DCE5FA;
            border-radius: 999px;
            padding: 7px 11px;
            margin-right: 7px;
            font-size: 11px;
            color: #43557C;
        }}

        .metric-card {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 16px 17px;
            min-height: 112px;
            box-shadow: 0 5px 18px rgba(20,35,80,.04);
        }}

        .metric-label {{
            color: {MUTED};
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .3px;
        }}

        .metric-value {{
            color: {NAVY};
            font-size: 24px;
            font-weight: 800;
            margin-top: 8px;
        }}

        .metric-delta {{
            color: {GREEN};
            font-size: 11px;
            font-weight: 700;
            margin-top: 5px;
        }}

        .section-card {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 18px 18px 12px 18px;
            margin-bottom: 18px;
            box-shadow: 0 5px 18px rgba(20,35,80,.035);
        }}

        .section-title {{
            color: {NAVY};
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 2px;
        }}

        .section-caption {{
            color: {MUTED};
            font-size: 11px;
            margin-bottom: 8px;
        }}

        .insight-card {{
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 14px;
            margin-bottom: 10px;
            background: white;
        }}

        .insight-title {{
            font-size: 12px;
            font-weight: 800;
            color: {NAVY};
        }}

        .insight-text {{
            color: {MUTED};
            font-size: 11px;
            line-height: 1.5;
            margin-top: 4px;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 999px;
            font-size: 10px;
            font-weight: 700;
            margin-top: 7px;
        }}

        .badge-green {{ background: #E9F8F0; color: #087443 !important; }}
        .badge-orange {{ background: #FFF5E5; color: #A15C00 !important; }}
        .badge-red {{ background: #FFF0F2; color: #B4233F !important; }}
        .badge-blue {{ background: #EDF5FF; color: #155EAA !important; }}

        div[data-testid="stMetric"] {{
            background: white;
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 12px 14px;
            box-shadow: 0 5px 18px rgba(20,35,80,.04);
        }}

        div[data-testid="stMetricLabel"] {{
            font-size: 11px;
            font-weight: 700;
        }}

        div[data-testid="stMetricValue"] {{
            font-size: 22px;
            color: {NAVY};
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            border-bottom: 1px solid {BORDER};
        }}

        .stTabs [data-baseweb="tab"] {{
            font-size: 12px;
            font-weight: 700;
        }}

        .stButton > button {{
            border-radius: 10px;
            font-weight: 700;
        }}

        .footer {{
            color: #94A3B8;
            font-size: 10px;
            text-align: center;
            padding: 18px 0 8px 0;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# FUNCIONES
# =========================================================
@st.cache_data
def load_csv(path):
    return prepare_data(pd.read_csv(path))

def prepare_data(df):
    df = df.copy()
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Faltan estas columnas obligatorias: " + ", ".join(missing))

    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df["Ventas_Soles"] = pd.to_numeric(df["Ventas_Soles"], errors="coerce").fillna(0)
    df["Utilidad_Soles"] = pd.to_numeric(df["Utilidad_Soles"], errors="coerce").fillna(0)

    for col in ["Producto", "Categoria", "Canal_Venta"]:
        df[col] = df[col].fillna("Sin especificar").astype(str)

    return (
        df.dropna(subset=["Fecha"])
        .sort_values("Fecha")
        .reset_index(drop=True)
    )

def validate_data(df):
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]

def pct_change(current, previous):
    if previous == 0:
        return np.nan if current == 0 else np.inf
    return (current - previous) / previous * 100

def money(v):
    return f"S/ {v:,.2f}"

def make_bar(df, x, y, title=None, height=310, horizontal=False):
    if horizontal:
        fig = px.bar(
            df, x=x, y=y, orientation="h",
            color=y, color_discrete_sequence=PRODUCT_COLORS,
        )
    else:
        fig = px.bar(
            df, x=x, y=y,
            color=x, color_discrete_sequence=PRODUCT_COLORS,
        )

    fig.update_layout(
        height=height,
        title=title,
        showlegend=False,
        margin=dict(l=10, r=10, t=30 if title else 10, b=45),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", color=TEXT, size=11),
        xaxis=dict(showgrid=False, zeroline=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="#EEF1F6", zeroline=False, title=None),
        hoverlabel=dict(bgcolor=NAVY, font_size=11),
    )
    return fig

def make_line(daily):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily.index, y=daily["Ventas_Soles"],
        name="Ventas", mode="lines+markers",
        line=dict(color=PURPLE, width=3),
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=daily.index, y=daily["Utilidad_Soles"],
        name="Utilidad", mode="lines+markers",
        line=dict(color=TEAL, width=3),
        marker=dict(size=5),
    ))
    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=45),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", color=TEXT, size=11),
        legend=dict(orientation="h", y=1.08, x=0),
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="#EEF1F6", title=None),
        hovermode="x unified",
    )
    return fig

# =========================================================
# DATOS BASE
# =========================================================
try:
    df_base = load_csv("dataset_mype_transacciones.csv")
except Exception as e:
    st.error("No se pudo cargar el archivo de datos.")
    st.code(str(e))
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <span class="brand-mark">N</span>
            <span class="brand-name">NEX<span>DATA</span></span>
            <div class="brand-tagline">Conecta tus datos con mejores decisiones.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navegación")
    st.caption("ANÁLISIS")

    st.markdown(
        """
        <div style="padding:8px 10px;background:rgba(91,75,231,.35);
        border-radius:10px;font-size:12px;font-weight:700;">
        Dashboard
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("Productos y rentabilidad")
    st.markdown("Alertas y decisiones")
    st.markdown("Simulador")
    st.markdown("Datos")

    st.markdown("---")
    st.markdown("### Datos del negocio")

    uploaded = st.file_uploader(
        "Cargar Excel o CSV",
        type=["csv", "xlsx"],
        help="Puedes reemplazar los datos de demostración por los datos reales de tu negocio.",
    )

    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith(".xlsx"):
                uploaded_df = pd.read_excel(uploaded)
            else:
                uploaded_df = pd.read_csv(uploaded)

            missing = validate_data(uploaded_df)
            if missing:
                st.error("Faltan columnas: " + ", ".join(missing))
                df_source = df_base.copy()
            else:
                df_source = prepare_data(uploaded_df)
                st.success("Datos cargados correctamente.")
        except Exception as e:
            st.error(f"No se pudo leer el archivo: {e}")
            df_source = df_base.copy()
    else:
        df_source = df_base.copy()

    with st.expander("Editar datos"):
        edited_df = st.data_editor(
            df_source,
            key=f"editor_{uploaded.name if uploaded else 'demo'}",
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config={
                "Fecha": st.column_config.DateColumn("Fecha"),
                "Ventas_Soles": st.column_config.NumberColumn("Ventas (S/)", format="S/ %.2f"),
                "Utilidad_Soles": st.column_config.NumberColumn("Utilidad (S/)", format="S/ %.2f"),
            },
        )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-card-title">Tu negocio tiene datos.</div>
            <div class="sidebar-card-text">
            NEXDATA transforma información en hallazgos, alertas y decisiones accionables.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

df_raw = prepare_data(edited_df)

if df_raw.empty:
    st.warning("No hay registros válidos para analizar.")
    st.stop()

# =========================================================
# FILTROS
# =========================================================
max_date = df_raw["Fecha"].max()
min_date = df_raw["Fecha"].min()

with st.sidebar:
    st.markdown("### Filtros de análisis")
    periodo_sel = st.selectbox(
        "Periodo",
        ["Últimos 30 días", "Mes actual", "Mes anterior", "Todo el registro"],
    )

    categorias = ["Todas"] + sorted(df_raw["Categoria"].unique().tolist())
    cat_sel = st.selectbox("Categoría", categorias)

    productos_filtrados = (
        df_raw[df_raw["Categoria"] == cat_sel]["Producto"].unique().tolist()
        if cat_sel != "Todas"
        else df_raw["Producto"].unique().tolist()
    )
    prod_sel = st.selectbox("Producto", ["Todos"] + sorted(productos_filtrados))

    canales = ["Todos"] + sorted(df_raw["Canal_Venta"].unique().tolist())
    canal_sel = st.selectbox("Canal de venta", canales)

if periodo_sel == "Últimos 30 días":
    fecha_fin = max_date
    fecha_inicio = max_date - pd.Timedelta(days=29)
    dias = 30
elif periodo_sel == "Mes actual":
    fecha_inicio = max_date.replace(day=1)
    fecha_fin = max_date
    dias = (fecha_fin - fecha_inicio).days + 1
elif periodo_sel == "Mes anterior":
    primer_dia = max_date.replace(day=1)
    fecha_fin = primer_dia - pd.Timedelta(days=1)
    fecha_inicio = fecha_fin.replace(day=1)
    dias = (fecha_fin - fecha_inicio).days + 1
else:
    fecha_inicio = min_date
    fecha_fin = max_date
    dias = (fecha_fin - fecha_inicio).days + 1

fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
fecha_inicio_prev = fecha_fin_prev - pd.Timedelta(days=dias - 1)

def filter_df(df, start, end, category="Todas", product="Todos", channel="Todos"):
    out = df[(df["Fecha"] >= start) & (df["Fecha"] <= end)].copy()
    if category != "Todas":
        out = out[out["Categoria"] == category]
    if product != "Todos":
        out = out[out["Producto"] == product]
    if channel != "Todos":
        out = out[out["Canal_Venta"] == channel]
    return out

df_curr = filter_df(df_raw, fecha_inicio, fecha_fin, cat_sel, prod_sel, canal_sel)
df_prev = filter_df(df_raw, fecha_inicio_prev, fecha_fin_prev, cat_sel, prod_sel, canal_sel)

if df_curr.empty:
    st.warning("No existen datos para los filtros seleccionados.")
    st.stop()

# =========================================================
# KPIs
# =========================================================
ventas = df_curr["Ventas_Soles"].sum()
ventas_prev = df_prev["Ventas_Soles"].sum()
utilidad = df_curr["Utilidad_Soles"].sum()
utilidad_prev = df_prev["Utilidad_Soles"].sum()
margen = utilidad / ventas * 100 if ventas else 0
margen_prev = utilidad_prev / ventas_prev * 100 if ventas_prev else 0
transacciones = len(df_curr)
transacciones_prev = len(df_prev)
ticket = ventas / transacciones if transacciones else 0
ticket_prev = ventas_prev / transacciones_prev if transacciones_prev else 0

delta_ventas = pct_change(ventas, ventas_prev)
delta_utilidad = pct_change(utilidad, utilidad_prev)
delta_transacciones = pct_change(transacciones, transacciones_prev)
delta_ticket = pct_change(ticket, ticket_prev)
delta_margen = margen - margen_prev

# =========================================================
# ENCABEZADO
# =========================================================
st.markdown('<div class="page-title">Hola, bienvenida a NEXDATA</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Aquí tienes un resumen del rendimiento de tu negocio.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Convierte tus datos en <span>oportunidades</span></div>
        <div class="hero-text">
            Analiza el rendimiento de tu negocio, identifica oportunidades de mejora
            y toma decisiones con mayor confianza.
        </div>
        <div class="hero-pills">
            <span class="hero-pill">Análisis en tiempo real</span>
            <span class="hero-pill">Alertas automáticas</span>
            <span class="hero-pill">Recomendaciones</span>
            <span class="hero-pill">Simulador de escenarios</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# KPIs
# =========================================================
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Ventas totales", money(ventas), f"{delta_ventas:.1f}%" if np.isfinite(delta_ventas) else "Nuevo periodo")
k2.metric("Utilidad neta", money(utilidad), f"{delta_utilidad:.1f}%" if np.isfinite(delta_utilidad) else "Nuevo periodo")
k3.metric("Margen de utilidad", f"{margen:.1f}%", f"{delta_margen:.1f} pp")
k4.metric("N.º de ventas", f"{transacciones:,}", f"{delta_transacciones:.1f}%" if np.isfinite(delta_transacciones) else "Nuevo periodo")
k5.metric("Ticket promedio", money(ticket), f"{delta_ticket:.1f}%" if np.isfinite(delta_ticket) else "Nuevo periodo")

st.caption(
    f"Periodo analizado: {fecha_inicio.strftime('%d/%m/%Y')} – "
    f"{fecha_fin.strftime('%d/%m/%Y')} · {len(df_curr):,} registros"
)

# =========================================================
# PESTAÑAS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Dashboard",
        "Productos y rentabilidad",
        "Alertas y decisiones",
        "Simulador",
        "Datos",
    ]
)

# =========================================================
# TAB 1
# =========================================================
with tab1:
    st.markdown(
        '<div class="section-card"><div class="section-title">Evolución de ventas y utilidad</div>'
        '<div class="section-caption">Comportamiento del periodo seleccionado</div>',
        unsafe_allow_html=True,
    )

    daily = (
        df_curr.groupby(df_curr["Fecha"].dt.date)[["Ventas_Soles", "Utilidad_Soles"]]
        .sum()
        .sort_index()
    )
    st.plotly_chart(make_line(daily), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        channel_sales = (
            df_curr.groupby("Canal_Venta")["Ventas_Soles"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        st.markdown(
            '<div class="section-card"><div class="section-title">Ventas por canal</div>'
            '<div class="section-caption">Distribución de ingresos según canal</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            make_bar(channel_sales, "Canal_Venta", "Ventas_Soles", height=290),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        category_sales = (
            df_curr.groupby("Categoria")["Ventas_Soles"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        st.markdown(
            '<div class="section-card"><div class="section-title">Ventas por categoría</div>'
            '<div class="section-caption">Categorías con mayor facturación</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            make_bar(category_sales, "Categoria", "Ventas_Soles", height=290),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2
# =========================================================
with tab2:
    prod_sales = (
        df_curr.groupby("Producto")["Ventas_Soles"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    prod_profit = df_curr.groupby("Producto")[["Ventas_Soles", "Utilidad_Soles"]].sum()
    prod_profit["Margen_%"] = np.where(
        prod_profit["Ventas_Soles"] > 0,
        prod_profit["Utilidad_Soles"] / prod_profit["Ventas_Soles"] * 100,
        0,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            '<div class="section-card"><div class="section-title">Ventas por producto</div>'
            '<div class="section-caption">Cada producto se muestra con un color diferente</div>',
            unsafe_allow_html=True,
        )
        fig = make_bar(prod_sales.head(10), "Producto", "Ventas_Soles", height=360)
        fig.update_traces(texttemplate="S/ %{y:,.0f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        margin_chart = (
            prod_profit["Margen_%"]
            .sort_values(ascending=False)
            .reset_index()
        )
        st.markdown(
            '<div class="section-card"><div class="section-title">Margen por producto</div>'
            '<div class="section-caption">Rentabilidad relativa de cada producto</div>',
            unsafe_allow_html=True,
        )
        fig2 = make_bar(margin_chart.head(10), "Producto", "Margen_%", height=360)
        fig2.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-card"><div class="section-title">Tabla de rentabilidad</div>'
        '<div class="section-caption">Comparación de ventas, utilidad, margen y participación</div>',
        unsafe_allow_html=True,
    )

    table = prod_profit.copy()
    table["Participación_Ventas_%"] = np.where(
        ventas > 0, table["Ventas_Soles"] / ventas * 100, 0
    )
    table = table.sort_values("Ventas_Soles", ascending=False)

    st.dataframe(
        table.style.format({
            "Ventas_Soles": "S/ {:,.2f}",
            "Utilidad_Soles": "S/ {:,.2f}",
            "Margen_%": "{:.1f}%",
            "Participación_Ventas_%": "{:.1f}%",
        }),
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 3
# =========================================================
with tab3:
    st.markdown(
        '<div class="section-card"><div class="section-title">¿Qué me dicen mis datos?</div>'
        '<div class="section-caption">Hallazgos generados automáticamente a partir del periodo seleccionado</div>',
        unsafe_allow_html=True,
    )

    prod_sales_series = df_curr.groupby("Producto")["Ventas_Soles"].sum().sort_values(ascending=False)
    margin_series = prod_profit["Margen_%"].sort_values(ascending=False)
    channel_series = df_curr.groupby("Canal_Venta")["Ventas_Soles"].sum().sort_values(ascending=False)

    if margen < margen_prev - 1:
        st.markdown(
            f'<div class="insight-card"><div class="insight-title">Rentabilidad en observación</div>'
            f'<div class="insight-text">El margen actual es {margen:.1f}%, frente a {margen_prev:.1f}% en el periodo anterior. '
            f'Conviene revisar costos y precios.</div><span class="badge badge-red">Atención</span></div>',
            unsafe_allow_html=True,
        )
    elif margen > margen_prev + 1:
        st.markdown(
            f'<div class="insight-card"><div class="insight-title">Mejora de rentabilidad</div>'
            f'<div class="insight-text">El margen subió a {margen:.1f}%. Identifica los productos o canales que explican la mejora.</div>'
            f'<span class="badge badge-green">Positivo</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="insight-card"><div class="insight-title">Margen estable</div>'
            f'<div class="insight-text">La rentabilidad se mantiene alrededor de {margen:.1f}%.</div>'
            f'<span class="badge badge-blue">Estable</span></div>',
            unsafe_allow_html=True,
        )

    if not prod_sales_series.empty:
        top_product = prod_sales_series.index[0]
        top_share = prod_sales_series.iloc[0] / ventas * 100 if ventas else 0
        st.markdown(
            f'<div class="insight-card"><div class="insight-title">Producto líder</div>'
            f'<div class="insight-text"><b>{top_product}</b> concentra aproximadamente {top_share:.1f}% de las ventas.</div>'
            f'<span class="badge badge-green">Oportunidad</span></div>',
            unsafe_allow_html=True,
        )

    if not margin_series.empty:
        best_margin_product = margin_series.index[0]
        best_margin = margin_series.iloc[0]
        st.markdown(
            f'<div class="insight-card"><div class="insight-title">Mayor margen</div>'
            f'<div class="insight-text"><b>{best_margin_product}</b> presenta un margen aproximado de {best_margin:.1f}%.</div>'
            f'<span class="badge badge-blue">Rentabilidad</span></div>',
            unsafe_allow_html=True,
        )

    if not channel_series.empty:
        best_channel = channel_series.index[0]
        channel_share = channel_series.iloc[0] / ventas * 100 if ventas else 0
        st.markdown(
            f'<div class="insight-card"><div class="insight-title">Canal principal</div>'
            f'<div class="insight-text"><b>{best_channel}</b> representa aproximadamente {channel_share:.1f}% de las ventas.</div>'
            f'<span class="badge badge-blue">Desempeño</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-card"><div class="section-title">Acciones recomendadas</div>'
        '<div class="section-caption">Sugerencias basadas en los indicadores seleccionados</div>',
        unsafe_allow_html=True,
    )

    recommendations = []
    if margen < margen_prev:
        recommendations.append("Revisar costos y precios de los productos con mayor volumen de ventas.")
    if ticket < 40:
        recommendations.append("Probar combos o ventas cruzadas para elevar el ticket promedio.")
    if not prod_sales_series.empty:
        recommendations.append(
            f"Proteger el stock y disponibilidad de {prod_sales_series.index[0]}, "
            "porque es el producto con mayor facturación."
        )
    if not margin_series.empty:
        recommendations.append(
            f"Evaluar promociones para {margin_series.index[0]}, "
            "que presenta el mayor margen."
        )

    if not recommendations:
        recommendations.append("Mantener seguimiento periódico de ventas, margen y ticket promedio.")

    for i, rec in enumerate(recommendations, 1):
        st.write(f"**{i}.** {rec}")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 4
# =========================================================
with tab4:
    st.markdown(
        '<div class="section-card"><div class="section-title">Simulador de decisiones</div>'
        '<div class="section-caption">Evalúa cómo podrían cambiar ventas y utilidad antes de tomar una decisión</div>',
        unsafe_allow_html=True,
    )

    s1, s2 = st.columns(2)

    with s1:
        precio_factor = st.slider("Variación del precio (%)", -30, 30, 0, 1)
        ventas_factor = st.slider("Variación de cantidad vendida (%)", -50, 100, 0, 5)

    with s2:
        costo_factor = st.slider("Variación de costos (%)", -30, 30, 0, 1)
        otros_factor = st.slider("Ajuste adicional de demanda (%)", -20, 20, 0, 1)

    demanda_total = (1 + ventas_factor / 100) * (1 + otros_factor / 100)
    ventas_sim = ventas * (1 + precio_factor / 100) * demanda_total
    utilidad_sim = (
        utilidad
        + ventas * (demanda_total - 1) * (margen / 100)
        + ventas * (precio_factor / 100) * demanda_total
        - ventas * demanda_total * (costo_factor / 100)
    )
    margen_sim = utilidad_sim / ventas_sim * 100 if ventas_sim else 0

    r1, r2, r3 = st.columns(3)
    r1.metric("Ventas proyectadas", money(ventas_sim), money(ventas_sim - ventas))
    r2.metric("Utilidad proyectada", money(utilidad_sim), money(utilidad_sim - utilidad))
    r3.metric("Margen proyectado", f"{margen_sim:.1f}%", f"{margen_sim - margen:.1f} pp")

    if utilidad_sim > utilidad:
        st.success("El escenario simulado mejora la utilidad respecto al escenario actual.")
    elif utilidad_sim < utilidad:
        st.warning("El escenario simulado reduce la utilidad. Revisa las variables antes de tomar una decisión.")
    else:
        st.info("El escenario simulado mantiene la utilidad.")

    comparison = pd.DataFrame({
        "Escenario": ["Actual", "Simulado"],
        "Ventas": [ventas, ventas_sim],
        "Utilidad": [utilidad, utilidad_sim],
        "Margen": [margen, margen_sim],
    }).set_index("Escenario")

    st.dataframe(
        comparison.style.format({
            "Ventas": "S/ {:,.2f}",
            "Utilidad": "S/ {:,.2f}",
            "Margen": "{:.1f}%",
        }),
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 5
# =========================================================
with tab5:
    st.markdown(
        '<div class="section-card"><div class="section-title">Datos del negocio</div>'
        '<div class="section-caption">Edita los registros y descarga una copia actualizada</div>',
        unsafe_allow_html=True,
    )

    edited_df_main = st.data_editor(
        df_raw,
        key="editor_principal",
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha"),
            "Ventas_Soles": st.column_config.NumberColumn("Ventas (S/)", format="S/ %.2f"),
            "Utilidad_Soles": st.column_config.NumberColumn("Utilidad (S/)", format="S/ %.2f"),
        },
    )

    st.download_button(
        "Descargar datos actuales en CSV",
        data=edited_df_main.to_csv(index=False).encode("utf-8"),
        file_name="datos_nexdata_actualizados.csv",
        mime="text/csv",
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PIE
# =========================================================
st.markdown(
    '<div class="footer">NEXDATA · Inteligencia de Datos · Gestión por Resultados 2026</div>',
    unsafe_allow_html=True,
)
