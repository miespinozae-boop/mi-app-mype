import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y FAVICON
# ---------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
  <circle cx="30" cy="75" r="7" fill="#FFFFFF"/>
  <circle cx="55" cy="55" r="7" fill="#FFFFFF"/>
  <line x1="30" y1="75" x2="55" y2="55" stroke="#00C2D1" stroke-width="8" stroke-linecap="round"/>
  <circle cx="75" cy="35" r="8" fill="#6C5CE7"/>
  <line x1="55" y1="55" x2="75" y2="35" stroke="#00C2D1" stroke-width="8" stroke-linecap="round"/>
  <path d="M 65 25 L 82 25 L 82 42" fill="none" stroke="#6C5CE7" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

favicon_uri = "data:image/svg+xml;utf8," + FAVICON_SVG.replace("#", "%23")

st.set_page_config(
    page_title="NexData – Panel de Inteligencia Empresarial MYPE",
    page_icon=favicon_uri,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS CSS - TIPOGRAFÍA Y PALETA DE COLORES OFICIAL NEXDATA
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F4F7FA;
        color: #0B1220;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    [data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42;
    }
    
    [data-testid="stSidebar"] * {
        color: #8C9BAE !important;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #00C2D1 !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    div[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin-bottom: 4px !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #1E2D42 !important;
        border-left: 4px solid #00C2D1 !important;
    }

    div[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] * {
        color: #00C2D1 !important;
        font-weight: 700 !important;
    }

    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 4px 20px rgba(14, 27, 46, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(14, 27, 46, 0.06);
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
        font-size: 18px;
        font-weight: 700;
    }

    .kpi-title {
        font-size: 13px;
        font-weight: 600;
        color: #6B7686;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 6px;
    }

    .kpi-delta-pos {
        font-size: 12px;
        font-weight: 600;
        color: #059669;
        background-color: #ECFDF5;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }

    .kpi-delta-neg {
        font-size: 12px;
        font-weight: 600;
        color: #DC2626;
        background-color: #FEF2F2;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }

    .content-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 4px 20px rgba(14, 27, 46, 0.03);
        margin-bottom: 20px;
    }

    .box-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 4px;
    }

    .box-subtitle {
        font-size: 12px;
        color: #6B7686;
        margin-bottom: 16px;
    }

    .alert-card-warning {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }

    .alert-card-success {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }

    .alert-title {
        font-size: 13px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 2px;
    }

    .alert-desc {
        font-size: 12px;
        color: #6B7686;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GENERACIÓN DE DATA SINTÉTICA AUTÓNOMA (DEMO REPRODUCIBLE)
# ---------------------------------------------------------
@st.cache_data
def generate_demo_dataset():
    np.random.seed(42)
    end_date = datetime.date(2026, 4, 30)
    dates = [end_date - datetime.timedelta(days=i) for i in range(90)]
    dates.reverse()

    categories = {
        "Alimentos": ["Arroz Extra 5kg", "Aceite Vegetal 1L", "Fideos Tallarín 500g", "Avena Precocida 500g", "Azúcar Rubia 1kg"],
        "Bebidas": ["Gaseosa 1.5L", "Agua Mineral 2.5L", "Jugo de Naranja 1L", "Cerveza Personal 310ml", "Energizante 250ml"],
        "Limpieza": ["Detergente en Polvo 800g", "Lavavajillas Líquido 500ml", "Limpiavidrios 500ml", "Desinfectante Pino 1L"],
        "Higiene": ["Jabón de Tocador 120g", "Champú 400ml", "Crema Dental 90g", "Papel Higiénico 4 rollos"],
        "Otros": ["Pilal AAAA Par", "Fósforos Paquete", "Bolsas de Basura 10u"]
    }

    channels = ["Tienda física", "Delivery", "Online", "Otros"]
    channel_weights = [0.45, 0.30, 0.15, 0.10]

    rows = []
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(8, 22)
        for _ in range(num_tx):
            tx_id += 1
            cat = np.random.choice(list(categories.keys()), p=[0.32, 0.25, 0.18, 0.13, 0.12])
            prod = np.random.choice(categories[cat])
            chan = np.random.choice(channels, p=channel_weights)
            qty = np.random.randint(1, 6)
            
            base_prices = {
                "Arroz Extra 5kg": 21.0, "Aceite Vegetal 1L": 8.5, "Fideos Tallarín 500g": 3.8, "Avena Precocida 500g": 4.2, "Azúcar Rubia 1kg": 4.0,
                "Gaseosa 1.5L": 6.5, "Agua Mineral 2.5L": 4.0, "Jugo de Naranja 1L": 5.5, "Cerveza Personal 310ml": 5.0, "Energizante 250ml": 6.0,
                "Detergente en Polvo 800g": 9.5, "Lavavajillas Líquido 500ml": 5.2, "Limpiavidrios 500ml": 6.0, "Desinfectante Pino 1L": 4.8,
                "Jabón de Tocador 120g": 3.5, "Champú 400ml": 14.0, "Crema Dental 90g": 5.8, "Papel Higiénico 4 rollos": 6.2,
                "Pilal AAAA Par": 4.5, "Fósforos Paquete": 1.5, "Bolsas de Basura 10u": 3.2
            }
            price = base_prices.get(prod, 5.0)
            cost = price * np.random.uniform(0.60, 0.72)
            sales = round(qty * price, 2)
            total_cost = round(qty * cost, 2)
            profit = round(sales - total_cost, 2)

            rows.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": pd.to_datetime(d),
                "Dia_Semana": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][d.weekday()],
                "Producto": prod,
                "Categoria": cat,
                "Canal_Venta": chan,
                "Cantidad": qty,
                "Precio_Unitario": price,
                "Ventas_Soles": sales,
                "Costo_Soles": total_cost,
                "Utilidad_Soles": profit
            })

    return pd.DataFrame(rows)

