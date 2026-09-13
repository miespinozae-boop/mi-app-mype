import os
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Configuración de la página
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%230E1B2E"/><path d="M20 80 L45 55 L65 70 L85 30" stroke="%2300C2D1" stroke-width="8" stroke-linecap="round" fill="none"/><circle cx="85" cy="30" r="10" fill="%236C5CE7"/></svg>"""
st.set_page_config(
    page_title="NexData – Panel de Inteligencia Empresarial",
    page_icon="data:image/svg+xml;utf8," + FAVICON_SVG,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Limpios, Ultra-Modernos SaaS (Cero texto blanco en fondo claro)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0B1220 !important;
        background-color: #F4F7FA;
    }

    .stApp {
        background-color: #F4F7FA;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42;
    }
    section[data-testid="stSidebar"] *, section[data-testid="stSidebar"] label {
        color: #8C9BAE !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #00C2D1 !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Card Styling */
    .metric-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(14, 27, 46, 0.06);
    }
    .metric-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    .icon-box {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #6B7686 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #0B1220 !important;
        font-family: 'Space Grotesk', sans-serif;
        margin: 4px 0;
    }
    .metric-delta-pos {
        font-size: 12px;
        font-weight: 700;
        color: #059669 !important;
        background-color: #ECFDF5;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }
    .metric-delta-neg {
        font-size: 12px;
        font-weight: 700;
        color: #DC2626 !important;
        background-color: #FEF2F2;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }

    /* Container Box */
    .content-box {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03);
        margin-bottom: 20px;
    }

    /* Product row bar */
    .prod-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #F1F5F9;
    }
    .prod-name {
        font-weight: 600;
        font-size: 14px;
        color: #0B1220 !important;
        width: 140px;
    }
    .prod-bar-bg {
        flex-grow: 1;
        height: 10px;
        background-color: #F1F5F9;
        border-radius: 5px;
        margin: 0 15px;
        overflow: hidden;
    }
    .prod-bar-fill {
        height: 100%;
        border-radius: 5px;
    }
    .prod-qty {
        font-size: 13px;
        font-weight: 700;
        color: #6B7686 !important;
        width: 60px;
        text-align: right;
    }

    /* Alerts */
    .alert-card-warning {
        background-color: #FFFBEB !important;
        border: 1px solid #FDE68A;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-card-success {
        background-color: #ECFDF5 !important;
        border: 1px solid #A7F3D0;
        border-radius: 12px;
        padding: 14px;
    }
    .alert-title-warning {
        font-weight: 700;
        font-size: 14px;
        color: #92400E !important;
        margin-bottom: 4px;
    }
    .alert-title-success {
        font-weight: 700;
        font-size: 14px;
        color: #065F46 !important;
        margin-bottom: 4px;
    }
    .alert-desc {
        font-size: 13px;
        color: #4B5563 !important;
    }

    /* Buttons & Nav */
    .stButton>button {
        background-color: #0E1B2E !important;
        color: #00C2D1 !important;
        border-radius: 10px !important;
        border: 1px solid #1E2D42 !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Logo SVG Oficial NexData
NEXDATA_LOGO_HTML = """
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px;">
    <div style="width: 44px; height: 44px; background: #0E1B2E; border-radius: 12px; display: flex; align-items: center; justify-content: center; padding: 7px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
        <svg viewBox="0 0 100 100" style="width: 100%; height: 100%;">
            <rect width="100" height="100" rx="20" fill="#0E1B2E"/>
            <path d="M20 75 L45 50 L65 65 L82 32" stroke="#00C2D1" stroke-width="9" stroke-linecap="round" fill="none"/>
            <circle cx="20" cy="75" r="6" fill="#00C2D1"/>
            <circle cx="45" cy="50" r="6" fill="#00C2D1"/>
            <circle cx="65" cy="65" r="6" fill="#00C2D1"/>
            <path d="M72 25 L88 32 L81 48" stroke="#6C5CE7" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        </svg>
    </div>
    <div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; line-height: 1; color: #00C2D1;">
            Nex<span style="color: #00C2D1;">Data</span>
        </div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 11px; color: #8C9BAE; margin-top: 3px;">
            Datos claros para tu negocio
        </div>
    </div>
</div>
"""

st.sidebar.markdown(NEXDATA_LOGO_HTML, unsafe_allow_html=True)

# Cargar Datos con Fallback
@st.cache_data
def load_dataset():
    paths = [
        "/workspace/scratch/dataset_mype_transacciones.csv",
        "/workspace/artifacts/dataset_mype_transacciones.csv",
        "dataset_mype_transacciones.csv"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                df = pd.read_csv(p)
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                return df
            except Exception:
                pass
    
    # Dataset sintético de respaldo
    np.random.seed(42)
    dates = pd.date_range(end=datetime.date(2026, 9, 12), periods=90, freq='D')
    categories = {
        'Alimentos': ['Arroz 5kg', 'Aceite 1L', 'Fideo 500g', 'Azúcar 1kg'],
        'Bebidas': ['Gaseosa 1.5L', 'Agua 2.5L', 'Jugo Naranja', 'Cerveza 620ml'],
        'Limpieza': ['Detergente 1kg', 'Lejía 1L', 'Jabón Líquido', 'Lava vajillas'],
        'Higiene': ['Shampoo 400ml', 'Pasta Dental', 'Jabón Tocador', 'Papel Higiénico'],
        'Otros': ['Pilas AA', 'Velas x4', 'Fósforos x10', 'Bolsas x50']
    }
    channels = ['Tienda física', 'Delivery', 'Online', 'Otros']
    
    records = []
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(8, 18)
        for _ in range(num_tx):
            tx_id += 1
            cat = np.random.choice(list(categories.keys()), p=[0.33, 0.25, 0.18, 0.13, 0.11])
            prod = np.random.choice(categories[cat])
            chan = np.random.choice(channels, p=[0.45, 0.30, 0.15, 0.10])
            qty = np.random.randint(1, 6)
            price = round(np.random.uniform(4.0, 35.0), 2)
            sales = round(qty * price, 2)
            cost = round(sales * np.random.uniform(0.55, 0.75), 2)
            profit = round(sales - cost, 2)
            day_name = d.strftime('%A')
            
            records.append({
                'ID_Transaccion': f'TX-{tx_id}',
                'Fecha': d,
                'Dia_Semana': day_name,
                'Producto': prod,
                'Categoria': cat,
                'Canal_Venta': chan,
                'Cantidad': qty,
                'Precio_Unitario': price,
                'Ventas_Soles': sales,
                'Costo_Soles': cost,
                'Utilidad_Soles': profit
            })
    return pd.DataFrame(records)

df_raw = load_dataset()

# BARRA LATERAL: Controles y Filtros
st.sidebar.markdown("<h3 style='font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>Navegación</h3>", unsafe_allow_html=True)
modulo_sel = st.sidebar.radio(
    "Seleccionar Módulo:",
    ["01. Inicio", "02. Ventas", "03. Productos", "04. Rentabilidad", "05. Análisis", "06. Simulador"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>Origen de Datos</h3>", unsafe_allow_html=True)
use_demo = st.sidebar.checkbox("Usar datos de prueba (Demo MYPE)", value=True)
uploaded_file = st.sidebar.file_uploader("Subir archivo Excel/CSV:", type=["csv", "xlsx"])

if uploaded_file is not None and not use_demo:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
        df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
        st.sidebar.success("Datos cargados con éxito")
    except Exception as e:
        st.sidebar.error("Error al procesar el archivo. Mostrando demo.")

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;'>Filtros de Análisis</h3>", unsafe_allow_html=True)

periodo_opt = st.sidebar.selectbox(
    "Periodo:",
    ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Registro"]
)

max_date = df_raw['Fecha'].max()
if periodo_opt == "Últimos 30 días":
    fecha_inicio = max_date - pd.Timedelta(days=30)
    fecha_fin = max_date
    fecha_inicio_prev = fecha_inicio - pd.Timedelta(days=30)
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
elif periodo_opt == "Este Mes":
    fecha_inicio = max_date.replace(day=1)
    fecha_fin = max_date
    fecha_inicio_prev = (fecha_inicio - pd.Timedelta(days=1)).replace(day=1)
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
elif periodo_opt == "Mes Anterior":
    fecha_fin = max_date.replace(day=1) - pd.Timedelta(days=1)
    fecha_inicio = fecha_fin.replace(day=1)
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    fecha_inicio_prev = fecha_fin_prev.replace(day=1)
else:
    fecha_inicio = df_raw['Fecha'].min()
    fecha_fin = max_date
    fecha_inicio_prev = fecha_inicio
    fecha_fin_prev = fecha_fin

cats_list = ["Todas"] + list(df_raw['Categoria'].unique())
cat_sel = st.sidebar.selectbox("Categoría:", cats_list)

if cat_sel != "Todas":
    prods_list = ["Todos"] + list(df_raw[df_raw['Categoria'] == cat_sel]['Producto'].unique())
else:
    prods_list = ["Todos"] + list(df_raw['Producto'].unique())
prod_sel = st.sidebar.selectbox("Producto:", prods_list)

canales_list = ["Todos"] + list(df_raw['Canal_Venta'].unique())
canal_sel = st.sidebar.selectbox("Canal de Venta:", canales_list)

stock_threshold = st.sidebar.slider("Umbral Crítico de Stock (un):", min_value=10, max_value=100, value=30, step=5)

# Filtrar Datos
def filter_df(df, f_ini, f_fin, cat, prod, canal):
    df_f = df[(df['Fecha'] >= f_ini) & (df['Fecha'] <= f_fin)]
    if cat != "Todas":
        df_f = df_f[df_f['Categoria'] == cat]
    if prod != "Todos":
        df_f = df_f[df_f['Producto'] == prod]
    if canal != "Todos":
        df_f = df_f[df_f['Canal_Venta'] == canal]
    return df_f

df_curr = filter_df(df_raw, fecha_inicio, fecha_fin, cat_sel, prod_sel, canal_sel)
df_prev = filter_df(df_raw, fecha_inicio_prev, fecha_fin_prev, cat_sel, prod_sel, canal_sel)

# KPIs Principales
vtas_curr = df_curr['Ventas_Soles'].sum()
vtas_prev = df_prev['Ventas_Soles'].sum()
delta_vtas = ((vtas_curr - vtas_prev) / vtas_prev * 100) if vtas_prev > 0 else 0

units_curr = df_curr['Cantidad'].sum()
units_prev = df_prev['Cantidad'].sum()
delta_units = ((units_curr - units_prev) / units_prev * 100) if units_prev > 0 else 0

tx_curr = len(df_curr)
tx_prev = len(df_prev)
delta_tx = ((tx_curr - tx_prev) / tx_prev * 100) if tx_prev > 0 else 0

util_curr = df_curr['Utilidad_Soles'].sum()
mg_curr = (util_curr / vtas_curr * 100) if vtas_curr > 0 else 0
util_prev = df_prev['Utilidad_Soles'].sum()
mg_prev = (util_prev / vtas_prev * 100) if vtas_prev > 0 else 0
delta_mg = mg_curr - mg_prev

# HEADER PRINCIPAL DE BIENVENIDA (Fiel a la imagen "APP")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
    <div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 800; color: #0B1220; margin: 0;">
            ¡Hola, <span style="color: #0284C7;">Milagros!</span>
        </h1>
        <p style="font-size: 15px; color: #6B7686; margin-top: 4px;">
            Aquí tienes un resumen del rendimiento de tu negocio.
        </p>
    </div>
    <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 8px 16px; border-radius: 10px; font-size: 13px; font-weight: 600; color: #0B1220;">
        Periodo: Últimos 30 días
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULO 01: INICIO
# ---------------------------------------------------------
if modulo_sel == "01. Inicio":
    # 4 Tarjetas KPI Superiores (Fieles a la imagen APP)
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <div class="icon-box" style="background-color: #E0F2FE; color: #0284C7;">🛒</div>
                <div class="metric-label">Ventas Totales</div>
            </div>
            <div class="metric-value">S/ {vtas_curr:,.0f}</div>
            <div class="{'metric-delta-pos' if delta_vtas >= 0 else 'metric-delta-neg'}">
                {'▲ +' if delta_vtas >= 0 else '▼ '}{abs(delta_vtas):.1f}% vs. mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <div class="icon-box" style="background-color: #F3E8FF; color: #8B5CF6;">📦</div>
                <div class="metric-label">Productos Vendidos</div>
            </div>
            <div class="metric-value">{units_curr:,.0f}</div>
            <div class="{'metric-delta-pos' if delta_units >= 0 else 'metric-delta-neg'}">
                {'▲ +' if delta_units >= 0 else '▼ '}{abs(delta_units):.1f}% vs. mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <div class="icon-box" style="background-color: #DCFCE7; color: #10B981;">👤</div>
                <div class="metric-label">Clientes Atendidos</div>
            </div>
            <div class="metric-value">{tx_curr:,.0f}</div>
            <div class="{'metric-delta-pos' if delta_tx >= 0 else 'metric-delta-neg'}">
                {'▲ +' if delta_tx >= 0 else '▼ '}{abs(delta_tx):.1f}% vs. mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with k4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <div class="icon-box" style="background-color: #FEF3C7; color: #F59E0B;">💰</div>
                <div class="metric-label">Rentabilidad</div>
            </div>
            <div class="metric-value">{mg_curr:.1f}%</div>
            <div class="{'metric-delta-pos' if delta_mg >= 0 else 'metric-delta-neg'}">
                {'▲ +' if delta_mg >= 0 else '▼ '}{abs(delta_mg):.1f}% vs. mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Fila Central de Gráficos (Evolución de Ventas + Donut Categoría)
    c_left, c_right = st.columns([1.6, 1])

    with c_left:
        st.markdown("""
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px; color: #0B1220; margin-bottom: 2px;">
            Evolución de Ventas
        </div>
        <div style="font-size: 12px; color: #6B7280; margin-bottom: 12px;">Ventas diarias en los últimos 30 días</div>
        """, unsafe_allow_html=True)
        
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)['Ventas_Soles'].sum().reset_index()
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'],
            y=df_daily['Ventas_Soles'],
            mode='lines+markers',
            line=dict(color='#0284C7', width=3, shape='spline'),
            marker=dict(size=6, color='#0284C7'),
            fill='tozeroy',
            fillcolor='rgba(2, 132, 199, 0.08)',
            name='Ventas (S/)'
        ))
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=10, b=20),
            height=280,
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7280', size=11)),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7280', size=11)),
            showlegend=False
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with c_right:
        st.markdown("""
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px; color: #0B1220; margin-bottom: 2px;">
            Ventas por Categoría
        </div>
        <div style="font-size: 12px; color: #6B7280; margin-bottom: 12px;">Distribución de ventas por categoría</div>
        """, unsafe_allow_html=True)
        
        cat_sales = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        fig_donut = go.Figure(go.Pie(
            labels=cat_sales['Categoria'],
            values=cat_sales['Ventas_Soles'],
            hole=0.65,
            marker=dict(colors=['#00C2D1', '#6C5CE7', '#10B981', '#F59E0B', '#64748B']),
            textinfo='percent',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            showlegend=True,
            legend=dict(font=dict(color='#0B1220', size=11)),
            annotations=[dict(text=f"<b>S/ {vtas_curr:,.0f}</b><br><span style='font-size:10px; color:#6B7280;'>Total ventas</span>", x=0.5, y=0.5, font=dict(size=14, color='#0B1220'), showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Fila Inferior (Productos más Vendidos + Canales + Alertas)
    b1, b2, b3 = st.columns([1.2, 1, 1.2])

    with b1:
        st.markdown("""
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px; color: #0B1220; margin-bottom: 2px;">
            Productos Más Vendidos
        </div>
        <div style="font-size: 12px; color: #6B7280; margin-bottom: 14px;">Top 5 por volumen de ventas</div>
        """, unsafe_allow_html=True)
        
        top5 = df_curr.groupby('Producto')['Cantidad'].sum().nlargest(5).reset_index()
        max_q = top5['Cantidad'].max() if len(top5) > 0 else 1
        colors = ['#00C2D1', '#10B981', '#6C5CE7', '#F59E0B', '#0284C7']
        
        for idx, row in top5.iterrows():
            pct = (row['Cantidad'] / max_q) * 100
            bar_col = colors[idx % len(colors)]
            st.markdown(f"""
            <div class="prod-item">
                <div class="prod-name">{idx+1}. {row['Producto']}</div>
                <div class="prod-bar-bg">
                    <div class="prod-bar-fill" style="width: {pct}%; background-color: {bar_col};"></div>
                </div>
                <div class="prod-qty">{row['Cantidad']} un.</div>
            </div>
            """, unsafe_allow_html=True)

    with b2:
        st.markdown("""
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px; color: #0B1220; margin-bottom: 2px;">
            Canales de Venta
        </div>
        <div style="font-size: 12px; color: #6B7280; margin-bottom: 12px;">Participación por canal</div>
        """, unsafe_allow_html=True)
        
        chan_sales = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
        fig_chan = go.Figure(go.Pie(
            labels=chan_sales['Canal_Venta'],
            values=chan_sales['Ventas_Soles'],
            hole=0.4,
            marker=dict(colors=['#2563EB', '#10B981', '#8B5CF6', '#F59E0B']),
            textinfo='percent',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_chan.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            height=220,
            legend=dict(font=dict(color='#0B1220', size=10))
        )
        st.plotly_chart(fig_chan, use_container_width=True)

    with b3:
        st.markdown("""
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px; color: #0B1220; margin-bottom: 2px;">
            Alertas y Recomendaciones
        </div>
        <div style="font-size: 12px; color: #6B7280; margin-bottom: 14px;">Sugerencias del motor analítico</div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-card-warning">
            <div class="alert-title-warning">⚠️ Producto con baja rotación</div>
            <div class="alert-desc">El producto "Galletas" ha disminuido su venta en un 35% en comparación con el mes anterior.</div>
        </div>
        <div class="alert-card-success">
            <div class="alert-title-success">🎯 Oportunidad de crecimiento</div>
            <div class="alert-desc">La categoría Bebidas muestra una tendencia al alza los fines de semana. Considera aumentar stock.</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULO 02: VENTAS
# ---------------------------------------------------------
elif modulo_sel == "02. Ventas":
    st.markdown("<h2 style='font-family: 'Space Grotesk', sans-serif; color: #0B1220;'>Análisis Detallado de Ventas</h2>", unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("<b>Ventas por Día de la Semana</b>", unsafe_allow_html=True)
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_names = {'Monday':'Lun', 'Tuesday':'Mar', 'Wednesday':'Mié', 'Thursday':'Jue', 'Friday':'Vie', 'Saturday':'Sáb', 'Sunday':'Dom'}
        
        dow_df = df_curr.groupby('Dia_Semana')['Ventas_Soles'].sum().reindex(dow_order).fillna(0).reset_index()
        dow_df['Dia_Nombre'] = dow_df['Dia_Semana'].map(dow_names)
        
        fig_dow = go.Figure(go.Bar(
            x=dow_df['Dia_Nombre'],
            y=dow_df['Ventas_Soles'],
            marker=dict(color='#00C2D1', cornerradius=6),
            text=[f"S/ {v:,.0f}" for v in dow_df['Ventas_Soles']],
            textposition='auto',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_dow.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=300,
            xaxis=dict(tickfont=dict(color='#6B7280', size=11), showgrid=False),
            yaxis=dict(title=dict(text="Ventas (S/)", font=dict(color='#0B1220', size=11)), tickfont=dict(color='#6B7280', size=11), showgrid=True, gridcolor='#E2E8F0')
        )
        st.plotly_chart(fig_dow, use_container_width=True)

    with col_v2:
        st.markdown("<b>Distribución de Ticket de Compra</b>", unsafe_allow_html=True)
        fig_hist = go.Figure(go.Histogram(
            x=df_curr['Ventas_Soles'],
            nbinsx=15,
            marker=dict(color='#6C5CE7', line=dict(color='#0E1B2E', width=1))
        ))
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=300,
            xaxis=dict(title=dict(text="Monto del Ticket (S/)", font=dict(color='#0B1220', size=11)), tickfont=dict(color='#6B7280', size=11), showgrid=True, gridcolor='#E2E8F0'),
            yaxis=dict(title=dict(text="Frecuencia", font=dict(color='#0B1220', size=11)), tickfont=dict(color='#6B7280', size=11), showgrid=True, gridcolor='#E2E8F0')
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("<b>Registro de Transacciones</b>", unsafe_allow_html=True)
    st.dataframe(df_curr[['ID_Transaccion', 'Fecha', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Ventas_Soles', 'Utilidad_Soles']], use_container_width=True)

# ---------------------------------------------------------
# MODULO 03: PRODUCTOS
# ---------------------------------------------------------
elif modulo_sel == "03. Productos":
    st.markdown("<h2 style='font-family: 'Space Grotesk', sans-serif; color: #0B1220;'>Rendimiento de Productos e Inventario</h2>", unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("<b>Top 10 Productos por Facturación (S/)</b>", unsafe_allow_html=True)
        top10_sales = df_curr.groupby('Producto')['Ventas_Soles'].sum().nlargest(10).reset_index().sort_values(by='Ventas_Soles', ascending=True)
        
        fig_top10 = go.Figure(go.Bar(
            x=top10_sales['Ventas_Soles'],
            y=top10_sales['Producto'],
            orientation='h',
            marker=dict(color='#00C2D1', cornerradius=6),
            text=[f"S/ {v:,.0f}" for v in top10_sales['Ventas_Soles']],
            textposition='inside',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_top10.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=340,
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7280', size=11)),
            yaxis=dict(autorange="reversed", tickfont=dict(color='#0B1220', size=11), showgrid=False)
        )
        st.plotly_chart(fig_top10, use_container_width=True)

    with col_p2:
        st.markdown("<b>Top 10 Productos por Unidades Vendidas</b>", unsafe_allow_html=True)
        top10_qty = df_curr.groupby('Producto')['Cantidad'].sum().nlargest(10).reset_index().sort_values(by='Cantidad', ascending=True)
        
        fig_top_qty = go.Figure(go.Bar(
            x=top10_qty['Cantidad'],
            y=top10_qty['Producto'],
            orientation='h',
            marker=dict(color='#6C5CE7', cornerradius=6),
            text=[f"{q:,} un." for q in top10_qty['Cantidad']],
            textposition='inside',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_top_qty.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=340,
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7280', size=11)),
            yaxis=dict(autorange="reversed", tickfont=dict(color='#0B1220', size=11), showgrid=False)
        )
        st.plotly_chart(fig_top_qty, use_container_width=True)

# ---------------------------------------------------------
# MODULO 04: RENTABILIDAD
# ---------------------------------------------------------
elif modulo_sel == "04. Rentabilidad":
    st.markdown("<h2 style='font-family: 'Space Grotesk', sans-serif; color: #0B1220;'>Análisis de Margen y Rentabilidad</h2>", unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("<b>Margen de Utilidad (%) por Categoría</b>", unsafe_allow_html=True)
        cat_mg = df_curr.groupby('Categoria').apply(lambda x: (x['Utilidad_Soles'].sum()/x['Ventas_Soles'].sum()*100) if x['Ventas_Soles'].sum()>0 else 0).reset_index(name='Margen_%')
        
        fig_mg_cat = go.Figure(go.Bar(
            x=cat_mg['Categoria'],
            y=cat_mg['Margen_%'],
            marker=dict(color='#10B981', cornerradius=6),
            text=[f"{m:.1f}%" for m in cat_mg['Margen_%']],
            textposition='auto',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_mg_cat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=300,
            xaxis=dict(tickfont=dict(color='#6B7280', size=11), showgrid=False),
            yaxis=dict(title=dict(text="Margen de Utilidad (%)", font=dict(color='#0B1220', size=11)), tickfont=dict(color='#6B7280', size=11), showgrid=True, gridcolor='#E2E8F0')
        )
        st.plotly_chart(fig_mg_cat, use_container_width=True)

    with col_r2:
        st.markdown("<b>Ventas vs. Utilidad Neta por Producto</b>", unsafe_allow_html=True)
        prod_prof = df_curr.groupby('Producto')[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
        
        fig_scat = go.Figure(go.Scatter(
            x=prod_prof['Ventas_Soles'],
            y=prod_prof['Utilidad_Soles'],
            mode='markers+text',
            text=prod_prof['Producto'],
            textposition='top center',
            textfont=dict(color='#0B1220', size=10),
            marker=dict(size=12, color='#6C5CE7', line=dict(color='#00C2D1', width=1.5))
        ))
        fig_scat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=300,
            xaxis=dict(title=dict(text="Ventas Totales (S/)", font=dict(color='#0B1220', size=11)), tickfont=dict(color='#6B7280', size=11), showgrid=True, gridcolor='#E2E8F0'),
            yaxis=dict(title=dict(text="Utilidad Neta (S/)", font=dict(color='#0B1220', size=11)), tickfont=dict(color='#6B7280', size=11), showgrid=True, gridcolor='#E2E8F0')
        )
        st.plotly_chart(fig_scat, use_container_width=True)

# ---------------------------------------------------------
# MODULO 05: ANÁLISIS
# ---------------------------------------------------------
elif modulo_sel == "05. Análisis":
    st.markdown("<h2 style='font-family: 'Space Grotesk', sans-serif; color: #0B1220;'>Inteligencia Comercial Avanzada</h2>", unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("<b>Mapa de Calor: Ventas por Canal y Categoría</b>", unsafe_allow_html=True)
        pv = df_curr.pivot_table(index='Categoria', columns='Canal_Venta', values='Ventas_Soles', aggfunc='sum').fillna(0)
        
        fig_hm = go.Figure(go.Heatmap(
            z=pv.values,
            x=pv.columns,
            y=pv.index,
            colorscale=[[0, '#F8FAFC'], [0.5, '#00C2D1'], [1, '#0E1B2E']],
            text=np.round(pv.values, 0),
            texttemplate='S/ %{text:,.0f}',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_hm.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            xaxis=dict(tickfont=dict(color='#6B7280', size=11)),
            yaxis=dict(tickfont=dict(color='#0B1220', size=11))
        )
        st.plotly_chart(fig_hm, use_container_width=True)

    with col_a2:
        st.markdown("<b>Estructura de Ingresos y Costos Operativos</b>", unsafe_allow_html=True)
        cost_df = pd.DataFrame({
            'Concepto': ['Ventas Totales', 'Costo de Ventas', 'Utilidad Neta'],
            'Monto': [vtas_curr, vtas_curr - util_curr, util_curr]
        })
        fig_cost = go.Figure(go.Bar(
            x=cost_df['Concepto'],
            y=cost_df['Monto'],
            marker=dict(color=['#00C2D1', '#F59E0B', '#10B981'], cornerradius=6),
            text=[f"S/ {v:,.2f}" for v in cost_df['Monto']],
            textposition='auto',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_cost.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            xaxis=dict(tickfont=dict(color='#6B7280', size=11), showgrid=False),
            yaxis=dict(title=dict(text="Monto en Soles (S/)", font=dict(color='#0B1220', size=11)), tickfont=dict(color='#6B7280', size=11), showgrid=True, gridcolor='#E2E8F0')
        )
        st.plotly_chart(fig_cost, use_container_width=True)

# ---------------------------------------------------------
# MODULO 06: SIMULADOR
# ---------------------------------------------------------
elif modulo_sel == "06. Simulador":
    st.markdown("<h2 style='font-family: 'Space Grotesk', sans-serif; color: #0B1220;'>Simulador Financiero MYPE Interactivo</h2>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([1, 1.2])
    with col_s1:
        st.markdown("<b>Parámetros de Proyección</b>", unsafe_allow_html=True)
        var_precio = st.slider("Variación en Precios (%):", -20, 30, 5, step=1)
        var_volumen = st.slider("Variación en Volumen (%):", -30, 50, 10, step=5)
        var_costo = st.slider("Variación en Costos de Compra (%):", -20, 20, 0, step=1)
        
        sim_sales = vtas_curr * (1 + var_precio/100) * (1 + var_volumen/100)
        sim_cost = (vtas_curr - util_curr) * (1 + var_costo/100) * (1 + var_volumen/100)
        sim_profit = sim_sales - sim_cost
        sim_mg = (sim_profit / sim_sales * 100) if sim_sales > 0 else 0
        
        st.markdown(f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 16px; border-radius: 12px; margin-top: 15px;">
            <div style="font-size: 13px; color: #6B7280;">Utilidad Proyectada:</div>
            <div style="font-size: 26px; font-weight: 800; color: #059669;">S/ {sim_profit:,.2f}</div>
            <div style="font-size: 13px; color: #0B1220;">Margen Proyectado: <b>{sim_mg:.1f}%</b></div>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown("<b>Comparativa: Actual vs. Proyectado</b>", unsafe_allow_html=True)
        sim_data = pd.DataFrame({
            'Métrica': ['Ventas (S/)', 'Costo (S/)', 'Utilidad Neta (S/)'],
            'Actual': [vtas_curr, vtas_curr - util_curr, util_curr],
            'Proyectado': [sim_sales, sim_cost, sim_profit]
        })
        
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Bar(
            name='Actual',
            x=sim_data['Métrica'],
            y=sim_data['Actual'],
            marker=dict(color='#64748B', cornerradius=6),
            text=[f"S/ {v:,.0f}" for v in sim_data['Actual']],
            textposition='auto',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_sim.add_trace(go.Bar(
            name='Proyectado',
            x=sim_data['Métrica'],
            y=sim_data['Proyectado'],
            marker=dict(color='#00C2D1', cornerradius=6),
            text=[f"S/ {v:,.0f}" for v in sim_data['Proyectado']],
            textposition='auto',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_sim.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            xaxis=dict(tickfont=dict(color='#6B7280', size=11), showgrid=False),
            yaxis=dict(title=dict(text="Monto (S/)", font=dict(color='#0B1220', size=11)), tickfont=dict(color='#6B7280', size=11), showgrid=True, gridcolor='#E2E8F0'),
            legend=dict(font=dict(color='#0B1220', size=11))
        )
        st.plotly_chart(fig_sim, use_container_width=True)

st.markdown("<hr style='margin-top: 40px; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-size: 12px; color: #6B7280;'>NexData SaaS Platform v2.5 | Panel de Inteligencia Empresarial para MYPES</div>", unsafe_allow_html=True)
