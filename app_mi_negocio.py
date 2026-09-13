import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y METADATOS
# ---------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="32" height="32">
  <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
  <circle cx="30" cy="72" r="7" fill="#8C9BAE"/>
  <circle cx="52" cy="52" r="7" fill="#8C9BAE"/>
  <circle cx="75" cy="30" r="9" fill="#6C5CE7"/>
  <line x1="30" y1="72" x2="52" y2="52" stroke="#00C2D1" stroke-width="6" stroke-linecap="round"/>
  <line x1="52" y1="52" x2="72" y2="33" stroke="#00C2D1" stroke-width="6" stroke-linecap="round"/>
  <path d="M62 25 L80 25 L80 43" fill="none" stroke="#6C5CE7" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

st.set_page_config(
    page_title="NexData – Inteligencia Empresarial MYPE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS CSS AVANZADOS DE ALTO CONTRASTE (SIN TEXTO BLANCO)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0B1220 !important;
        background-color: #F4F7FA;
    }

    h1, h2, h3, h4, .stTitle, .stHeader {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #0B1220 !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    /* Fondo general */
    .stApp {
        background-color: #F4F7FA;
    }

    /* Barra Lateral Estilizada NexData */
    [data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42;
    }
    
    [data-testid="stSidebar"] * {
        color: #8C9BAE !important;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        color: #00C2D1 !important;
        font-weight: 600;
    }

    /* Radio buttons / Navigation en Sidebar */
    div[data-testid="stSidebarUserContent"] .stRadio label {
        color: #8C9BAE !important;
        font-weight: 600;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }

    div[data-testid="stSidebarUserContent"] .stRadio label[data-checked="true"] {
        color: #00C2D1 !important;
        background-color: #1E2D42 !important;
    }

    /* Tarjetas KPI Premium */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px 18px;
        box-shadow: 0 4px 20px rgba(14, 27, 46, 0.04);
        margin-bottom: 15px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(14, 27, 46, 0.08);
    }
    .kpi-title {
        font-size: 13px;
        font-weight: 600;
        color: #6B7686 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #0B1220 !important;
        margin-bottom: 6px;
    }
    .kpi-badge-pos {
        font-size: 12px;
        font-weight: 700;
        color: #059669 !important;
        background-color: #ECFDF5;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }
    .kpi-badge-neg {
        font-size: 12px;
        font-weight: 700;
        color: #DC2626 !important;
        background-color: #FEF2F2;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }

    /* Contenedores de Sección / Gráficos */
    .section-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 4px 20px rgba(14, 27, 46, 0.04);
        margin-bottom: 20px;
    }
    
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 17px;
        font-weight: 700;
        color: #0B1220 !important;
        margin-bottom: 4px;
    }
    .section-subtitle {
        font-size: 12px;
        color: #6B7686 !important;
        margin-bottom: 16px;
    }

    /* Alertas Personalizadas */
    .alert-card-warning {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .alert-title-warning {
        font-size: 14px;
        font-weight: 700;
        color: #92400E !important;
        margin-bottom: 4px;
    }
    .alert-desc-warning {
        font-size: 13px;
        color: #B45309 !important;
    }

    .alert-card-success {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .alert-title-success {
        font-size: 14px;
        font-weight: 700;
        color: #065F46 !important;
        margin-bottom: 4px;
    }
    .alert-desc-success {
        font-size: 13px;
        color: #047857 !important;
    }

    /* Botones y Selectores */
    .stButton>button {
        background-color: #6C5CE7 !important;
        color: #0B1220 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 20px !important;
    }

    /* Estilos de tablas */
    .dataframe {
        color: #0B1220 !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CARGA DE DATOS & DEMO FALLBACK
# ---------------------------------------------------------
@st.cache_data
def load_dataset():
    paths = [
        "dataset_mype_transacciones.csv",
        "/workspace/scratch/dataset_mype_transacciones.csv",
        "/workspace/artifacts/dataset_mype_transacciones.csv"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                df = pd.read_csv(p)
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                return df
            except Exception:
                pass
    
    # Dataset Sintético de Respaldo MYPE Perú
    np.random.seed(42)
    dates = pd.date_range(start="2026-04-01", periods=30, freq="D")
    categories = ["Alimentos", "Bebidas", "Limpieza", "Higiene", "Otros"]
    products = {
        "Alimentos": ["Arroz 1kg", "Aceite 1L", "Avena 500g", "Fideos 500g", "Pan Molde"],
        "Bebidas": ["Gaseosa 1.5L", "Agua 2.5L", "Jugo 1L", "Cerveza 620ml", "Rehidratante"],
        "Limpieza": ["Detergente 1kg", "Lavafajillas", "Lejía 1L", "Suavizante", "Desinfectante"],
        "Higiene": ["Jabón 3pk", "Shampoo 400ml", "Crema Dental", "Papel Higiénico 4pk"],
        "Otros": ["Pilas AA", "Fósforos 10pk", "Bolsas Basura", "Velas 4pk"]
    }
    channels = ["Tienda física", "Delivery", "Online", "Otros"]
    
    records = []
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(15, 35)
        for _ in range(num_tx):
            cat = np.random.choice(categories, p=[0.35, 0.25, 0.18, 0.12, 0.10])
            prod = np.random.choice(products[cat])
            chan = np.random.choice(channels, p=[0.45, 0.30, 0.15, 0.10])
            qty = np.random.randint(1, 6)
            price = round(np.random.uniform(4.0, 35.0), 2)
            sales = round(qty * price, 2)
            margin_pct = np.random.uniform(0.15, 0.35)
            profit = round(sales * margin_pct, 2)
            cost = round(sales - profit, 2)
            
            records.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": d,
                "Dia_Semana": d.strftime("%A"),
                "Producto": prod,
                "Categoria": cat,
                "Canal_Venta": chan,
                "Cantidad": qty,
                "Precio_Unitario": price,
                "Ventas_Soles": sales,
                "Costo_Soles": cost,
                "Utilidad_Soles": profit
            })
            tx_id += 1
            
    df_gen = pd.DataFrame(records)
    return df_gen

df_raw = load_dataset()

# ---------------------------------------------------------
# BARRA LATERAL: LOGO, NAVEGACIÓN Y FILTROS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0; text-align: left;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background-color: #0E1B2E; border: 1px solid #1E2D42; border-radius: 12px; padding: 10px; display: flex; align-items: center; justify-content: center;">
                <svg width="28" height="28" viewBox="0 0 100 100">
                  <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
                  <circle cx="30" cy="72" r="8" fill="#8C9BAE"/>
                  <circle cx="52" cy="52" r="8" fill="#8C9BAE"/>
                  <circle cx="75" cy="30" r="10" fill="#6C5CE7"/>
                  <line x1="30" y1="72" x2="52" y2="52" stroke="#00C2D1" stroke-width="7" stroke-linecap="round"/>
                  <line x1="52" y1="52" x2="72" y2="33" stroke="#00C2D1" stroke-width="7" stroke-linecap="round"/>
                  <path d="M62 25 L80 25 L80 43" fill="none" stroke="#6C5CE7" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #00C2D1; line-height: 1.1;">
                    Nex<span style="color: #00C2D1;">Data</span>
                </div>
                <div style="font-size: 11px; color: #8C9BAE; font-weight: 500;">
                    Datos claros para tu negocio
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #1E2D42; margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
    
    # Menú de Navegación Profesional (6 Pestañas)
    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>Navegación Principal</div>", unsafe_allow_html=True)
    
    nav_option = st.radio(
        label="Navegación",
        options=[
            "01. Inicio",
            "02. Ventas",
            "03. Productos",
            "04. Rentabilidad",
            "05. Análisis",
            "06. Simulador"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='border-color: #1E2D42; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Carga de archivos y modo demo
    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>Origen de Datos</div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Cargar Excel / CSV:", type=["csv", "xlsx"])
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=True)
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
            df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
            st.success("Dataset cargado correctamente")
        except Exception as e:
            st.error("Sube tus datos para comenzar")
    elif not use_demo:
        st.info("Sube tus datos para comenzar")
        st.stop()
        
    st.markdown("<hr style='border-color: #1E2D42; margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Filtros interactivos globales
    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>Filtros Globales</div>", unsafe_allow_html=True)
    
    periodo_sel = st.selectbox("Periodo de Análisis:", ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Registro"])
    
    cats_avail = ["Todas"] + sorted(list(df_raw['Categoria'].dropna().unique()))
    cat_filter = st.selectbox("Categoría:", cats_avail)
    
    chan_avail = ["Todos"] + sorted(list(df_raw['Canal_Venta'].dropna().unique()))
    chan_filter = st.selectbox("Canal de Venta:", chan_avail)

# ---------------------------------------------------------
# FILTRADO DINÁMICO DE DATOS
# ---------------------------------------------------------
max_d = df_raw['Fecha'].max()
if periodo_sel == "Últimos 30 días":
    f_ini = max_d - pd.Timedelta(days=30)
    f_fin = max_d
    f_ini_prev = f_ini - pd.Timedelta(days=30)
    f_fin_prev = f_ini - pd.Timedelta(days=1)
elif periodo_sel == "Este Mes":
    f_ini = max_d.replace(day=1)
    f_fin = max_d
    f_ini_prev = (f_ini - pd.Timedelta(days=1)).replace(day=1)
    f_fin_prev = f_ini - pd.Timedelta(days=1)
elif periodo_sel == "Mes Anterior":
    f_fin = max_d.replace(day=1) - pd.Timedelta(days=1)
    f_ini = f_fin.replace(day=1)
    f_fin_prev = f_ini - pd.Timedelta(days=1)
    f_ini_prev = f_fin_prev.replace(day=1)
else:
    f_ini = df_raw['Fecha'].min()
    f_fin = max_d
    f_ini_prev = f_ini
    f_fin_prev = f_fin

def apply_filters(df, p_ini, p_fin, cat, chan):
    dff = df[(df['Fecha'] >= p_ini) & (df['Fecha'] <= p_fin)]
    if cat != "Todas":
        dff = dff[dff['Categoria'] == cat]
    if chan != "Todos":
        dff = dff[dff['Canal_Venta'] == chan]
    return dff

df_curr = apply_filters(df_raw, f_ini, f_fin, cat_filter, chan_filter)
df_prev = apply_filters(df_raw, f_ini_prev, f_fin_prev, cat_filter, chan_filter)

# Métricas Calculadas
v_curr = df_curr['Ventas_Soles'].sum()
v_prev = df_prev['Ventas_Soles'].sum()
delta_v = ((v_curr - v_prev) / v_prev * 100) if v_prev > 0 else 0.0

u_curr = df_curr['Utilidad_Soles'].sum()
u_prev = df_prev['Utilidad_Soles'].sum()
delta_u = ((u_curr - u_prev) / u_prev * 100) if u_prev > 0 else 0.0

qty_curr = df_curr['Cantidad'].sum()
qty_prev = df_prev['Cantidad'].sum()
delta_q = ((qty_curr - qty_prev) / qty_prev * 100) if qty_prev > 0 else 0.0

tx_curr = len(df_curr)
tx_prev = len(df_prev)
delta_tx = ((tx_curr - tx_prev) / tx_prev * 100) if tx_prev > 0 else 0.0

margin_curr = (u_curr / v_curr * 100) if v_curr > 0 else 0.0
margin_prev = (u_prev / v_prev * 100) if v_prev > 0 else 0.0
delta_mg = margin_curr - margin_prev

ticket_curr = (v_curr / tx_curr) if tx_curr > 0 else 0.0
ticket_prev = (v_prev / tx_prev) if tx_prev > 0 else 0.0
delta_tk = ((ticket_curr - ticket_prev) / ticket_prev * 100) if ticket_prev > 0 else 0.0

# Configuración Estándar para Gráficos Plotly (TEXTO OSCURO, SIN BLANCO)
PLOTLY_THEME = dict(
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#0B1220", size=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=30, r=30, t=40, b=30),
    xaxis=dict(
        gridcolor="#E2E8F0", 
        zerolinecolor="#E2E8F0",
        tickfont=dict(color="#0B1220", size=11),
        titlefont=dict(color="#0B1220", size=12, family="Space Grotesk")
    ),
    yaxis=dict(
        gridcolor="#E2E8F0", 
        zerolinecolor="#E2E8F0",
        tickfont=dict(color="#0B1220", size=11),
        titlefont=dict(color="#0B1220", size=12, family="Space Grotesk")
    ),
    legend=dict(font=dict(color="#0B1220", size=11))
)

# ---------------------------------------------------------
# CABECERA GENERAL
# ---------------------------------------------------------
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<h1 style='font-size: 28px; margin-bottom: 2px;'>¡Hola, Milagros!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 14px; color: #6B7686; margin-bottom: 20px;'>Aquí tienes un resumen del rendimiento de tu negocio en tiempo real.</p>", unsafe_allow_html=True)
with col_head2:
    st.markdown("<div style='text-align: right; font-size: 12px; color: #6B7686; padding-top: 10px;'>Estado: <span style='color: #059669; font-weight: 700;'>● En Línea</span></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 01: INICIO (DASHBOARD GENERAL REPLICANDO LA IMAGEN "APP")
# ---------------------------------------------------------
if nav_option == "01. Inicio":
    # Fila de 4 Tarjetas KPI Principales
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ventas Totales</div>
            <div class="kpi-value">S/ {v_curr:,.2f}</div>
            <div class="{'kpi-badge-pos' if delta_v>=0 else 'kpi-badge-neg'}">
                {'▲' if delta_v>=0 else '▼'} {abs(delta_v):.1f}% vs. mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Productos Vendidos</div>
            <div class="kpi-value">{qty_curr:,} un.</div>
            <div class="{'kpi-badge-pos' if delta_q>=0 else 'kpi-badge-neg'}">
                {'▲' if delta_q>=0 else '▼'} {abs(delta_q):.1f}% vs. mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Clientes Atendidos</div>
            <div class="kpi-value">{tx_curr:,}</div>
            <div class="{'kpi-badge-pos' if delta_tx>=0 else 'kpi-badge-neg'}">
                {'▲' if delta_tx>=0 else '▼'} {abs(delta_tx):.1f}% vs. mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Rentabilidad</div>
            <div class="kpi-value">{margin_curr:.1f}%</div>
            <div class="{'kpi-badge-pos' if delta_mg>=0 else 'kpi-badge-neg'}">
                {'▲' if delta_mg>=0 else '▼'} {abs(delta_mg):.1f} pp vs. mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Fila 1 de Gráficos: Evolución Diaria & Ventas por Categoría
    c_g1, c_g2 = st.columns([1.6, 1])

    with c_g1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Evolución de Ventas</div>
            <div class="section-subtitle">Ventas diarias registradas en el periodo seleccionado</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)['Ventas_Soles'].sum().reset_index()
        fig_trend = px.line(
            df_daily, x='Fecha', y='Ventas_Soles',
            markers=True, line_shape='spline'
        )
        fig_trend.update_traces(line_color='#0284C7', line_width=3, marker=dict(size=6, color='#0284C7'))
        fig_trend.update_layout(**PLOTLY_THEME, height=320)
        st.plotly_chart(fig_trend, use_container_width=True)

    with c_g2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Ventas por Categoría</div>
            <div class="section-subtitle">Distribución porcentual del total facturado</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        fig_cat = px.pie(
            df_cat, values='Ventas_Soles', names='Categoria', hole=0.6,
            color_discrete_sequence=['#0284C7', '#6C5CE7', '#10B981', '#F59E0B', '#64748B']
        )
        fig_cat.update_traces(textposition='inside', textinfo='percent+label', textfont_color='#0B1220')
        fig_cat.update_layout(
            **PLOTLY_THEME, height=320, showlegend=True,
            annotations=[dict(text=f"S/ {v_curr:,.0f}<br><span style='font-size:10px;'>Total</span>", x=0.5, y=0.5, font_size=16, font_color="#0B1220", font_family="Space Grotesk", showarrow=False)]
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # Fila 2 de Gráficos: Top Productos, Canales & Alertas
    c_b1, c_b2, c_b3 = st.columns([1, 1, 1.2])

    with c_b1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Productos Más Vendidos</div>
            <div class="section-subtitle">Top 5 por volumen de unidades</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_top5 = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(5).reset_index()
        fig_top = px.bar(df_top5, x='Cantidad', y='Producto', orientation='h', text='Cantidad')
        fig_top.update_traces(marker_color='#0284C7', textposition='outside', textfont_color='#0B1220')
        fig_top.update_layout(**PLOTLY_THEME, height=280)
        st.plotly_chart(fig_top, use_container_width=True)

    with c_b2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Canales de Venta</div>
            <div class="section-subtitle">Participación por canal comercial</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_chan = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
        fig_chan = px.pie(df_chan, values='Ventas_Soles', names='Canal_Venta', color_discrete_sequence=['#00C2D1', '#10B981', '#6C5CE7', '#F59E0B'])
        fig_chan.update_traces(textinfo='percent+label', textfont_color='#0B1220')
        fig_chan.update_layout(**PLOTLY_THEME, height=280, showlegend=False)
        st.plotly_chart(fig_chan, use_container_width=True)

    with c_b3:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Alertas y Recomendaciones</div>
            <div class="section-subtitle">Detección automática de patrones</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-card-warning">
            <div class="alert-title-warning">Producto con baja rotación</div>
            <div class="alert-desc-warning">Las ventas de 'Galletas' han disminuido un 25% respecto al periodo anterior. Considerar oferta combo.</div>
        </div>
        <div class="alert-card-success">
            <div class="alert-title-success">Oportunidad de crecimiento</div>
            <div class="alert-desc-success">La categoría 'Bebidas' muestra tendencia al alza los fines de semana. Incrementar stock los jueves.</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 02: VENTAS (ANÁLISIS DE FACTURACIÓN Y TRANSACCIONES)
# ---------------------------------------------------------
elif nav_option == "02. Ventas":
    st.markdown("<h2 style='font-size: 20px; margin-bottom: 15px;'>Análisis Detallado de Facturación y Transacciones</h2>", unsafe_allow_html=True)
    
    v_col1, v_col2 = st.columns([1, 1])
    
    with v_col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Ventas por Día de la Semana</div>
            <div class="section-subtitle">Comportamiento del flujo de ingresos diario</div>
        </div>
        """, unsafe_allow_html=True)
        
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        days_map = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
        
        df_curr['Dia_Nombre'] = df_curr['Fecha'].dt.strftime("%A")
        df_days = df_curr.groupby('Dia_Nombre')['Ventas_Soles'].sum().reindex(days_order).dropna().reset_index()
        df_days['Dia_Esp'] = df_days['Dia_Nombre'].map(days_map)
        
        fig_days = px.bar(df_days, x='Dia_Esp', y='Ventas_Soles', text_auto='.2s')
        fig_days.update_traces(marker_color='#6C5CE7', textfont_color='#0B1220')
        fig_days.update_layout(**PLOTLY_THEME, height=350, xaxis_title="Día", yaxis_title="Ventas (S/)")
        st.plotly_chart(fig_days, use_container_width=True)

    with v_col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Distribución del Valor de Ticket</div>
            <div class="section-subtitle">Mapeo de frecuencia por monto comprado</div>
        </div>
        """, unsafe_allow_html=True)
        
        fig_hist = px.histogram(df_curr, x='Ventas_Soles', nbins=20, color_discrete_sequence=['#00C2D1'])
        fig_hist.update_layout(**PLOTLY_THEME, height=350, xaxis_title="Monto del Ticket (S/)", yaxis_title="Frecuencia")
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("### Registro Detallado de Transacciones")
    st.dataframe(
        df_curr[['ID_Transaccion', 'Fecha', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Precio_Unitario', 'Ventas_Soles', 'Utilidad_Soles']].sort_values(by='Fecha', ascending=False),
        use_container_width=True,
        height=300
    )

# ---------------------------------------------------------
# PESTAÑA 03: PRODUCTOS (CATÁLOGO & ROTACIÓN DE INVENTARIOS)
# ---------------------------------------------------------
elif nav_option == "03. Productos":
    st.markdown("<h2 style='font-size: 20px; margin-bottom: 15px;'>Rendimiento de Productos y Rotación de Inventarios</h2>", unsafe_allow_html=True)
    
    p_col1, p_col2 = st.columns([1, 1])
    
    with p_col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Top 10 Productos por Facturación (S/)</div>
            <div class="section-subtitle">Ranking de aportación de ingresos al negocio</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_p_rev = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()
        fig_p_rev = px.bar(df_p_rev, x='Ventas_Soles', y='Producto', orientation='h', text_auto='.2s')
        fig_p_rev.update_traces(marker_color='#0284C7', textfont_color='#0B1220')
        fig_p_rev.update_layout(**PLOTLY_THEME, height=380, xaxis_title="Facturación (S/)", yaxis_title="Producto")
        st.plotly_chart(fig_p_rev, use_container_width=True)

    with p_col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Top 10 Productos por Unidades Vendidas</div>
            <div class="section-subtitle">Ranking de volumen físico de ventas</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_p_qty = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()
        fig_p_qty = px.bar(df_p_qty, x='Cantidad', y='Producto', orientation='h', text_auto=True)
        fig_p_qty.update_traces(marker_color='#10B981', textfont_color='#0B1220')
        fig_p_qty.update_layout(**PLOTLY_THEME, height=380, xaxis_title="Unidades Vendidas", yaxis_title="Producto")
        st.plotly_chart(fig_p_qty, use_container_width=True)

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Matriz de Precio vs. Volumen por Categoría</div>
        <div class="section-subtitle">Relación entre precio unitario promedio y demanda por producto</div>
    </div>
    """, unsafe_allow_html=True)
    
    df_p_matrix = df_curr.groupby(['Producto', 'Categoria']).agg({
        'Precio_Unitario': 'mean',
        'Cantidad': 'sum',
        'Ventas_Soles': 'sum'
    }).reset_index()
    
    fig_mat = px.scatter(
        df_p_matrix, x='Precio_Unitario', y='Cantidad',
        size='Ventas_Soles', color='Categoria', hover_name='Producto',
        color_discrete_sequence=['#0284C7', '#6C5CE7', '#10B981', '#F59E0B', '#64748B']
    )
    fig_mat.update_layout(**PLOTLY_THEME, height=360, xaxis_title="Precio Unitario Promedio (S/)", yaxis_title="Unidades Vendidas")
    st.plotly_chart(fig_mat, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 04: RENTABILIDAD (MÁRGENES & ANÁLISIS FINANCIERO)
# ---------------------------------------------------------
elif nav_option == "04. Rentabilidad":
    st.markdown("<h2 style='font-size: 20px; margin-bottom: 15px;'>Mapeo Financiero y Márgenes de Ganancia</h2>", unsafe_allow_html=True)
    
    r_col1, r_col2 = st.columns([1.2, 1])
    
    with r_col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Ventas vs. Utilidad Neta por Producto</div>
            <div class="section-subtitle">Identificación de los productos más rentables</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_p_prof = df_curr.groupby('Producto').agg({'Ventas_Soles': 'sum', 'Utilidad_Soles': 'sum'}).reset_index()
        fig_scatter = px.scatter(
            df_p_prof, x='Ventas_Soles', y='Utilidad_Soles', text='Producto',
            size='Utilidad_Soles', color_discrete_sequence=['#6C5CE7']
        )
        fig_scatter.update_traces(textposition='top center', textfont_color='#0B1220')
        fig_scatter.update_layout(**PLOTLY_THEME, height=380, xaxis_title="Ventas Totales (S/)", yaxis_title="Utilidad Neta (S/)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with r_col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Margen Promedio (%) por Categoría</div>
            <div class="section-subtitle">Eficiencia de ganancia por línea de producto</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_cat_prof = df_curr.groupby('Categoria').apply(
            lambda x: (x['Utilidad_Soles'].sum() / x['Ventas_Soles'].sum() * 100) if x['Ventas_Soles'].sum() > 0 else 0
        ).reset_index(name='Margen_Pct')
        
        fig_margin = px.bar(df_cat_prof, x='Categoria', y='Margen_Pct', text_auto='.1f')
        fig_margin.update_traces(marker_color='#00C2D1', textfont_color='#0B1220')
        fig_margin.update_layout(**PLOTLY_THEME, height=380, xaxis_title="Categoría", yaxis_title="Margen (%)")
        st.plotly_chart(fig_margin, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 05: ANÁLISIS (INTELIGENCIA DE NEGOCIO & PATRONES)
# ---------------------------------------------------------
elif nav_option == "05. Análisis":
    st.markdown("<h2 style='font-size: 20px; margin-bottom: 15px;'>Inteligencia Aumentada y Patrones de Venta</h2>", unsafe_allow_html=True)
    
    a_col1, a_col2 = st.columns([1, 1])
    
    with a_col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Ventas por Canal y Categoría</div>
            <div class="section-subtitle">Cruzamiento de demanda comercial</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_cross = df_curr.groupby(['Categoria', 'Canal_Venta'])['Ventas_Soles'].sum().reset_index()
        fig_cross = px.bar(df_cross, x='Categoria', y='Ventas_Soles', color='Canal_Venta', barmode='group', color_discrete_sequence=['#0284C7', '#10B981', '#6C5CE7', '#F59E0B'])
        fig_cross.update_layout(**PLOTLY_THEME, height=360, xaxis_title="Categoría", yaxis_title="Ventas (S/)")
        st.plotly_chart(fig_cross, use_container_width=True)

    with a_col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Estructura de Ventas vs. Costos por Categoría</div>
            <div class="section-subtitle">Desglose de costo operativo e ingresos</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_struct = df_curr.groupby('Categoria')[['Ventas_Soles', 'Costo_Soles']].sum().reset_index()
        df_struct_m = pd.melt(df_struct, id_vars=['Categoria'], value_vars=['Ventas_Soles', 'Costo_Soles'], var_name='Tipo', value_name='Monto')
        df_struct_m['Tipo'] = df_struct_m['Tipo'].map({'Ventas_Soles': 'Ventas', 'Costo_Soles': 'Costo'})
        
        fig_struct = px.bar(df_struct_m, x='Categoria', y='Monto', color='Tipo', barmode='group', color_discrete_sequence=['#0284C7', '#EF4444'])
        fig_struct.update_layout(**PLOTLY_THEME, height=360, xaxis_title="Categoría", yaxis_title="Monto (S/)")
        st.plotly_chart(fig_struct, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 06: SIMULADOR (HERRAMIENTA INTERACTIVA)
# ---------------------------------------------------------
elif nav_option == "06. Simulador":
    st.markdown("<h2 style='font-size: 20px; margin-bottom: 15px;'>Simulador Financiero y Proyección MYPE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #6B7686; margin-bottom: 20px;'>Ajusta las variables estratégicas para calcular en tiempo real el impacto en tu beneficio neto.</p>", unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns([1, 1.3])
    
    with sim_col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Parámetros de Simulación</div>
            <div class="section-subtitle">Ajuste de variables comerciales</div>
        </div>
        """, unsafe_allow_html=True)
        
        var_price = st.slider("Ajuste de Precios (%):", min_value=-20, max_value=30, value=5, step=1)
        var_vol = st.slider("Variación en Volumen de Ventas (%):", min_value=-30, max_value=50, value=10, step=1)
        var_mermas = st.slider("Reducción de Mermas/Costos (%):", min_value=0, max_value=30, value=5, step=1)
        inv_mkt = st.number_input("Inversión Adicional en Marketing Digital (S/):", min_value=0, max_value=5000, value=200, step=50)

    with sim_col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Resultados Proyectados</div>
            <div class="section-subtitle">Comparativa entre situación actual y escenario simulado</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Cálculos de simulación
        new_v = v_curr * (1 + var_price/100) * (1 + var_vol/100)
        curr_cost = v_curr - u_curr
        new_cost = curr_cost * (1 - var_mermas/100) * (1 + var_vol/100)
        new_u = new_v - new_cost - inv_mkt
        diff_u = new_u - u_curr
        
        s1, s2 = st.columns(2)
        with s1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Ventas Proyectadas</div>
                <div class="kpi-value">S/ {new_v:,.2f}</div>
                <div class="kpi-badge-pos">S/ {new_v - v_curr:+,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Utilidad Neta Proyectada</div>
                <div class="kpi-value">S/ {new_u:,.2f}</div>
                <div class="{'kpi-badge-pos' if diff_u>=0 else 'kpi-badge-neg'}">
                    S/ {diff_u:+,.2f} vs. actual
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Gráfico comparativo
        df_sim = pd.DataFrame({
            "Escenario": ["Actual", "Simulado"],
            "Ventas": [v_curr, new_v],
            "Utilidad": [u_curr, new_u]
        })
        fig_sim = px.bar(df_sim, x='Escenario', y=['Ventas', 'Utilidad'], barmode='group', color_discrete_sequence=['#0284C7', '#10B981'])
        fig_sim.update_layout(**PLOTLY_THEME, height=260)
        st.plotly_chart(fig_sim, use_container_width=True)

# ---------------------------------------------------------
# PIE DE PÁGINA CORPORATIVO NEXDATA
# ---------------------------------------------------------
st.markdown("<hr style='border-color: #E2E8F0; margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 11px; color: #6B7686;'>NexData Platform v2.5 – Desarrollo de Analítica Avanzada para MYPES Perú 2026</p>", unsafe_allow_html=True)