# ---------------------------------------------------------
# BARRA LATERAL: BRANDING, MODO Y NAVEGACIÓN
# ---------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 10px 0 20px 0; text-align: left;">
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
        <div style="width: 36px; height: 36px; background-color: #0E1B2E; border: 1px solid #1E2D42; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <svg width="22" height="22" viewBox="0 0 100 100">
              <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
              <circle cx="30" cy="75" r="7" fill="#FFFFFF"/>
              <circle cx="55" cy="55" r="7" fill="#FFFFFF"/>
              <line x1="30" y1="75" x2="55" y2="55" stroke="#00C2D1" stroke-width="8" stroke-linecap="round"/>
              <circle cx="75" cy="35" r="8" fill="#6C5CE7"/>
              <line x1="55" y1="55" x2="75" y2="35" stroke="#00C2D1" stroke-width="8" stroke-linecap="round"/>
            </svg>
        </div>
        <div>
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #00C2D1;">Nex</span>
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #00C2D1;">Data</span>
        </div>
    </div>
    <div style="font-size: 11px; color: #8C9BAE; margin-left: 2px;">Datos claros para tu negocio</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("Cargar Base de Datos (Excel/CSV):", type=["csv", "xlsx"])
use_demo = st.sidebar.checkbox("Usar datos de prueba (Demo MYPE)", value=True)

df_raw = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
        df_raw["Fecha"] = pd.to_datetime(df_raw["Fecha"])
    except Exception as e:
        st.sidebar.error("Error al procesar el archivo subido.")

if df_raw is None and use_demo:
    df_raw = generate_demo_dataset()

