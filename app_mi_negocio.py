import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(
    page_title="NexData – Inteligencia Empresarial MYPE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force Light Theme & Custom CSS for High Contrast and Zero White Text
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0B1220 !important;
        background-color: #F8FAFC !important;
    }
    
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {
        color: #0B1220 !important;
    }

    div[data-testid="stRadio"] > div {
        gap: 6px;
    }
    div[data-testid="stRadio"] label {
        background-color: #F1F5F9 !important;
        color: #0B1220 !important;
        padding: 10px 16px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border: 1px solid #E2E8F0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: #E2E8F0 !important;
        color: #00C2D1 !important;
    }
    
    .greeting-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 2px;
    }
    .greeting-title span {
        color: #0284C7;
    }
    .greeting-sub {
        font-size: 15px;
        color: #6B7686;
        margin-bottom: 25px;
    }

    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .kpi-icon-box {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 18px;
    }
    .icon-blue { background-color: #E0F2FE; color: #0284C7; }
    .icon-purple { background-color: #F3E8FF; color: #8B5CF6; }
    .icon-green { background-color: #D1FAE5; color: #10B981; }
    .icon-orange { background-color: #FFEDD5; color: #F97316; }

    .kpi-label {
        font-size: 13px;
        font-weight: 600;
        color: #6B7686;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #0B1220;
        margin: 4px 0;
    }
    .kpi-delta-pos {
        font-size: 12px;
        font-weight: 700;
        color: #059669;
    }

    .section-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
        margin-bottom: 20px;
    }
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 17px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 4px;
    }
    .section-sub {
        font-size: 12px;
        color: #6B7686;
        margin-bottom: 15px;
    }

    .alert-orange {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-orange-title {
        font-weight: 700;
        color: #B45309;
        font-size: 13px;
        margin-bottom: 4px;
    }
    .alert-orange-desc {
        color: #78350F;
        font-size: 12px;
    }

    .alert-green {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 10px;
        padding: 14px;
    }
    .alert-green-title {
        font-weight: 700;
        color: #047857;
        font-size: 13px;
        margin-bottom: 4px;
    }
    .alert-green-desc {
        color: #064E3B;
        font-size: 12px;
    }

    .stDataFrame, div[data-testid="stTable"] {
        color: #0B1220 !important;
    }
</style>
""", unsafe_allow_html=True)

# Logo NexData SVG
logo_svg = """
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px; padding: 5px;">
    <svg width="42" height="42" viewBox="0 0 100 100" fill="none">
        <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
        <circle cx="30" cy="75" r="7" fill="#6B7686"/>
        <circle cx="55" cy="55" r="7" fill="#6B7686"/>
        <line x1="30" y1="75" x2="55" y2="55" stroke="#00C2D1" stroke-width="7" stroke-linecap="round"/>
        <line x1="55" y1="55" x2="78" y2="28" stroke="#00C2D1" stroke-width="7" stroke-linecap="round"/>
        <circle cx="78" cy="28" r="9" fill="#6C5CE7"/>
        <path d="M70 20 L86 20 L86 36" stroke="#6C5CE7" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; line-height: 1; color: #0B1220;">
            Nex<span style="color: #00C2D1;">Data</span>
        </div>
        <div style="font-size: 11px; color: #6B7686; font-weight: 500; margin-top: 3px;">
            Datos claros para tu negocio
        </div>
    </div>
</div>
"""
st.sidebar.markdown(logo_svg, unsafe_allow_html=True)

st.sidebar.markdown('<div style="font-size: 12px; font-weight: 700; color: #6B7686; margin-bottom: 8px; text-transform: uppercase;">Navegación</div>', unsafe_allow_html=True)

menu_opt = st.sidebar.radio(
    "",
    ["01. Inicio", "02. Ventas", "03. Productos", "04. Rentabilidad", "05. Análisis", "06. Simulador"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown('<div style="font-size: 12px; font-weight: 700; color: #6B7686; margin-bottom: 8px; text-transform: uppercase;">Carga de Datos</div>', unsafe_allow_html=True)

demo_mode = st.sidebar.checkbox("Usar datos de prueba (Demo MYPE)", value=True)
uploaded_file = st.sidebar.file_uploader("Sube tu archivo (.csv o .xlsx)", type=["csv", "xlsx"])

@st.cache_data
def load_default_data():
    dates = pd.date_range(start="2026-04-01", periods=30, freq="D")
    categories = ["Alimentos", "Bebidas", "Limpieza", "Higiene", "Otros"]
    products = {
        "Alimentos": ["Arroz 1kg", "Aceite 1L", "Fideos 500g", "Galletas Pack", "Azúcar 1kg"],
        "Bebidas": ["Gaseosa 1.5L", "Agua Mineral 600ml", "Jugo Naranja 1L", "Cerveza 620ml"],
        "Limpieza": ["Detergente 800g", "Lavavajillas 500ml", "Lejía 1L"],
        "Higiene": ["Jabón de Tocador", "Shampoo 400ml", "Crema Dental"],
        "Otros": ["Pilas AA", "Fósforos Pack"]
    }
    channels = ["Tienda física", "Delivery", "Online", "Otros"]
    
    np.random.seed(42)
    records = []
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(25, 45)
        for _ in range(num_tx):
            tx_id += 1
            cat = np.random.choice(categories, p=[0.33, 0.25, 0.18, 0.13, 0.11])
            prod = np.random.choice(products[cat])
            chan = np.random.choice(channels, p=[0.45, 0.30, 0.15, 0.10])
            qty = np.random.randint(1, 6)
            unit_price = np.random.uniform(3.5, 28.0)
            cost_ratio = np.random.uniform(0.60, 0.80)
            sales = qty * unit_price
            cost = sales * cost_ratio
            profit = sales - cost
            records.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": d,
                "Dia_Semana": d.strftime("%A"),
                "Categoria": cat,
                "Producto": prod,
                "Canal_Venta": chan,
                "Cantidad": qty,
                "Precio_Unitario": round(unit_price, 2),
                "Ventas_Soles": round(sales, 2),
                "Costo_Soles": round(cost, 2),
                "Utilidad_Soles": round(profit, 2)
            })
    df = pd.DataFrame(records)
    return df

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
        df_raw["Fecha"] = pd.to_datetime(df_raw["Fecha"])
    except Exception as e:
        st.error("Error al procesar el archivo. Cargando dataset de prueba.")
        df_raw = load_default_data()
elif demo_mode:
    df_raw = load_default_data()
else:
    df_raw = None

if df_raw is None:
    st.markdown('''
    <div style="background-color: #FFFFFF; border: 2px dashed #CBD5E1; border-radius: 16px; padding: 50px; text-align: center; margin-top: 40px;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; color: #0B1220; margin-bottom: 10px;">
            Sube tus datos para comenzar
        </div>
        <div style="font-size: 15px; color: #6B7686; max-width: 500px; margin: 0 auto 20px auto;">
            Sube tu registro de ventas en CSV o Excel en la barra lateral, o marca la casilla "Usar datos de prueba" para explorar la plataforma en vivo.
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.stop()

df_curr = df_raw.copy()

def apply_plotly_style(fig, title_text=""):
    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(family="Space Grotesk, sans-serif", size=16, color="#0B1220")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#0B1220", size=12),
        margin=dict(l=30, r=30, t=40, b=30),
        xaxis=dict(
            title_font=dict(color="#0B1220", size=12),
            tickfont=dict(color="#0B1220", size=11),
            gridcolor="#E2E8F0",
            zerolinecolor="#E2E8F0"
        ),
        yaxis=dict(
            title_font=dict(color="#0B1220", size=12),
            tickfont=dict(color="#0B1220", size=11),
            gridcolor="#E2E8F0",
            zerolinecolor="#E2E8F0"
        ),
        legend=dict(
            font=dict(color="#0B1220", size=11)
        )
    )
    return fig

# ---------------------------------------------------------
# PESTAÑA 01: INICIO
# ---------------------------------------------------------
if menu_opt == "01. Inicio":
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown('''
        <div class="greeting-title">¡Hola, <span>Milagros!</span></div>
        <div class="greeting-sub">Aquí tienes un resumen del rendimiento de tu negocio.</div>
        ''', unsafe_allow_html=True)
    with col_h2:
        st.selectbox("", ["Últimos 30 días", "Este Mes", "Mes Anterior"], index=0)

    k1, k2, k3, k4 = st.columns(4)
    vtas_tot = df_curr["Ventas_Soles"].sum()
    prod_tot = df_curr["Cantidad"].sum()
    cli_tot = len(df_curr["ID_Transaccion"].unique())
    util_tot = df_curr["Utilidad_Soles"].sum()
    mg_pct = (util_tot / vtas_tot * 100) if vtas_tot > 0 else 0

    with k1:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box icon-blue">🛒</div>
                <div class="kpi-label">Ventas Totales</div>
            </div>
            <div class="kpi-value">S/ {vtas_tot:,.0f}</div>
            <div class="kpi-delta-pos">▲ +12.5% vs. mes anterior</div>
        </div>
        ''', unsafe_allow_html=True)

    with k2:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box icon-purple">📦</div>
                <div class="kpi-label">Productos Vendidos</div>
            </div>
            <div class="kpi-value">{prod_tot:,}</div>
            <div class="kpi-delta-pos">▲ +8.3% vs. mes anterior</div>
        </div>
        ''', unsafe_allow_html=True)

    with k3:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box icon-green">👤</div>
                <div class="kpi-label">Clientes Atendidos</div>
            </div>
            <div class="kpi-value">{cli_tot:,}</div>
            <div class="kpi-delta-pos">▲ +15.7% vs. mes anterior</div>
        </div>
        ''', unsafe_allow_html=True)

    with k4:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box icon-orange">💰</div>
                <div class="kpi-label">Rentabilidad</div>
            </div>
            <div class="kpi-value">{mg_pct:.1f}%</div>
            <div class="kpi-delta-pos">▲ +4.2% vs. mes anterior</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cg1, cg2 = st.columns([1.6, 1])

    with cg1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Evolución de Ventas</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Ventas diarias en los últimos 30 días</div>', unsafe_allow_html=True)
        
        df_daily = df_curr.groupby(df_curr["Fecha"].dt.date)["Ventas_Soles"].sum().reset_index()
        fig_evo = go.Figure()
        fig_evo.add_trace(go.Scatter(
            x=df_daily["Fecha"],
            y=df_daily["Ventas_Soles"],
            mode="lines+markers",
            line=dict(color="#0284C7", width=3, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(2, 132, 199, 0.08)",
            marker=dict(size=6, color="#0284C7")
        ))
        apply_plotly_style(fig_evo)
        fig_evo.update_layout(height=280)
        st.plotly_chart(fig_evo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cg2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Ventas por Categoría</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Distribución de ventas por categoría</div>', unsafe_allow_html=True)
        
        df_cat = df_curr.groupby("Categoria")["Ventas_Soles"].sum().reset_index()
        fig_cat = go.Figure(data=[go.Pie(
            labels=df_cat["Categoria"],
            values=df_cat["Ventas_Soles"],
            hole=0.65,
            marker=dict(colors=["#0284C7", "#8B5CF6", "#10B981", "#F97316", "#EC4899"]),
            textinfo="percent",
            insidetextfont=dict(color="#0B1220", size=11)
        )])
        fig_cat.add_annotation(
            text=f"S/ {vtas_tot:,.0f}<br><span style='font-size:11px; color:#6B7686;'>Total ventas</span>",
            x=0.5, y=0.5, font=dict(size=15, color="#0B1220", family="Space Grotesk"), showarrow=False
        )
        apply_plotly_style(fig_cat)
        fig_cat.update_layout(height=280, showlegend=True)
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c_b1, c_b2, c_b3 = st.columns([1, 1, 1.2])

    with c_b1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Productos Más Vendidos</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Top 5 por volumen de ventas</div>', unsafe_allow_html=True)
        
        df_top = df_curr.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(5).reset_index()
        fig_top = go.Figure(go.Bar(
            x=df_top["Cantidad"],
            y=df_top["Producto"],
            orientation="h",
            marker=dict(color=["#0284C7", "#10B981", "#8B5CF6", "#F97316", "#00C2D1"]),
            text=df_top["Cantidad"].apply(lambda x: f"{x} un."),
            textposition="outside",
            textfont=dict(color="#0B1220", size=11)
        ))
        apply_plotly_style(fig_top)
        fig_top.update_layout(height=240, yaxis=dict(autorange="reverse"))
        st.plotly_chart(fig_top, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_b2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Canales de Venta</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Participación por canal</div>', unsafe_allow_html=True)
        
        df_chan = df_curr.groupby("Canal_Venta")["Ventas_Soles"].sum().reset_index()
        fig_chan = go.Figure(go.Pie(
            labels=df_chan["Canal_Venta"],
            values=df_chan["Ventas_Soles"],
            marker=dict(colors=["#0284C7", "#10B981", "#8B5CF6", "#F97316"]),
            textinfo="percent+label",
            textfont=dict(color="#0B1220", size=10)
        ))
        apply_plotly_style(fig_chan)
        fig_chan.update_layout(height=240, showlegend=False)
        st.plotly_chart(fig_chan, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_b3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Alertas y Recomendaciones</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Detección automática de patrones</div>', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="alert-orange">
            <div class="alert-orange-title">⚠️ Producto con baja rotación</div>
            <div class="alert-orange-desc">El producto "Galletas Pack" ha disminuido su venta en un 35% en comparación con el mes anterior.</div>
        </div>
        <div class="alert-green">
            <div class="alert-green-title">🎯 Oportunidad de crecimiento</div>
            <div class="alert-green-desc">La categoría de Bebidas muestra una tendencia al alza. Considera aumentar el stock en fin de semana.</div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 02: VENTAS
# ---------------------------------------------------------
elif menu_opt == "02. Ventas":
    st.markdown('<div class="greeting-title">Análisis Detallado de <span>Ventas</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="greeting-sub">Exploración de patrones temporales, canales e historial de transacciones.</div>', unsafe_allow_html=True)

    v1, v2 = st.columns(2)
    with v1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Ventas por Día de la Semana</div>', unsafe_allow_html=True)
        
        df_dow = df_curr.groupby("Dia_Semana")["Ventas_Soles"].sum().reset_index()
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        df_dow["Dia_Semana"] = pd.Categorical(df_dow["Dia_Semana"], categories=dow_order, ordered=True)
        df_dow = df_dow.sort_values("Dia_Semana")
        
        fig_dow = go.Figure(go.Bar(
            x=["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
            y=df_dow["Ventas_Soles"],
            marker=dict(color="#0284C7"),
            text=df_dow["Ventas_Soles"].apply(lambda x: f"S/ {x:,.0f}"),
            textposition="outside",
            textfont=dict(color="#0B1220", size=11)
        ))
        apply_plotly_style(fig_dow)
        fig_dow.update_layout(height=320)
        st.plotly_chart(fig_dow, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with v2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Distribución del Monto por Ticket</div>', unsafe_allow_html=True)
        
        fig_hist = go.Figure(go.Histogram(
            x=df_curr["Ventas_Soles"],
            nbinsx=15,
            marker=dict(color="#8B5CF6", line=dict(color="#0B1220", width=1))
        ))
        apply_plotly_style(fig_hist)
        fig_hist.update_layout(height=320, xaxis_title="Monto del Ticket (S/)", yaxis_title="Frecuencia")
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Historial de Transacciones Registradas</div>', unsafe_allow_html=True)
    st.dataframe(df_curr[["ID_Transaccion", "Fecha", "Producto", "Categoria", "Canal_Venta", "Cantidad", "Precio_Unitario", "Ventas_Soles", "Utilidad_Soles"]], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 03: PRODUCTOS
# ---------------------------------------------------------
elif menu_opt == "03. Productos":
    st.markdown('<div class="greeting-title">Rendimiento de <span>Productos</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="greeting-sub">Ranking de facturación, volumen y matriz de rotación de catálogo.</div>', unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Top 10 Productos por Facturación (S/)</div>', unsafe_allow_html=True)
        
        df_p_rev = df_curr.groupby("Producto")["Ventas_Soles"].sum().sort_values(ascending=False).head(10).reset_index()
        fig_p_rev = go.Figure(go.Bar(
            x=df_p_rev["Ventas_Soles"],
            y=df_p_rev["Producto"],
            orientation="h",
            marker=dict(color="#00C2D1"),
            text=df_p_rev["Ventas_Soles"].apply(lambda x: f"S/ {x:,.0f}"),
            textposition="outside",
            textfont=dict(color="#0B1220", size=10)
        ))
        apply_plotly_style(fig_p_rev)
        fig_p_rev.update_layout(height=360, yaxis=dict(autorange="reverse"))
        st.plotly_chart(fig_p_rev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Matriz de Rotación (Precio vs. Demanda)</div>', unsafe_allow_html=True)
        
        df_scat = df_curr.groupby("Producto").agg({
            "Precio_Unitario": "mean",
            "Cantidad": "sum",
            "Ventas_Soles": "sum"
        }).reset_index()
        
        fig_scat = go.Figure(go.Scatter(
            x=df_scat["Precio_Unitario"],
            y=df_scat["Cantidad"],
            mode="markers+text",
            text=df_scat["Producto"],
            textposition="top center",
            textfont=dict(color="#0B1220", size=10),
            marker=dict(size=df_scat["Ventas_Soles"]/30, color="#6C5CE7", opacity=0.8)
        ))
        apply_plotly_style(fig_scat)
        fig_scat.update_layout(height=360, xaxis_title="Precio Promedio (S/)", yaxis_title="Unidades Vendidas")
        st.plotly_chart(fig_scat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 04: RENTABILIDAD
# ---------------------------------------------------------
elif menu_opt == "04. Rentabilidad":
    st.markdown('<div class="greeting-title">Análisis de <span>Rentabilidad</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="greeting-sub">Estructura de costos, margen de utilidad por categoría y retorno por producto.</div>', unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Margen de Utilidad (%) por Categoría</div>', unsafe_allow_html=True)
        
        df_mg = df_curr.groupby("Categoria").agg({
            "Ventas_Soles": "sum",
            "Utilidad_Soles": "sum"
        }).reset_index()
        df_mg["Margen_Pct"] = (df_mg["Utilidad_Soles"] / df_mg["Ventas_Soles"] * 100).round(1)
        
        fig_mg = go.Figure(go.Bar(
            x=df_mg["Categoria"],
            y=df_mg["Margen_Pct"],
            marker=dict(color="#10B981"),
            text=df_mg["Margen_Pct"].apply(lambda x: f"{x}%"),
            textposition="outside",
            textfont=dict(color="#0B1220", size=11)
        ))
        apply_plotly_style(fig_mg)
        fig_mg.update_layout(height=340, yaxis_title="Margen (%)")
        st.plotly_chart(fig_mg, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Relación Ventas vs. Utilidad Neta</div>', unsafe_allow_html=True)
        
        df_pu = df_curr.groupby("Producto").agg({
            "Ventas_Soles": "sum",
            "Utilidad_Soles": "sum"
        }).reset_index()
        
        fig_pu = go.Figure(go.Scatter(
            x=df_pu["Ventas_Soles"],
            y=df_pu["Utilidad_Soles"],
            mode="markers+text",
            text=df_pu["Producto"],
            textposition="bottom right",
            textfont=dict(color="#0B1220", size=10),
            marker=dict(size=10, color="#0284C7")
        ))
        apply_plotly_style(fig_pu)
        fig_pu.update_layout(height=340, xaxis_title="Ventas Totales (S/)", yaxis_title="Utilidad Neta (S/)")
        st.plotly_chart(fig_pu, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 05: ANÁLISIS
# ---------------------------------------------------------
elif menu_opt == "05. Análisis":
    st.markdown('<div class="greeting-title">Inteligencia Avanzada de <span>Análisis</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="greeting-sub">Cruce multidimensional de canales, categorías y comportamiento del consumidor.</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Mapa de Calor (Canal vs. Categoría)</div>', unsafe_allow_html=True)
        
        pivot_hm = df_curr.pivot_table(index="Categoria", columns="Canal_Venta", values="Ventas_Soles", aggfunc="sum").fillna(0)
        
        fig_hm = go.Figure(go.Heatmap(
            z=pivot_hm.values,
            x=pivot_hm.columns,
            y=pivot_hm.index,
            colorscale="Blues",
            texttemplate="S/ %{z:,.0f}",
            textfont=dict(color="#0B1220", size=11)
        ))
        apply_plotly_style(fig_hm)
        fig_hm.update_layout(height=350)
        st.plotly_chart(fig_hm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with a2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Estructura de Ingresos vs. Costos</div>', unsafe_allow_html=True)
        
        df_stack = df_curr.groupby("Categoria").agg({
            "Costo_Soles": "sum",
            "Utilidad_Soles": "sum"
        }).reset_index()
        
        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(name="Costo Operativo", x=df_stack["Categoria"], y=df_stack["Costo_Soles"], marker_color="#6B7686"))
        fig_stack.add_trace(go.Bar(name="Utilidad Neta", x=df_stack["Categoria"], y=df_stack["Utilidad_Soles"], marker_color="#00C2D1"))
        apply_plotly_style(fig_stack)
        fig_stack.update_layout(barmode="stack", height=350)
        st.plotly_chart(fig_stack, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 06: SIMULADOR
# ---------------------------------------------------------
elif menu_opt == "06. Simulador":
    st.markdown('<div class="greeting-title">Simulador Financiero <span>MYPE</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="greeting-sub">Modifica parámetros en tiempo real para proyectar el impacto en ventas y utilidad.</div>', unsafe_allow_html=True)

    s_col1, s_col2 = st.columns([1, 1.3])

    with s_col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Variables de Simulación</div>', unsafe_allow_html=True)
        
        var_precio = st.slider("Aumento / Reducción de Precios (%)", -20, 30, 5, step=1)
        var_volumen = st.slider("Incremento de Volumen de Ventas (%)", -10, 50, 15, step=1)
        var_costo = st.slider("Reducción de Costos de Proveedores (%)", 0, 25, 8, step=1)
        
        vtas_base = df_curr["Ventas_Soles"].sum()
        util_base = df_curr["Utilidad_Soles"].sum()
        cost_base = df_curr["Costo_Soles"].sum()

        vtas_sim = vtas_base * (1 + var_precio/100) * (1 + var_volumen/100)
        cost_sim = cost_base * (1 + var_volumen/100) * (1 - var_costo/100)
        util_sim = vtas_sim - cost_sim
        diff_util = util_sim - util_base

        st.markdown('---')
        st.markdown(f'''
        <div style="background-color: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 10px; padding: 15px;">
            <div style="font-size: 13px; font-weight: 700; color: #047857;">Impacto Estimado en Utilidad:</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 800; color: #065F46; margin: 4px 0;">
                +S/ {diff_util:,.2f}
            </div>
            <div style="font-size: 12px; color: #047857;">
                Utilidad Proyectada: <b>S/ {util_sim:,.2f}</b> (vs S/ {util_base:,.2f} actual)
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with s_col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Comparativa: Actual vs. Proyectado</div>', unsafe_allow_html=True)
        
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Bar(
            name="Actual",
            x=["Ventas Totales", "Costo Operativo", "Utilidad Neta"],
            y=[vtas_base, cost_base, util_base],
            marker_color="#6B7686",
            text=[f"S/ {vtas_base:,.0f}", f"S/ {cost_base:,.0f}", f"S/ {util_base:,.0f}"],
            textposition="outside",
            textfont=dict(color="#0B1220", size=11)
        ))
        fig_sim.add_trace(go.Bar(
            name="Proyectado",
            x=["Ventas Totales", "Costo Operativo", "Utilidad Neta"],
            y=[vtas_sim, cost_sim, util_sim],
            marker_color="#00C2D1",
            text=[f"S/ {vtas_sim:,.0f}", f"S/ {cost_sim:,.0f}", f"S/ {util_sim:,.0f}"],
            textposition="outside",
            textfont=dict(color="#0B1220", size=11)
        ))
        apply_plotly_style(fig_sim)
        fig_sim.update_layout(barmode="group", height=380)
        st.plotly_chart(fig_sim, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="font-size: 12px; color: #6B7686; text-align: center;">NexData – Plataforma de Inteligencia Empresarial para MYPES | Proyecto de Gestión por Resultados 2026</div>', unsafe_allow_html=True)
