import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import io

# -----------------------------------------------------------------------------
# 0. CONFIGURACIÓN DE PÁGINA Y FUERZA DE TEMA CLARO (LIGHT MODE)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NEXDATA - Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Integrales: Garantizan contraste 100% claro, letra oscura sobre fondo claro
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Forzar fondo general claro y letra oscura */
    :root {
        --background-color: #F8FAFC !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #0F172A !important;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    /* Ocultar elementos innecesarios */
    header[data-testid="stHeader"] { background-color: rgba(248, 250, 252, 0.9) !important; }
    footer { visibility: hidden !important; }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }

    /* Forzar texto oscuro en Selectbox, Radio y Dropdowns */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="popover"], div[role="listbox"], div[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    div[role="option"]:hover {
        background-color: #EFF6FF !important;
        color: #2563EB !important;
    }
    .stSelectbox label, .stRadio label, .stFileUploader label {
        color: #1E293B !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }

    /* Opciones de navegación (Radio) estilizadas y visibles */
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        color: #334155 !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
        display: block !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background-color: #EFF6FF !important;
        color: #2563EB !important;
        border-color: #BFDBFE !important;
    }

    /* Títulos y párrafos */
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
    p, span, div, label {
        color: #1E293B;
    }

    /* Logo Sidebar */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 5px 0px 20px 0px;
    }
    .logo-box {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 20px;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }
    .logo-text {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A !important;
        letter-spacing: -0.5px;
    }

    /* Tarjeta inferior Sidebar */
    .sidebar-card {
        background-color: #F0F9FF !important;
        border: 1px solid #BAE6FD !important;
        border-radius: 12px;
        padding: 14px;
        margin-top: 25px;
    }
    .sidebar-card-title {
        font-size: 13px;
        font-weight: 700;
        color: #0369A1 !important;
    }
    .sidebar-card-sub {
        font-size: 11px;
        color: #0284C7 !important;
        margin-top: 4px;
    }

    /* Tarjetas KPI */
    .kpi-card-box {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .kpi-head {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }
    .kpi-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .kpi-label-text {
        font-size: 13px;
        font-weight: 700;
        color: #64748B !important;
    }
    .kpi-val-text {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A !important;
        margin: 4px 0;
        letter-spacing: -0.5px;
    }
    .kpi-delta-pos {
        font-size: 12px;
        font-weight: 700;
        color: #16A34A !important;
    }
    .kpi-delta-neg {
        font-size: 12px;
        font-weight: 700;
        color: #DC2626 !important;
    }

    /* Cards de Contenido */
    .content-box {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .box-title {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 2px;
    }
    .box-sub {
        font-size: 12px;
        color: #64748B !important;
        margin-bottom: 15px;
    }

    /* Pestañas (Tabs) */
    button[data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563EB !important;
        border-bottom-color: #2563EB !important;
    }

    /* Badges de Alertas */
    .alert-card-warning {
        background-color: #FFFBEB !important;
        border: 1px solid #FDE68A !important;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }
    .alert-card-success {
        background-color: #F0FDF4 !important;
        border: 1px solid #BBF7D0 !important;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }
    .alert-card-title {
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .alert-card-text {
        font-size: 12px;
        color: #334155 !important;
        line-height: 1.4;
    }

    /* Tablas / DataFrames */
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. CARGA ROBUSTA DE DATOS (CSV O EXCEL CON FALLBACK AUTOMÁTICO)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data_from_file(file_bytes, filename):
    try:
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding='utf-8')
            except Exception:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding='latin-1', sep=None, engine='python')
        else:
            df = pd.read_excel(io.BytesIO(file_bytes))

        # Normalizar nombres de columnas
        col_map = {}
        for c in df.columns:
            c_clean = str(c).strip().lower()
            if any(k in c_clean for k in ['fecha', 'date', 'day', 'día']):
                col_map[c] = 'Fecha'
            elif any(k in c_clean for k in ['ventas_soles', 'ventas', 'monto', 'sales', 'ingresos', 'precio_total']):
                col_map[c] = 'Ventas_Soles'
            elif any(k in c_clean for k in ['costo_soles', 'costo', 'cost', 'costos']):
                col_map[c] = 'Costo_Soles'
            elif any(k in c_clean for k in ['utilidad_soles', 'utilidad', 'profit', 'ganancia', 'margen_soles']):
                col_map[c] = 'Utilidad_Soles'
            elif any(k in c_clean for k in ['producto', 'product', 'item', 'descripcion', 'artículo']):
                col_map[c] = 'Producto'
            elif any(k in c_clean for k in ['categoria', 'category', 'rubro', 'tipo']):
                col_map[c] = 'Categoria'
            elif any(k in c_clean for k in ['canal_venta', 'canal', 'channel', 'medio']):
                col_map[c] = 'Canal_Venta'
            elif any(k in c_clean for k in ['cantidad', 'quantity', 'unidades', 'units', 'qty']):
                col_map[c] = 'Cantidad'

        df = df.rename(columns=col_map)

        # Verificar / Crear columnas obligatorias faltantes
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df = df.dropna(subset=['Fecha'])
        else:
            df['Fecha'] = pd.date_range(end=pd.Timestamp.now(), periods=len(df), freq='D')

        if 'Ventas_Soles' not in df.columns:
            num_cols = df.select_dtypes(include=[np.number]).columns
            if len(num_cols) > 0:
                df['Ventas_Soles'] = df[num_cols[0]]
            else:
                df['Ventas_Soles'] = 100.0

        if 'Costo_Soles' not in df.columns:
            df['Costo_Soles'] = df['Ventas_Soles'] * 0.7

        if 'Utilidad_Soles' not in df.columns:
            df['Utilidad_Soles'] = df['Ventas_Soles'] - df['Costo_Soles']

        if 'Producto' not in df.columns:
            df['Producto'] = 'Producto General'

        if 'Categoria' not in df.columns:
            df['Categoria'] = 'General'

        if 'Canal_Venta' not in df.columns:
            df['Canal_Venta'] = 'Tienda física'

        if 'Cantidad' not in df.columns:
            df['Cantidad'] = 1

        return df, filename
    except Exception as e:
        return None, str(e)

def load_default_data():
    # Buscar archivo predeterminado en rutas conocidas
    paths = [
        "/workspace/scratch/dataset_mype_transacciones.csv",
        "/workspace/artifacts/dataset_mype_transacciones.csv",
        "dataset_mype_transacciones.csv"
    ]
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            return df, "Dataset MYPE Predeterminado"

    # Fallback autogenerado si no existe el archivo local
    dates = pd.date_range(start="2026-08-01", periods=60, freq='D')
    np.random.seed(42)
    rows = []
    prods = [
        ("Arroz Costeño 5kg", "Alimentos", 24.50, 18.00),
        ("Aceite Primor 1L", "Alimentos", 11.50, 8.50),
        ("Leche Gloria 400g", "Alimentos", 4.80, 3.80),
        ("Inca Kola 1.5L", "Bebidas", 7.50, 5.20),
        ("Cerveza Cusqueña", "Bebidas", 9.00, 6.50),
        ("Detergente Opal 1kg", "Limpieza", 12.00, 8.80),
        ("Jabón Camay", "Higiene", 3.50, 2.20),
        ("Galletas Soda Field", "Otros", 2.50, 1.50)
    ]
    canales = ["Tienda física", "Delivery", "Online", "Otros"]
    for d in dates:
        for _ in range(np.random.randint(5, 15)):
            p_name, cat, p_val, c_val = prods[np.random.randint(0, len(prods))]
            qty = np.random.randint(1, 5)
            v_soles = qty * p_val
            c_soles = qty * c_val
            u_soles = v_soles - c_soles
            canal = np.random.choice(canales, p=[0.45, 0.30, 0.15, 0.10])
            rows.append({
                'Fecha': d,
                'Producto': p_name,
                'Categoria': cat,
                'Canal_Venta': canal,
                'Cantidad': qty,
                'Precio_Unitario': p_val,
                'Ventas_Soles': v_soles,
                'Costo_Soles': c_soles,
                'Utilidad_Soles': u_soles
            })
    df_gen = pd.DataFrame(rows)
    return df_gen, "Dataset Autogenerado MYPE"

# -----------------------------------------------------------------------------
# 2. BARRA LATERAL (OPERATIVA, FILTROS Y NAVEGACIÓN)
# -----------------------------------------------------------------------------
with st.sidebar:
    # Logo NEXDATA
    st.markdown("""
        <div class="sidebar-logo">
            <div class="logo-box">N</div>
            <div class="logo-text">NEXDATA</div>
        </div>
    """, unsafe_allow_html=True)

    # Cargador de Archivos opcional
    uploaded_file = st.file_uploader("📂 Cargar Excel / CSV (Opcional)", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        df_loaded, source_name = load_data_from_file(file_bytes, uploaded_file.name)
        if df_loaded is None:
            st.error(f"Error al leer archivo: {source_name}")
            df_raw, source_name = load_default_data()
        else:
            df_raw = df_loaded
    else:
        df_raw, source_name = load_default_data()

    st.markdown("---")
    st.markdown("<p style='font-weight:700; font-size:13px; color:#475569; margin-bottom:8px;'>MENÚ DE NAVEGACIÓN</p>", unsafe_allow_html=True)

    menu_opt = st.radio(
        "Navegación",
        ["Inicio", "Ventas", "Productos", "Rentabilidad", "Análisis", "Simulador"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<p style='font-weight:700; font-size:13px; color:#475569; margin-bottom:8px;'>🔍 FILTROS DE NEGOCIO</p>", unsafe_allow_html=True)

    # Filtro Periodo
    periodo_opt = st.selectbox(
        "Periodo:",
        ["Últimos 30 días", "Este Mes", "Último Trimestre", "Todo el Registro"],
        index=0
    )

    # Lógica de fechas
    max_date = df_raw['Fecha'].max()
    min_date = df_raw['Fecha'].min()

    if periodo_opt == "Últimos 30 días":
        fecha_fin = max_date
        fecha_ini = max_date - pd.Timedelta(days=30)
        fecha_fin_prev = fecha_ini - pd.Timedelta(days=1)
        fecha_ini_prev = fecha_fin_prev - pd.Timedelta(days=30)
    elif periodo_opt == "Este Mes":
        fecha_fin = max_date
        fecha_ini = pd.Timestamp(max_date.year, max_date.month, 1)
        fecha_fin_prev = fecha_ini - pd.Timedelta(days=1)
        fecha_ini_prev = pd.Timestamp(fecha_fin_prev.year, fecha_fin_prev.month, 1)
    elif periodo_opt == "Último Trimestre":
        fecha_fin = max_date
        fecha_ini = max_date - pd.Timedelta(days=90)
        fecha_fin_prev = fecha_ini - pd.Timedelta(days=1)
        fecha_ini_prev = fecha_fin_prev - pd.Timedelta(days=90)
    else:
        fecha_ini = min_date
        fecha_fin = max_date
        fecha_ini_prev = min_date
        fecha_fin_prev = max_date

    # Filtro Categoría
    cats_all = ["Todas"] + sorted(list(df_raw['Categoria'].dropna().unique()))
    cat_sel = st.selectbox("Categoría:", cats_all, index=0)

    # Filtro Producto
    if cat_sel != "Todas":
        prods_all = ["Todos"] + sorted(list(df_raw[df_raw['Categoria'] == cat_sel]['Producto'].dropna().unique()))
    else:
        prods_all = ["Todos"] + sorted(list(df_raw['Producto'].dropna().unique()))
    prod_sel = st.selectbox("Producto:", prods_all, index=0)

    # Filtro Canal de Venta
    canales_all = ["Todos"] + sorted(list(df_raw['Canal_Venta'].dropna().unique()))
    canal_sel = st.selectbox("Canal de Venta:", canales_all, index=0)

    st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-card-title">💡 Tu negocio, en mejores decisiones</div>
            <div class="sidebar-card-sub">NEXDATA SaaS | Analítica para MYPES</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. FILTRADO DINÁMICO DE DATOS (ACTUAL Y ANTERIOR PARA COMPARATIVA)
# -----------------------------------------------------------------------------
def filter_dataframe(df, f_ini, f_fin, cat, prod, canal):
    dff = df[(df['Fecha'] >= f_ini) & (df['Fecha'] <= f_fin)].copy()
    if cat != "Todas":
        dff = dff[dff['Categoria'] == cat]
    if prod != "Todos":
        dff = dff[dff['Producto'] == prod]
    if canal != "Todos":
        dff = dff[dff['Canal_Venta'] == canal]
    return dff

df_curr = filter_dataframe(df_raw, fecha_ini, fecha_fin, cat_sel, prod_sel, canal_sel)
df_prev = filter_dataframe(df_raw, fecha_ini_prev, fecha_fin_prev, cat_sel, prod_sel, canal_sel)

# Cálculo de KPIs
vtas_curr = df_curr['Ventas_Soles'].sum()
vtas_prev = df_prev['Ventas_Soles'].sum()
delta_vtas = ((vtas_curr - vtas_prev) / vtas_prev * 100) if vtas_prev > 0 else 0.0

qty_curr = df_curr['Cantidad'].sum()
qty_prev = df_prev['Cantidad'].sum()
delta_qty = ((qty_curr - qty_prev) / qty_prev * 100) if qty_prev > 0 else 0.0

tx_curr = len(df_curr)
tx_prev = len(df_prev)
delta_tx = ((tx_curr - tx_prev) / tx_prev * 100) if tx_prev > 0 else 0.0

util_curr = df_curr['Utilidad_Soles'].sum()
util_prev = df_prev['Utilidad_Soles'].sum()

mg_curr = (util_curr / vtas_curr * 100) if vtas_curr > 0 else 0.0
mg_prev = (util_prev / vtas_prev * 100) if vtas_prev > 0 else 0.0
delta_mg = mg_curr - mg_prev

ticket_curr = (vtas_curr / tx_curr) if tx_curr > 0 else 0.0
ticket_prev = (vtas_prev / tx_prev) if tx_prev > 0 else 0.0
delta_ticket = ((ticket_curr - ticket_prev) / ticket_prev * 100) if ticket_prev > 0 else 0.0

# -----------------------------------------------------------------------------
# 4. ENCABEZADO Y KPI CARDS (RÉPLICA FIEL DE INTERFAZ)
# -----------------------------------------------------------------------------
c_head_left, c_head_right = st.columns([2.5, 1])

with c_head_left:
    st.markdown("""
        <div>
            <h1 style="font-size: 28px; margin: 0; padding: 0;">¡Hola, <span style="color: #2563EB;">Milagros</span>!</h1>
            <p style="font-size: 14px; color: #64748B; margin-top: 4px;">Aquí tienes un resumen del rendimiento de tu negocio.</p>
        </div>
    """, unsafe_allow_html=True)

with c_head_right:
    st.markdown(f"""
        <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:10px; padding:8px 12px; text-align:right;">
            <div style="font-size:11px; font-weight:700; color:#1E40AF;">📌 {source_name}</div>
            <div style="font-size:12px; font-weight:800; color:#1D4ED8;">{len(df_curr)} registros en periodo</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# 4 TARJETAS KPI
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
        <div class="kpi-card-box">
            <div class="kpi-head">
                <div class="kpi-icon" style="background-color:#EFF6FF; color:#2563EB;">🛒</div>
                <div class="kpi-label-text">Ventas Totales</div>
            </div>
            <div class="kpi-val-text">S/ {vtas_curr:,.2f}</div>
            <div class="{'kpi-delta-pos' if delta_vtas >= 0 else 'kpi-delta-neg'}">
                {'↑' if delta_vtas >= 0 else '↓'} {abs(delta_vtas):.1f}% <span style="color:#64748B; font-weight:500;">vs. periodo anterior</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
        <div class="kpi-card-box">
            <div class="kpi-head">
                <div class="kpi-icon" style="background-color:#F3E8FF; color:#9333EA;">📦</div>
                <div class="kpi-label-text">Productos Vendidos</div>
            </div>
            <div class="kpi-val-text">{qty_curr:,} un.</div>
            <div class="{'kpi-delta-pos' if delta_qty >= 0 else 'kpi-delta-neg'}">
                {'↑' if delta_qty >= 0 else '↓'} {abs(delta_qty):.1f}% <span style="color:#64748B; font-weight:500;">vs. periodo anterior</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
        <div class="kpi-card-box">
            <div class="kpi-head">
                <div class="kpi-icon" style="background-color:#DCFCE7; color:#16A34A;">👤</div>
                <div class="kpi-label-text">Clientes Atendidos</div>
            </div>
            <div class="kpi-val-text">{tx_curr:,} tx</div>
            <div class="{'kpi-delta-pos' if delta_tx >= 0 else 'kpi-delta-neg'}">
                {'↑' if delta_tx >= 0 else '↓'} {abs(delta_tx):.1f}% <span style="color:#64748B; font-weight:500;">vs. periodo anterior</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
        <div class="kpi-card-box">
            <div class="kpi-head">
                <div class="kpi-icon" style="background-color:#FFEDD5; color:#EA580C;">💲</div>
                <div class="kpi-label-text">Rentabilidad</div>
            </div>
            <div class="kpi-val-text">{mg_curr:.1f}%</div>
            <div class="{'kpi-delta-pos' if delta_mg >= 0 else 'kpi-delta-neg'}">
                {'↑' if delta_mg >= 0 else '↓'} {abs(delta_mg):.1f} pp <span style="color:#64748B; font-weight:500;">vs. periodo anterior</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. VISTAS DE PÁGINA SEGÚN SELECCIÓN DE NAVEGACIÓN
# -----------------------------------------------------------------------------

# VISTA 1: INICIO
if menu_opt == "Inicio":
    # Fila Central de Gráficos
    col_chart_left, col_chart_right = st.columns([1.8, 1.2])

    with col_chart_left:
        st.markdown("""
            <div class="content-box">
                <div class="box-title">📈 Evolución de Ventas</div>
                <div class="box-sub">Ventas diarias en el periodo seleccionado</div>
            </div>
        """, unsafe_allow_html=True)

        if not df_curr.empty:
            df_daily = df_curr.groupby(df_curr['Fecha'].dt.strftime('%d %b'))[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_daily['Fecha'],
                y=df_daily['Ventas_Soles'],
                mode='lines+markers',
                line=dict(color='#2563EB', width=3, shape='spline'),
                marker=dict(size=6, color='#2563EB', line=dict(color='#FFFFFF', width=2)),
                fill='tozeroy',
                fillcolor='rgba(37, 99, 235, 0.08)',
                name='Ventas (S/)'
            ))
            fig_line.update_layout(
                height=280,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#0F172A', family='Plus Jakarta Sans'),
                xaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#0F172A', size=11)),
                yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#0F172A', size=11)),
                showlegend=False
            )
            st.plotly_chart(fig_line, use_container_width=True, key="chart_evo_inicio")
        else:
            st.info("No hay datos en el rango seleccionado.")

    with col_chart_right:
        st.markdown("""
            <div class="content-box">
                <div class="box-title">📊 Ventas por Categoría</div>
                <div class="box-sub">Distribución de ventas por categoría</div>
            </div>
        """, unsafe_allow_html=True)

        if not df_curr.empty:
            df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
            fig_donut = go.Figure(data=[go.Pie(
                labels=df_cat['Categoria'],
                values=df_cat['Ventas_Soles'],
                hole=0.68,
                marker=dict(colors=['#2563EB', '#8B5CF6', '#10B981', '#F97316', '#06B6D4', '#E11D48']),
                textinfo='none',
                hoverinfo='label+value+percent'
            )])
            fig_donut.add_annotation(
                text=f"<b style='font-size:18px;color:#0F172A;'>S/ {vtas_curr:,.0f}</b><br><span style='font-size:12px;color:#64748B;'>Total ventas</span>",
                x=0.5, y=0.5, showarrow=False
            )
            fig_donut.update_layout(
                height=280,
                margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#0F172A', family='Plus Jakarta Sans'),
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.75, font=dict(color='#0F172A', size=11))
            )
            st.plotly_chart(fig_donut, use_container_width=True, key="chart_donut_inicio")

    # Fila Inferior (3 Columnas)
    bot_c1, bot_c2, bot_c3 = st.columns(3)

    with bot_c1:
        st.markdown("""
            <div class="content-box">
                <div class="box-title">📦 Productos Más Vendidos</div>
                <div class="box-sub">Top 5 por volumen de ventas</div>
            </div>
        """, unsafe_allow_html=True)
        if not df_curr.empty:
            top_p = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=False).head(5).reset_index()
            max_p = top_p['Cantidad'].max() if len(top_p) > 0 and top_p['Cantidad'].max() > 0 else 1
            colors_p = ['#2563EB', '#10B981', '#8B5CF6', '#F97316', '#06B6D4']
            for i, r in top_p.iterrows():
                pct = (r['Cantidad'] / max_p) * 100
                st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; color:#0F172A; margin-bottom:4px;">
                            <span>{i+1}. {r['Producto']}</span>
                            <span>{r['Cantidad']} un.</span>
                        </div>
                        <div style="background-color:#F1F5F9; border-radius:6px; height:8px; width:100%; overflow:hidden;">
                            <div style="height:100%; width:{pct}%; background-color:{colors_p[i % len(colors_p)]}; border-radius:6px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    with bot_c2:
        st.markdown("""
            <div class="content-box">
                <div class="box-title">📢 Canales de Venta</div>
                <div class="box-sub">Participación por canal comercial</div>
            </div>
        """, unsafe_allow_html=True)
        if not df_curr.empty:
            df_chan = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
            fig_pie = go.Figure(data=[go.Pie(
                labels=df_chan['Canal_Venta'],
                values=df_chan['Ventas_Soles'],
                hole=0,
                marker=dict(colors=['#2563EB', '#10B981', '#8B5CF6', '#F97316']),
                textinfo='percent',
                textfont=dict(size=12, color='#FFFFFF')
            )])
            fig_pie.update_layout(
                height=220,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#0F172A', family='Plus Jakarta Sans'),
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.8, font=dict(color='#0F172A', size=11))
            )
            st.plotly_chart(fig_pie, use_container_width=True, key="chart_chan_inicio")

    with bot_c3:
        st.markdown("""
            <div class="content-box">
                <div class="box-title">🔔 Alertas y Recomendaciones</div>
                <div class="box-sub">Sugerencias del motor de inteligencia MYPE</div>
                <div class="alert-card-warning">
                    <div class="alert-card-title" style="color:#92400E;">⚠️ Alerta de Inventario</div>
                    <div class="alert-card-text">Alta demanda detectada en fines de semana. Reabastecer stock de alimentos de alta rotación los días jueves.</div>
                </div>
                <div class="alert-card-success">
                    <div class="alert-card-title" style="color:#166534;">✅ Oportunidad Comercial</div>
                    <div class="alert-card-text">El canal digital representa el 30% de tus ventas. Promocionar Yape/Plin en mostrador para elevar el ticket promedio.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# VISTA 2: VENTAS
elif menu_opt == "Ventas":
    st.markdown("### 🛒 Análisis Detallado de Ventas")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.subheader("Evolución de Ingresos y Utilidad")
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
        fig_v = go.Figure()
        fig_v.add_trace(go.Bar(x=df_daily['Fecha'], y=df_daily['Ventas_Soles'], name='Ventas (S/)', marker_color='#2563EB'))
        fig_v.add_trace(go.Bar(x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'], name='Utilidad (S/)', marker_color='#10B981'))
        fig_v.update_layout(
            barmode='group', height=350,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#0F172A'),
            legend=dict(font=dict(color='#0F172A'))
        )
        st.plotly_chart(fig_v, use_container_width=True, key="chart_ventas_detail")

    with col_v2:
        st.subheader("Ventas por Canal Comercial")
        df_chan_detail = df_curr.groupby('Canal_Venta')[['Ventas_Soles', 'Cantidad']].sum().reset_index()
        fig_c = px.bar(df_chan_detail, x='Canal_Venta', y='Ventas_Soles', color='Canal_Venta', text_auto='.2f')
        fig_c.update_layout(
            height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#0F172A'), showlegend=False
        )
        st.plotly_chart(fig_c, use_container_width=True, key="chart_chan_detail")

    st.subheader("📋 Registro de Transacciones Filtradas")
    st.dataframe(df_curr[['Fecha', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Ventas_Soles', 'Utilidad_Soles']], use_container_width=True)

# VISTA 3: PRODUCTOS
elif menu_opt == "Productos":
    st.markdown("### 📦 Rendimiento de Productos e Inventarios")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.subheader("Top 10 Productos por Facturación (S/)")
        df_p_sales = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10)
        fig_p1 = px.bar(x=df_p_sales.values, y=df_p_sales.index, orientation='h', color_discrete_sequence=['#2563EB'])
        fig_p1.update_layout(
            height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#0F172A'), xaxis_title="Ventas Totales (S/)", yaxis_title="Producto"
        )
        st.plotly_chart(fig_p1, use_container_width=True, key="chart_prod_sales")

    with col_p2:
        st.subheader("Top 10 Productos por Margen de Rentabilidad (%)")
        df_p_mg = df_curr.groupby('Producto').apply(
            lambda x: (x['Utilidad_Soles'].sum() / x['Ventas_Soles'].sum() * 100) if x['Ventas_Soles'].sum() > 0 else 0
        ).sort_values(ascending=True).tail(10)
        fig_p2 = px.bar(x=df_p_mg.values, y=df_p_mg.index, orientation='h', color_discrete_sequence=['#10B981'])
        fig_p2.update_layout(
            height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#0F172A'), xaxis_title="Margen (%)", yaxis_title="Producto"
        )
        st.plotly_chart(fig_p2, use_container_width=True, key="chart_prod_margin")

# VISTA 4: RENTABILIDAD
elif menu_opt == "Rentabilidad":
    st.markdown("### 💲 Análisis de Rentabilidad y Márgenes")
    df_cat_prof = df_curr.groupby('Categoria').agg(
        Ventas=('Ventas_Soles', 'sum'),
        Costo=('Costo_Soles', 'sum'),
        Utilidad=('Utilidad_Soles', 'sum'),
        Unidades=('Cantidad', 'sum')
    ).reset_index()
    df_cat_prof['Margen_%'] = (df_cat_prof['Utilidad'] / df_cat_prof['Ventas'] * 100).round(1)

    fig_prof = px.bar(df_cat_prof, x='Categoria', y=['Ventas', 'Costo', 'Utilidad'], barmode='group',
                      title="Estructura Financiera por Categoría",
                      color_discrete_sequence=['#2563EB', '#DC2626', '#10B981'])
    fig_prof.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#0F172A'))
    st.plotly_chart(fig_prof, use_container_width=True, key="chart_rentabilidad")

    st.subheader("Matriz de Rotación por Categoría")
    st.dataframe(df_cat_prof, use_container_width=True)

# VISTA 5: ANÁLISIS
elif menu_opt == "Análisis":
    st.markdown("### 🔬 Análisis Multidimensional de Negocio")
    if 'Dia_Semana' in df_curr.columns:
        df_dow = df_curr.groupby('Dia_Semana')['Ventas_Soles'].sum().reset_index()
        fig_dow = px.bar(df_dow, x='Dia_Semana', y='Ventas_Soles', title="Ventas por Día de la Semana", color_discrete_sequence=['#8B5CF6'])
        fig_dow.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#0F172A'))
        st.plotly_chart(fig_dow, use_container_width=True, key="chart_dow")
    else:
        st.info("El dataset no incluye la columna 'Dia_Semana'.")

# VISTA 6: SIMULADOR
elif menu_opt == "Simulador":
    st.markdown("### 🎯 Simulador de Escenarios Comerciales para tu MYPE")
    st.markdown("Ajusta los parámetros para simular el impacto en tus ingresos y ganancias.")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        inc_sales = st.slider("Incremento proyectado en ventas (%)", 0, 50, 15)
        red_cost = st.slider("Reducción de costos por compras eficientes (%)", 0, 30, 10)
        plan_cost = st.selectbox("Plan de Suscripción SaaS", ["Plan Básico (S/ 50/mes)", "Plan Premium (S/ 150/mes)"])

    plan_price = 50.0 if "50" in plan_cost else 150.0
    sim_sales = vtas_curr * (1 + inc_sales / 100.0)
    sim_cost = (vtas_curr - util_curr) * (1 - red_cost / 100.0)
    sim_profit = sim_sales - sim_cost - plan_price
    net_benefit = sim_profit - util_curr
    roi = (net_benefit / plan_price * 100) if plan_price > 0 else 0

    with col_s2:
        st.markdown(f"""
            <div class="content-box" style="background:#F0FDF4; border-color:#BBF7D0;">
                <h3 style="color:#166534; margin-top:0;">Proyección de Resultados Simulados</h3>
                <p><b>Ventas Proyectadas:</b> S/ {sim_sales:,.2f}</p>
                <p><b>Costo Operativo Proyectado:</b> S/ {sim_cost:,.2f}</p>
                <p><b>Costo de Suscripción SaaS:</b> S/ {plan_price:,.2f} / mes</p>
                <hr>
                <h2 style="color:#15803D; margin:5px 0;">Utilidad Proyectada: S/ {sim_profit:,.2f} / mes</h2>
                <p style="font-size:14px; font-weight:700; color:#166534;">Ganancia Neta Adicional: +S/ {net_benefit:,.2f} / mes</p>
                <p style="font-size:14px; font-weight:800; color:#2563EB;">Retorno de Inversión (ROI): {roi:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)

# Pie de página
st.markdown("---")
st.caption("NEXDATA SaaS Platform v2.5 | Panel de Inteligencia Empresarial para MYPES – Gestión por Resultados 2026")