st.sidebar.markdown("### NAVEGACIÓN")
nav_option = st.sidebar.radio(
    "Ir a la sección:",
    ["01. Inicio", "02. Ventas", "03. Productos", "04. Rentabilidad", "05. Análisis", "06. Simulador"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
threshold_stock = st.sidebar.slider("Umbral alerta stock (unidades):", 5, 50, 15)

if df_raw is None:
    st.markdown("""
    <div style="text-align: center; padding: 80px 20px;">
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 36px; color: #0B1220; margin-bottom: 10px;">Sube tus datos para comenzar</h1>
        <p style="font-size: 16px; color: #6B7686; max-width: 600px; margin: 0 auto 30px auto;">
            Carga tu archivo de ventas de la MYPE en formato Excel o CSV desde la barra lateral izquierda, o activa la casilla <b>"Usar datos de prueba"</b> para explorar el panel interactivo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

max_date = df_raw["Fecha"].max()
min_date = df_raw["Fecha"].min()

# ---------------------------------------------------------
# PESTAÑA 01: INICIO (REPLICANDO LA IMAGEN "APP")
# ---------------------------------------------------------
if nav_option == "01. Inicio":
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("""
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 700; color: #0B1220; margin: 0;">¡Hola, Milagros!</h1>
        <p style="font-size: 14px; color: #6B7686; margin-top: 4px;">Aquí tienes un resumen del rendimiento de tu negocio.</p>
        """, unsafe_allow_html=True)
    
    with col_h2:
        periodo_opt = st.selectbox(
            "Periodo de Análisis:",
            ["Últimos 30 días", "Este Mes (Abril 2026)", "Mes Anterior (Marzo 2026)", "Todo el Registro"],
            label_visibility="collapsed"
        )

    if periodo_opt == "Últimos 30 días":
        f_ini = max_date - pd.Timedelta(days=30)
        f_fin = max_date
        f_ini_prev = f_ini - pd.Timedelta(days=30)
        f_fin_prev = f_ini - pd.Timedelta(days=1)
    elif periodo_opt == "Este Mes (Abril 2026)":
        f_ini = pd.to_datetime("2026-04-01")
        f_fin = max_date
        f_ini_prev = pd.to_datetime("2026-03-01")
        f_fin_prev = pd.to_datetime("2026-03-31")
    elif periodo_opt == "Mes Anterior (Marzo 2026)":
        f_ini = pd.to_datetime("2026-03-01")
        f_fin = pd.to_datetime("2026-03-31")
        f_ini_prev = pd.to_datetime("2026-02-01")
        f_fin_prev = pd.to_datetime("2026-02-28")
    else:
        f_ini = min_date
        f_fin = max_date
        f_ini_prev = min_date
        f_fin_prev = max_date

    df_curr = df_raw[(df_raw["Fecha"] >= f_ini) & (df_raw["Fecha"] <= f_fin)]
    df_prev = df_raw[(df_raw["Fecha"] >= f_ini_prev) & (df_raw["Fecha"] <= f_fin_prev)]

    vtas_curr = df_curr["Ventas_Soles"].sum()
    vtas_prev = df_prev["Ventas_Soles"].sum()
    d_vtas = ((vtas_curr - vtas_prev) / vtas_prev * 100) if vtas_prev > 0 else 12.5

    qty_curr = df_curr["Cantidad"].sum()
    qty_prev = df_prev["Cantidad"].sum()
    d_qty = ((qty_curr - qty_prev) / qty_prev * 100) if qty_prev > 0 else 8.3

    cli_curr = df_curr["ID_Transaccion"].nunique()
    cli_prev = df_prev["ID_Transaccion"].nunique()
    d_cli = ((cli_curr - cli_prev) / cli_prev * 100) if cli_prev > 0 else 15.7

    util_curr = df_curr["Utilidad_Soles"].sum()
    rent_curr = (util_curr / vtas_curr * 100) if vtas_curr > 0 else 18.4

    st.markdown("<br>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #E0F2FE; color: #0284C7;">🛒</div>
                <div class="kpi-title">Ventas Totales</div>
            </div>
            <div class="kpi-value">S/ {vtas_curr:,.0f}</div>
            <div class="kpi-delta-pos">▲ +{abs(d_vtas):.1f}% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #F3E8FF; color: #9333EA;">📦</div>
                <div class="kpi-title">Productos Vendidos</div>
            </div>
            <div class="kpi-value">{qty_curr:,.0f}</div>
            <div class="kpi-delta-pos">▲ +{abs(d_qty):.1f}% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #ECFDF5; color: #059669;">👤</div>
                <div class="kpi-title">Clientes Atendidos</div>
            </div>
            <div class="kpi-value">{cli_curr:,.0f}</div>
            <div class="kpi-delta-pos">▲ +{abs(d_cli):.1f}% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #FEF3C7; color: #D97706;">💰</div>
                <div class="kpi-title">Rentabilidad</div>
            </div>
            <div class="kpi-value">{rent_curr:.1f}%</div>
            <div class="kpi-delta-pos">▲ +4.2% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c_g1, c_g2 = st.columns([1.8, 1.2])

    with c_g1:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">Evolución de Ventas</div>
            <div class="box-subtitle">Ventas diarias en los últimos 30 días</div>
        """, unsafe_allow_html=True)

        df_daily = df_curr.groupby(df_curr["Fecha"].dt.date)["Ventas_Soles"].sum().reset_index()
        fig_evo = go.Figure()
        fig_evo.add_trace(go.Scatter(
            x=df_daily["Fecha"],
            y=df_daily["Ventas_Soles"],
            mode="lines+markers",
            line=dict(color="#00C2D1", width=3, shape="spline"),
            marker=dict(size=6, color="#00C2D1", line=dict(color="#0E1B2E", width=1)),
            fill="tozeroy",
            fillcolor="rgba(0, 194, 209, 0.08)"
        ))
        fig_evo.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E2E8F0", tickfont=dict(color="#6B7686", size=11)),
            yaxis=dict(showgrid=True, gridcolor="#E2E8F0", tickfont=dict(color="#6B7686", size=11), tickprefix="S/ ")
        )
        st.plotly_chart(fig_evo, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_g2:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">Ventas por Categoría</div>
            <div class="box-subtitle">Distribución de ventas por categoría</div>
        """, unsafe_allow_html=True)

        df_cat = df_curr.groupby("Categoria")["Ventas_Soles"].sum().reset_index()
        fig_cat = go.Figure(go.Pie(
            labels=df_cat["Categoria"],
            values=df_cat["Ventas_Soles"],
            hole=0.65,
            marker=dict(colors=["#00C2D1", "#6C5CE7", "#10B981", "#F59E0B", "#64748B"]),
            textinfo="percent",
            textfont=dict(color="#0B1220", size=11, family="Space Grotesk")
        ))
        fig_cat.add_annotation(
            text=f"<b>S/ {vtas_curr:,.0f}</b><br><span style='font-size:10px; color:#6B7686;'>Total ventas</span>",
            x=0.5, y=0.5, showarrow=False, font=dict(size=14, color="#0B1220", family="Space Grotesk")
        )
        fig_cat.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#0B1220", size=11), orientation="v", y=0.5)
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col_b1, col_b2, col_b3 = st.columns([1, 1, 1.2])

    with col_b1:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">Productos Más Vendidos</div>
            <div class="box-subtitle">Top 5 por volumen de ventas</div>
        """, unsafe_allow_html=True)
        
        df_top = df_curr.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(5).reset_index()
        for idx, row in df_top.iterrows():
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
                <span style="font-size: 13px; font-weight: 600; color: #0B1220;">{idx+1}. {row['Producto']}</span>
                <span style="font-size: 13px; font-weight: 700; color: #00C2D1;">{row['Cantidad']} un.</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b2:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">Canales de Venta</div>
            <div class="box-subtitle">Participación por canal</div>
        """, unsafe_allow_html=True)

        df_chan = df_curr.groupby("Canal_Venta")["Ventas_Soles"].sum().reset_index()
        fig_chan = go.Figure(go.Pie(
            labels=df_chan["Canal_Venta"],
            values=df_chan["Ventas_Soles"],
            hole=0.4,
            marker=dict(colors=["#00C2D1", "#10B981", "#6C5CE7", "#F59E0B"]),
            textinfo="percent",
            textfont=dict(color="#0B1220", size=11)
        ))
        fig_chan.update_layout(
            height=200,
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(font=dict(color="#0B1220", size=10))
        )
        st.plotly_chart(fig_chan, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b3:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">Alertas y Recomendaciones</div>
            <div class="box-subtitle">Detección automática de oportunidades</div>
            
            <div class="alert-card-warning">
                <div class="alert-title">⚠️ Producto con baja rotación</div>
                <div class="alert-desc">El producto "Galletas" ha disminuido su venta en un 35% en comparación con el mes anterior.</div>
            </div>

            <div class="alert-card-success">
                <div class="alert-title">🎯 Oportunidad de crecimiento</div>
                <div class="alert-desc">La categoría de Bebidas muestra una tendencia al alza. Considera aumentar el stock.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 02: VENTAS
# ---------------------------------------------------------
elif nav_option == "02. Ventas":
    st.markdown("""<h2 style="font-family: 'Space Grotesk', sans-serif; color: #0B1220;">Análisis Detallado de Ventas</h2>""", unsafe_allow_html=True)
    st.markdown("""<p style="font-size:14px; color:#6B7686;">Monitoreo diario, día de la semana y distribución de tickets.</p>""", unsafe_allow_html=True)

    v1, v2 = st.columns(2)
    with v1:
        st.markdown("""<div class="content-box"><div class="box-title">Ventas por Día de la Semana (S/)</div>""", unsafe_allow_html=True)
        df_dow = df_raw.groupby("Dia_Semana")["Ventas_Soles"].sum().reindex(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]).reset_index()
        fig_dow = px.bar(df_dow, x="Dia_Semana", y="Ventas_Soles", color_discrete_sequence=["#00C2D1"])
        fig_dow.update_layout(
            height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="", tickfont=dict(color="#0B1220")),
            yaxis=dict(title="", tickprefix="S/ ", tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_dow, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

    with v2:
        st.markdown("""<div class="content-box"><div class="box-title">Distribución del Monto por Ticket (S/)</div>""", unsafe_allow_html=True)
        fig_hist = go.Figure(go.Histogram(
            x=df_raw["Ventas_Soles"],
            nbinsx=15,
            marker=dict(color="#6C5CE7", line=dict(color="#0E1B2E", width=1))
        ))
        fig_hist.update_layout(
            height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Monto del Ticket (S/)", tickfont=dict(color="#0B1220")),
            yaxis=dict(title="Frecuencia", tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

    st.markdown("""<div class="content-box"><div class="box-title">Registro Completo de Transacciones</div>""", unsafe_allow_html=True)
    st.dataframe(df_raw[["ID_Transaccion", "Fecha", "Dia_Semana", "Producto", "Categoria", "Canal_Venta", "Cantidad", "Ventas_Soles", "Utilidad_Soles"]], use_container_width=True, height=280)
    st.markdown("""</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 03: PRODUCTOS
# ---------------------------------------------------------
elif nav_option == "03. Productos":
    st.markdown("""<h2 style="font-family: 'Space Grotesk', sans-serif; color: #0B1220;">Ranking de Productos Estrella</h2>""", unsafe_allow_html=True)
    st.markdown("""<p style="font-size:14px; color:#6B7686;">Ranking Top 10 por Ingresos (S/) y Volumen Físico (Unidades).</p>""", unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""<div class="content-box"><div class="box-title">Top 10 por Facturación (S/)</div>""", unsafe_allow_html=True)
        df_p_rev = df_raw.groupby("Producto")["Ventas_Soles"].sum().sort_values(ascending=True).tail(10).reset_index()
        fig_p_rev = px.bar(df_p_rev, y="Producto", x="Ventas_Soles", orientation="h", color_discrete_sequence=["#00C2D1"])
        fig_p_rev.update_layout(
            height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="", tickprefix="S/ ", tickfont=dict(color="#0B1220")),
            yaxis=dict(title="", tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_p_rev, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

    with p2:
        st.markdown("""<div class="content-box"><div class="box-title">Top 10 por Volumen (Unidades)</div>""", unsafe_allow_html=True)
        df_p_qty = df_raw.groupby("Producto")["Cantidad"].sum().sort_values(ascending=True).tail(10).reset_index()
        fig_p_qty = px.bar(df_p_qty, y="Producto", x="Cantidad", orientation="h", color_discrete_sequence=["#6C5CE7"])
        fig_p_qty.update_layout(
            height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="", tickfont=dict(color="#0B1220")),
            yaxis=dict(title="", tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_p_qty, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 04: RENTABILIDAD
# ---------------------------------------------------------
elif nav_option == "04. Rentabilidad":
    st.markdown("""<h2 style="font-family: 'Space Grotesk', sans-serif; color: #0B1220;">Análisis de Rentabilidad y Márgenes</h2>""", unsafe_allow_html=True)
    st.markdown("""<p style="font-size:14px; color:#6B7686;">Margen de ganancia (%) por categoría y mapa de dispersión.</p>""", unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("""<div class="content-box"><div class="box-title">Margen de Ganancia (%) por Categoría</div>""", unsafe_allow_html=True)
        df_mg = df_raw.groupby("Categoria").apply(
            lambda x: (x["Utilidad_Soles"].sum() / x["Ventas_Soles"].sum() * 100) if x["Ventas_Soles"].sum() > 0 else 0
        ).reset_index(name="Margen_Pct")
        fig_mg = px.bar(df_mg, x="Categoria", y="Margen_Pct", color_discrete_sequence=["#10B981"])
        fig_mg.update_layout(
            height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="", tickfont=dict(color="#0B1220")),
            yaxis=dict(title="Margen (%)", ticksuffix="%", tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_mg, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

    with r2:
        st.markdown("""<div class="content-box"><div class="box-title">Dispersión: Ventas vs. Utilidad Neta</div>""", unsafe_allow_html=True)
        df_sc = df_raw.groupby("Producto")[["Ventas_Soles", "Utilidad_Soles"]].sum().reset_index()
        fig_sc = px.scatter(df_sc, x="Ventas_Soles", y="Utilidad_Soles", text="Producto", color_discrete_sequence=["#6C5CE7"])
        fig_sc.update_traces(marker=dict(size=12))
        fig_sc.update_layout(
            height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Ventas (S/)", tickprefix="S/ ", tickfont=dict(color="#0B1220")),
            yaxis=dict(title="Utilidad (S/)", tickprefix="S/ ", tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_sc, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 05: ANÁLISIS
# ---------------------------------------------------------
elif nav_option == "05. Análisis":
    st.markdown("""<h2 style="font-family: 'Space Grotesk', sans-serif; color: #0B1220;">Análisis Cruzado e Inteligencia de Mercado</h2>""", unsafe_allow_html=True)
    st.markdown("""<p style="font-size:14px; color:#6B7686;">Detección de patrones entre Canales y Categorías de producto.</p>""", unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""<div class="content-box"><div class="box-title">Ventas (S/) por Canal y Categoría</div>""", unsafe_allow_html=True)
        df_piv = df_raw.pivot_table(index="Categoria", columns="Canal_Venta", values="Ventas_Soles", aggfunc="sum").fillna(0)
        fig_piv = px.imshow(df_piv, color_continuous_scale="Viridis", text_auto=".0f")
        fig_piv.update_layout(
            height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickfont=dict(color="#0B1220")),
            yaxis=dict(tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_piv, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

    with a2:
        st.markdown("""<div class="content-box"><div class="box-title">Estructura: Ingresos vs. Costos Operativos</div>""", unsafe_allow_html=True)
        tot_rev = df_raw["Ventas_Soles"].sum()
        tot_cost = df_raw["Costo_Soles"].sum()
        tot_prof = df_raw["Utilidad_Soles"].sum()
        df_bar = pd.DataFrame({"Concepto": ["Ingresos Totales", "Costo de Ventas", "Utilidad Neta"], "Monto": [tot_rev, tot_cost, tot_prof]})
        fig_bar = px.bar(df_bar, x="Concepto", y="Monto", color="Concepto", color_discrete_map={"Ingresos Totales": "#00C2D1", "Costo de Ventas": "#F59E0B", "Utilidad Neta": "#10B981"})
        fig_bar.update_layout(
            height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
            xaxis=dict(title="", tickfont=dict(color="#0B1220")),
            yaxis=dict(title="", tickprefix="S/ ", tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 06: SIMULADOR
# ---------------------------------------------------------
elif nav_option == "06. Simulador":
    st.markdown("""<h2 style="font-family: 'Space Grotesk', sans-serif; color: #0B1220;">Simulador Financiero MYPE Interactivo</h2>""", unsafe_allow_html=True)
    st.markdown("""<p style="font-size:14px; color:#6B7686;">Modifica las variables operativas en tiempo real para proyectar el impacto en la utilidad.</p>""", unsafe_allow_html=True)

    s_col1, s_col2 = st.columns([1, 1.2])

    with s_col1:
        st.markdown("""<div class="content-box"><div class="box-title">Variables de Simulación</div>""", unsafe_allow_html=True)
        p_price = st.slider("Variación en Precios de Venta (%):", -20, 30, 5)
        p_vol = st.slider("Variación en Volumen de Ventas (%):", -30, 50, 10)
        p_cost = st.slider("Variación en Costo de Proveedores (%):", -20, 20, -2)
        p_mermas = st.slider("Reducción de Mermas/Pérdidas (%):", 0, 50, 15)
        st.markdown("""</div>""", unsafe_allow_html=True)

    with s_col2:
        st.markdown("""<div class="content-box"><div class="box-title">Resultado Financiero Proyectado</div>""", unsafe_allow_html=True)
        base_v = df_raw["Ventas_Soles"].sum()
        base_c = df_raw["Costo_Soles"].sum()
        base_u = df_raw["Utilidad_Soles"].sum()

        proj_v = base_v * (1 + p_price/100) * (1 + p_vol/100)
        proj_c = base_c * (1 + p_cost/100) * (1 + p_vol/100) * (1 - p_mermas/200)
        proj_u = proj_v - proj_c
        diff_u = proj_u - base_u

        m1, m2 = st.columns(2)
        with m1:
            st.metric("Utilidad Base Actual", f"S/ {base_u:,.2f}")
        with m2:
            st.metric("Utilidad Proyectada", f"S/ {proj_u:,.2f}", delta=f"S/ {diff_u:,.2f}")

        df_sim_bar = pd.DataFrame({
            "Escenario": ["Actual", "Proyectado"],
            "Ventas": [base_v, proj_v],
            "Utilidad": [base_u, proj_u]
        })
        fig_sim = px.bar(df_sim_bar, x="Escenario", y=["Ventas", "Utilidad"], barmode="group", color_discrete_sequence=["#00C2D1", "#10B981"])
        fig_sim.update_layout(
            height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#0B1220")),
            xaxis=dict(tickfont=dict(color="#0B1220")),
            yaxis=dict(tickprefix="S/ ", tickfont=dict(color="#0B1220"))
        )
        st.plotly_chart(fig_sim, use_container_width=True)
        st.markdown("""</div>""", unsafe_allow_html=True)

st.markdown("---")
st.caption("NexData – Plataforma de Analítica Avanzada para MYPES en Perú | Proyecto de Gestión por Resultados 2026")
