import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# NEXDATA — Panel de Inteligencia Empresarial
# Interfaz limpia, blanca y sencilla
# ============================================================

st.set_page_config(
    page_title="NEXDATA | Inteligencia Empresarial",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Paleta
# -----------------------------
BLUE = "#3B82F6"
GREEN = "#34C38F"
PURPLE = "#8B6ED8"
ORANGE = "#F6A23A"
CYAN = "#32B9C8"
NAVY = "#172B4D"
MUTED = "#64748B"
BORDER = "#E5EAF2"
BG = "#F8FAFC"

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: #F8FAFC;
        color: #172B4D;
    }

    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E5EAF2;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    .brand {
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 8px 0 35px 8px;
    }

    .brand-nex { color: #172B4D; }
    .brand-data { color: #3B82F6; }

    .welcome h1 {
        margin: 0;
        font-size: 30px;
        color: #172B4D;
        font-weight: 750;
    }

    .welcome p {
        margin-top: 5px;
        color: #64748B;
        font-size: 15px;
    }

    .section-title {
        color: #172B4D;
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 2px;
    }

    .section-subtitle {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 12px;
    }

    .kpi {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 18px 20px;
        min-height: 145px;
        box-shadow: 0 2px 10px rgba(23,43,77,.035);
    }

    .kpi-label {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 10px;
    }

    .kpi-value {
        color: #172B4D;
        font-size: 27px;
        font-weight: 750;
    }

    .kpi-change {
        color: #20A66A;
        font-size: 13px;
        margin-top: 8px;
    }

    .card {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 18px 20px 12px 20px;
        box-shadow: 0 2px 10px rgba(23,43,77,.035);
    }

    .mini-card {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 10px rgba(23,43,77,.035);
    }

    .alert-box {
        background: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 12px;
        padding: 13px 15px;
        margin-bottom: 10px;
    }

    .alert-title {
        font-weight: 700;
        color: #172B4D;
        font-size: 14px;
    }

    .alert-text {
        color: #64748B;
        font-size: 12px;
        margin-top: 4px;
    }

    div[data-testid="stButton"] button {
        border-radius: 9px;
        border: 1px solid #D9E2EF;
        background: #FFFFFF;
        color: #172B4D;
    }

    div[data-testid="stButton"] button:hover {
        border-color: #3B82F6;
        color: #3B82F6;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Datos
# -----------------------------
DATA_FILE = Path("dataset_mype_transacciones.csv")

@st.cache_data
def load_data():
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            return df
        except Exception:
            pass
    return pd.DataFrame()

df = load_data()

# -----------------------------
# Utilidades
# -----------------------------
def find_col(frame, names):
    lower = {str(c).lower().strip(): c for c in frame.columns}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    for c in frame.columns:
        cl = str(c).lower().strip()
        if any(name.lower() in cl for name in names):
            return c
    return None

def money(x):
    return f"S/ {x:,.2f}"

# Intentar detectar columnas del dataset
sales_col = find_col(df, ["venta", "ventas", "total_venta", "total", "ingreso", "importe"])
product_col = find_col(df, ["producto", "product"])
category_col = find_col(df, ["categoria", "categoría", "category"])
date_col = find_col(df, ["fecha", "date"])
qty_col = find_col(df, ["cantidad", "quantity", "unidades"])
profit_col = find_col(df, ["utilidad", "ganancia", "profit", "beneficio"])
channel_col = find_col(df, ["canal", "channel", "medio"])

# Valores de respaldo para que la interfaz siempre cargue
if not df.empty and sales_col:
    sales = pd.to_numeric(df[sales_col], errors="coerce").fillna(0)
    total_sales = float(sales.sum())
else:
    total_sales = 48950.00

if not df.empty and qty_col:
    quantity = pd.to_numeric(df[qty_col], errors="coerce").fillna(0)
    products_sold = int(quantity.sum())
else:
    products_sold = 1240

if not df.empty:
    clients_col = find_col(df, ["cliente", "clientes", "customer"])
    if clients_col:
        clients = int(df[clients_col].nunique())
    else:
        clients = len(df)
else:
    clients = 892

if not df.empty and profit_col:
    profit = pd.to_numeric(df[profit_col], errors="coerce").fillna(0)
    total_profit = float(profit.sum())
    margin = (total_profit / total_sales * 100) if total_sales else 0
else:
    margin = 18.4

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-nex">NEX</span><span class="brand-data">DATA</span></div>',
        unsafe_allow_html=True
    )

    menu = st.radio(
        "Navegación",
        ["Inicio", "Ventas", "Productos", "Rentabilidad", "Análisis", "Simulador"],
        label_visibility="collapsed"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        border:1px solid #E5EAF2;
        border-radius:14px;
        padding:18px;
        background:#FFFFFF;
        color:#64748B;
        font-size:13px;">
        <div style="font-size:18px;color:#3B82F6;font-weight:700;">N</div>
        <div style="margin-top:10px;">
            Tu negocio,<br>
            en mejores decisiones
        </div>
        <div style="margin-top:15px;color:#172B4D;font-weight:700;">
            NEXDATA
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
top1, top2 = st.columns([5, 1.2])

with top1:
    st.markdown("""
    <div class="welcome">
        <h1>¡Hola!</h1>
        <p>Aquí tienes un resumen del rendimiento de tu negocio.</p>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.selectbox("Negocio", ["Mi Negocio"], label_visibility="collapsed")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# -----------------------------
# KPIs
# -----------------------------
k1, k2, k3, k4 = st.columns(4)

kpis = [
    ("Ventas Totales", money(total_sales), "+12.5% vs. mes anterior", BLUE),
    ("Productos Vendidos", f"{products_sold:,}", "+8.3% vs. mes anterior", PURPLE),
    ("Clientes Atendidos", f"{clients:,}", "+15.7% vs. mes anterior", GREEN),
    ("Rentabilidad", f"{margin:.1f}%", "+4.2% vs. mes anterior", ORANGE),
]

for col, (label, value, change, accent) in zip([k1,k2,k3,k4], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi" style="border-top:3px solid {accent};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-change">↑ {change}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# -----------------------------
# Datos para gráficos
# -----------------------------
if not df.empty and product_col and sales_col:
    product_sales = (
        df.assign(_sales=pd.to_numeric(df[sales_col], errors="coerce").fillna(0))
          .groupby(product_col)["_sales"]
          .sum()
          .sort_values(ascending=False)
          .head(5)
    )
else:
    product_sales = pd.Series(
        [17500, 12500, 10500, 8200, 6500],
        index=["Producto A", "Producto B", "Producto C", "Producto D", "Producto E"]
    )

if not df.empty and category_col and sales_col:
    category_sales = (
        df.assign(_sales=pd.to_numeric(df[sales_col], errors="coerce").fillna(0))
          .groupby(category_col)["_sales"]
          .sum()
          .sort_values(ascending=False)
          .head(5)
    )
else:
    category_sales = pd.Series(
        [25500, 17500, 14500, 8500, 5200],
        index=["Alimentos", "Bebidas", "Limpieza", "Higiene", "Otros"]
    )

# -----------------------------
# Gráfico 1: Ventas por producto
# -----------------------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="card">
        <div class="section-title">Ventas por Producto</div>
        <div class="section-subtitle">Comparación de ventas por producto</div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    colors = [BLUE, GREEN, PURPLE, ORANGE, CYAN]

    for i, (name, value) in enumerate(product_sales.items()):
        fig.add_trace(go.Bar(
            x=[str(name)],
            y=[float(value)],
            marker_color=colors[i % len(colors)],
            text=[money(float(value))],
            textposition="outside",
            hovertemplate=f"{name}<br>Ventas: S/ %{{y:,.2f}}<extra></extra>"
        ))

    fig.update_layout(
        showlegend=False,
        height=310,
        margin=dict(l=10,r=10,t=15,b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=NAVY),
        yaxis=dict(
            title="Ventas (S/)",
            gridcolor="#EEF2F7",
            zeroline=False
        ),
        xaxis=dict(title="")
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Gráfico 2: Ventas por categoría
# -----------------------------
with c2:
    st.markdown("""
    <div class="card">
        <div class="section-title">Ventas por Categoría</div>
        <div class="section-subtitle">Distribución de las ventas por categoría</div>
    """, unsafe_allow_html=True)

    fig2 = go.Figure()
    for i, (name, value) in enumerate(category_sales.items()):
        fig2.add_trace(go.Bar(
            x=[str(name)],
            y=[float(value)],
            marker_color=colors[i % len(colors)],
            text=[money(float(value))],
            textposition="outside",
            hovertemplate=f"{name}<br>Ventas: S/ %{{y:,.2f}}<extra></extra>"
        ))

    fig2.update_layout(
        showlegend=False,
        height=310,
        margin=dict(l=10,r=10,t=15,b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=NAVY),
        yaxis=dict(
            title="Ventas (S/)",
            gridcolor="#EEF2F7",
            zeroline=False
        ),
        xaxis=dict(title="")
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# -----------------------------
# Fila inferior
# -----------------------------
b1, b2 = st.columns(2)

# Canales de venta
with b1:
    st.markdown("""
    <div class="card">
        <div class="section-title">Canales de Venta</div>
        <div class="section-subtitle">Distribución de las ventas según canal</div>
    """, unsafe_allow_html=True)

    if not df.empty and channel_col and sales_col:
        channel_sales = (
            df.assign(_sales=pd.to_numeric(df[sales_col], errors="coerce").fillna(0))
              .groupby(channel_col)["_sales"]
              .sum()
              .sort_values(ascending=False)
        )
    else:
        channel_sales = pd.Series(
            [25000, 14500, 10500],
            index=["Tienda física", "Delivery", "Online"]
        )

    fig3 = go.Figure()
    channel_colors = [BLUE, GREEN, PURPLE]

    for i, (name, value) in enumerate(channel_sales.items()):
        fig3.add_trace(go.Bar(
            x=[str(name)],
            y=[float(value)],
            marker_color=channel_colors[i % len(channel_colors)],
            text=[money(float(value))],
            textposition="outside",
            hovertemplate=f"{name}<br>Ventas: S/ %{{y:,.2f}}<extra></extra>"
        ))

    fig3.update_layout(
        showlegend=False,
        height=280,
        margin=dict(l=10,r=10,t=15,b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=NAVY),
        yaxis=dict(title="Ventas (S/)", gridcolor="#EEF2F7", zeroline=False),
        xaxis=dict(title="")
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# Resumen
with b2:
    st.markdown("""
    <div class="mini-card" style="min-height:330px;">
        <div style="font-size:19px;font-weight:700;color:#172B4D;">
            Resumen de la Semana
        </div>
        <div style="color:#64748B;font-size:13px;margin-top:4px;">
            Una lectura rápida de tus principales resultados.
        </div>

        <div style="margin-top:28px;padding:15px;border-radius:12px;background:#F7FBFF;">
            <div style="color:#3B82F6;font-weight:700;font-size:14px;">
                Rendimiento
            </div>
            <div style="color:#172B4D;font-size:25px;font-weight:750;margin-top:7px;">
                +12.5%
            </div>
            <div style="color:#64748B;font-size:12px;">
                crecimiento frente al periodo anterior
            </div>
        </div>

        <div style="margin-top:12px;padding:15px;border-radius:12px;background:#F7FCF9;">
            <div style="color:#20A66A;font-weight:700;font-size:14px;">
                Producto destacado
            </div>
            <div style="color:#172B4D;font-size:18px;font-weight:700;margin-top:7px;">
                {product}
            </div>
            <div style="color:#64748B;font-size:12px;">
                producto con mayor volumen de ventas
            </div>
        </div>
    </div>
    """.format(product=str(product_sales.index[0])), unsafe_allow_html=True)

# -----------------------------
# Módulos según navegación
# -----------------------------
if menu != "Inicio":
    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    if menu == "Ventas":
        st.markdown("### Ventas")
        st.info("Aquí puedes ampliar el análisis de ventas, evolución y comportamiento por periodo.")

    elif menu == "Productos":
        st.markdown("### Productos")
        st.info("Aquí puedes analizar productos más vendidos, rotación y desempeño.")

    elif menu == "Rentabilidad":
        st.markdown("### Rentabilidad")
        st.info("Aquí puedes revisar utilidad, costos y margen de cada producto.")

    elif menu == "Análisis":
        st.markdown("### Análisis")
        st.info("Aquí se concentrarán las alertas, tendencias y recomendaciones de NEXDATA.")

    elif menu == "Simulador":
        st.markdown("### Simulador")
        st.info("Modifica precio, cantidad o costos para evaluar distintos escenarios.")

# -----------------------------
# Pie
# -----------------------------
st.markdown(
    "<div style='height:25px;text-align:center;color:#94A3B8;font-size:11px;'>"
    "NEXDATA — Inteligencia de datos para negocios"
    "</div>",
    unsafe_allow_html=True
)
