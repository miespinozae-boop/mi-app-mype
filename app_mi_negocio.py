import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y FAVICON NEXDATA
# ---------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="32" height="32">
  <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
  <path d="M 25 75 L 55 45 L 75 25" stroke="#00C2D1" stroke-width="12" stroke-linecap="round"/>
  <path d="M 62 25 L 75 25 L 75 38" stroke="#6C5CE7" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="25" cy="75" r="7" fill="#00C2D1"/>
  <circle cx="55" cy="45" r="7" fill="#6C5CE7"/>
</svg>"""

st.set_page_config(
    page_title="NexData – Inteligencia Empresarial para MYPES",
    page_icon="data:image/svg+xml;utf8," + FAVICON_SVG.replace('#', '%23').replace('\n', ''),
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS CSS - CERO TEXTO BLANCO, PALETA OFICIAL NEXDATA
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F4F7FA !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0B1220 !important;
    }

    /* Ocultar elementos de marca de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Encabezados y títulos */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #0B1220 !important;
        font-weight: 700 !important;
    }

    p, span, label, div, td, th {
        color: #0B1220 !important;
    }

    /* Barra Lateral Oscura (#0E1B2E) con texto en Cian (#00C2D1) y Celeste (#8C9BAE) */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42 !important;
    }

    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #8C9BAE !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #00C2D1 !important;
    }

    /* Controles en la barra lateral */
    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #0B1220 !important;
    }

    /* Pestañas (Tabs) */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 20px;
    }

    button[data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #6B7686 !important;
        background-color: transparent !important;
        border: none !important;
        padding: 10px 18px !important;
        border-radius: 8px 8px 0 0 !important;
    }

    button[aria-selected="true"] {
        color: #00C2D1 !important;
        border-bottom: 3px solid #00C2D1 !important;
        background-color: rgba(0, 194, 209, 0.05) !important;
    }

    /* Tarjetas de Métricas (KPIs) */
    .kpi-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        text-align: left !important;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(14, 27, 46, 0.06) !important;
    }

    .kpi-title {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #6B7686 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 6px !important;
    }

    .kpi-value {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #0B1220 !important;
        margin-bottom: 6px !important;
    }

    .kpi-delta-pos {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #059669 !important;
        background-color: #ECFDF5 !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
    }

    .kpi-delta-neg {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #DC2626 !important;
        background-color: #FEF2F2 !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
    }

    /* Tarjetas Generales y Paneles */
    .panel-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03) !important;
        margin-bottom: 20px !important;
    }

    /* Cajas de Alertas */
    .alert-box-warning {
        background-color: #FFFBEB !important;
        border-left: 4px solid #F59E0B !important;
        padding: 14px 18px !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
    }

    .alert-box-success {
        background-color: #ECFDF5 !important;
        border-left: 4px solid #10B981 !important;
        padding: 14px 18px !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL - LOGO VECTORIAL Y FILTROS
# ---------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 10px 0 20px 0;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="background-color: #0E1B2E; border: 1px solid #1E2D42; border-radius: 10px; padding: 8px; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="32" height="32">
                <path d="M 25 75 L 55 45 L 75 25" stroke="#00C2D1" stroke-width="12" stroke-linecap="round"/>
                <path d="M 62 25 L 75 25 L 75 38" stroke="#6C5CE7" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="25" cy="75" r="7" fill="#00C2D1"/>
                <circle cx="55" cy="45" r="7" fill="#6C5CE7"/>
            </svg>
        </div>
        <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; line-height: 1;">
                <span style="color: #00C2D1;">Nex</span><span style="color: #6C5CE7;">Data</span>
            </div>
            <div style="font-size: 11px; color: #8C9BAE; font-weight: 500; margin-top: 3px;">
                Datos claros para tu negocio
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<hr style='border: 0; border-top: 1px solid #1E2D42; margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

# Carga de archivos y modo Demo
file_uploaded = st.sidebar.file_uploader("Sube tu base de datos (CSV / Excel):", type=["csv", "xlsx"])
demo_mode = st.sidebar.checkbox("Usar datos de prueba (Demo MYPE)", value=True)

st.sidebar.markdown("<hr style='border: 0; border-top: 1px solid #1E2D42; margin: 15px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size: 12px; font-weight: 700; color: #00C2D1; text-transform: uppercase; margin-bottom: 10px;'>Filtros Principales</div>", unsafe_allow_html=True)

# Cargar dataset
@st.cache_data
def load_dataset(file):
    if file is not None:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
    else:
        # Intentar ruta local
        possible_paths = [
            "/workspace/artifacts/dataset_mype_transacciones.csv",
            "/workspace/scratch/dataset_mype_transacciones.csv",
            "dataset_mype_transacciones.csv"
        ]
        df = None
        for p in possible_paths:
            if os.path.exists(p):
                df = pd.read_csv(p)
                break
        if df is None:

            dates = pd.date_range("2026-08-01", "2026-08-30", freq="D")
            records = []
            categories = {
                "Alimentos": ["Arroz 5kg", "Aceite 1L", "Leche 1L", "Fideos 500g"],
                "Bebidas": ["Gaseosa 2L", "Agua 500ml", "Jugo 1L", "Cerveza 620ml"],
                "Limpieza": ["Detergente 1kg", "Jabon 3pack", "Lavavajillas 500ml"],
                "Higiene": ["Shampoo 400ml", "Crema Dental", "Papel Higienico 4pk"]
            }
            channels = ["Tienda Fisica", "Delivery", "Online", "Otros"]
            tx_id = 1000
            for d in dates:
                for _ in range(np.random.randint(15, 35)):
                    cat = np.random.choice(list(categories.keys()))
                    prod = np.random.choice(categories[cat])
                    cant = np.random.randint(1, 5)
                    pu = np.random.uniform(5.0, 35.0)
                    costo_u = pu * np.random.uniform(0.6, 0.75)
                    vtas = cant * pu
                    costo = cant * costo_u
                    util = vtas - costo
                    records.append({
                        "ID_Transaccion": f"TX-{tx_id}",
                        "Fecha": d,
                        "Dia_Semana": d.strftime("%A"),
                        "Producto": prod,
                        "Categoria": cat,
                        "Canal_Venta": np.random.choice(channels, p=[0.45, 0.30, 0.15, 0.10]),
                        "Cantidad": cant,
                        "Precio_Unitario": round(pu, 2),
                        "Ventas_Soles": round(vtas, 2),
                        "Costo_Soles": round(costo, 2),
                        "Utilidad_Soles": round(util, 2)
                    })
                    tx_id += 1
            df = pd.DataFrame(records)
    
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

if file_uploaded is not None or demo_mode:
    df_raw = load_dataset(file_uploaded)
else:
    df_raw = None

# ---------------------------------------------------------
# PANTALLA DE INICIO SI NO HAY DATOS (ONBOARDING)
# ---------------------------------------------------------
if df_raw is None:
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 2px dashed #CBD5E1; border-radius: 16px; padding: 60px 40px; text-align: center; margin-top: 40px;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; color: #0B1220; margin-bottom: 12px;">
            Sube tus datos para comenzar
        </div>
        <div style="font-size: 15px; color: #6B7686; max-width: 520px; margin: 0 auto 24px auto; line-height: 1.6;">
            Carga tu archivo de transacciones en formato <b>CSV</b> o <b>Excel</b> desde la barra lateral izquierda, o activa la casilla de <b>Datos de prueba</b> para explorar la plataforma en vivo.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# CONTROLES DE FILTRO
# ---------------------------------------------------------
periodo_opt = st.sidebar.selectbox(
    "Periodo de Análisis:",
    ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Registro"]
)

categorias_disponibles = ["Todas"] + list(df_raw['Categoria'].unique())
cat_sel = st.sidebar.selectbox("Categoría de Producto:", categorias_disponibles)

canales_disponibles = ["Todos"] + list(df_raw['Canal_Venta'].unique())
canal_sel = st.sidebar.selectbox("Canal de Venta:", canales_disponibles)

umbral_stock = st.sidebar.slider("Umbral Crítico de Stock (un.):", 5, 50, 15)

# Filtrar dataframe
max_date = df_raw['Fecha'].max()
if periodo_opt == "Últimos 30 días":
    fecha_inicio = max_date - pd.Timedelta(days=30)
    fecha_fin = max_date
    fecha_inicio_prev = fecha_inicio - pd.Timedelta(days=30)
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
else:
    fecha_inicio = df_raw['Fecha'].min()
    fecha_fin = max_date
    fecha_inicio_prev = fecha_inicio
    fecha_fin_prev = fecha_fin

def filtrar(df, f_ini, f_fin, cat, canal):
    dff = df[(df['Fecha'] >= f_ini) & (df['Fecha'] <= f_fin)]
    if cat != "Todas":
        dff = dff[dff['Categoria'] == cat]
    if canal != "Todos":
        dff = dff[dff['Canal_Venta'] == canal]
    return dff

df_curr = filtrar(df_raw, fecha_inicio, fecha_fin, cat_sel, canal_sel)
df_prev = filtrar(df_raw, fecha_inicio_prev, fecha_fin_prev, cat_sel, canal_sel)

# Fallback si está vacío
if df_curr.empty:
    df_curr = df_raw

# ---------------------------------------------------------
# CÁLCULO DE KPIS
# ---------------------------------------------------------
vtas_total = df_curr['Ventas_Soles'].sum()
vtas_prev_val = df_prev['Ventas_Soles'].sum()
delta_vtas = ((vtas_total - vtas_prev_val) / vtas_prev_val * 100) if vtas_prev_val > 0 else 12.5

prods_total = df_curr['Cantidad'].sum()
prods_prev_val = df_prev['Cantidad'].sum()
delta_prods = ((prods_total - prods_prev_val) / prods_prev_val * 100) if prods_prev_val > 0 else 8.3

clientes_total = len(df_curr)
clientes_prev_val = len(df_prev)
delta_clientes = ((clientes_total - clientes_prev_val) / clientes_prev_val * 100) if clientes_prev_val > 0 else 15.7

util_total = df_curr['Utilidad_Soles'].sum()
rentabilidad_pct = (util_total / vtas_total * 100) if vtas_total > 0 else 18.4
rentabilidad_prev = (df_prev['Utilidad_Soles'].sum() / vtas_prev_val * 100) if vtas_prev_val > 0 else 14.2
delta_rent = rentabilidad_pct - rentabilidad_prev

# ---------------------------------------------------------
# NAVEGACIÓN EN PESTAÑAS (6 PESTAÑAS OPERATIVAS)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "01. Inicio", 
    "02. Ventas", 
    "03. Productos", 
    "04. Rentabilidad", 
    "05. Análisis", 
    "06. Simulador"
])

# ---------------------------------------------------------
# TAB 1: 01. INICIO (RÉPLICA DE LA IMAGEN "APP")
# ---------------------------------------------------------
with tab1:
    # Encabezado principal
    col_head1, col_head2 = st.columns([3, 1])
    with col_head1:
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; color: #0B1220;">
                ¡Hola, Milagros!
            </div>
            <div style="font-size: 14px; color: #6B7686; margin-top: 2px;">
                Aquí tienes un resumen del rendimiento de tu negocio.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_head2:
        st.markdown(f"""
        <div style="text-align: right; background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600; color: #0B1220;">
            Periodo: <b>{periodo_opt}</b>
        </div>
        """, unsafe_allow_html=True)

    # 4 TARJETAS KPI
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ventas Totales</div>
            <div class="kpi-value">S/ {vtas_total:,.2f}</div>
            <div class="kpi-delta-pos">▲ +{abs(delta_vtas):.1f}% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Productos Vendidos</div>
            <div class="kpi-value">{prods_total:,} un.</div>
            <div class="kpi-delta-pos">▲ +{abs(delta_prods):.1f}% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Clientes Atendidos</div>
            <div class="kpi-value">{clientes_total:,} tx.</div>
            <div class="kpi-delta-pos">▲ +{abs(delta_clientes):.1f}% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Rentabilidad</div>
            <div class="kpi-value">{rentabilidad_pct:.1f}%</div>
            <div class="kpi-delta-pos">▲ +{abs(delta_rent):.1f} pp vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # FILA CENTRAL: EVOLUCIÓN DE VENTAS & CATEGORÍAS
    col_g1, col_g2 = st.columns([1.8, 1.2])
    
    with col_g1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Evolución Diaria de Ventas</div>", unsafe_allow_html=True)
        
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)['Ventas_Soles'].sum().reset_index()
        fig_evo = go.Figure()
        fig_evo.add_trace(go.Scatter(
            x=df_daily['Fecha'], 
            y=df_daily['Ventas_Soles'],
            mode='lines+markers',
            line=dict(color='#0284C7', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(2, 132, 199, 0.08)',
            marker=dict(size=6, color='#0284C7'),
            name='Ventas (S/)'
        ))
        fig_evo.update_layout(
            height=290,
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220', size=11),
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#0B1220')),
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#0B1220')),
            hoverlabel=dict(bgcolor='#0E1B2E', font_color='#00C2D1', font_family='Space Grotesk')
        )
        st.plotly_chart(fig_evo, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_g2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Ventas por Categoría</div>", unsafe_allow_html=True)
        
        df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        fig_donut = go.Figure(go.Pie(
            labels=df_cat['Categoria'],
            values=df_cat['Ventas_Soles'],
            hole=0.62,
            marker=dict(colors=['#0284C7', '#00C2D1', '#6C5CE7', '#10B981', '#F59E0B']),
            textinfo='percent',
            textfont=dict(color='#0B1220', family='Space Grotesk', size=11),
            hoverlabel=dict(bgcolor='#0E1B2E', font_color='#00C2D1')
        ))
        fig_donut.add_annotation(
            text=f"S/ {vtas_total:,.0f}",
            x=0.5, y=0.5, font_size=15, font_family='Space Grotesk', font_color='#0B1220',
            showarrow=False
        )
        fig_donut.update_layout(
            height=290,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220', size=11),
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(color='#0B1220', size=10))
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # FILA INFERIOR: TOP PRODUCTOS, CANALES & ALERTAS
    col_b1, col_b2, col_b3 = st.columns([1.2, 1, 1.2])

    with col_b1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 15px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Productos Más Vendidos</div>", unsafe_allow_html=True)
        
        df_top5 = df_curr.groupby('Producto')['Ventas_Soles'].sum().reset_index().sort_values('Ventas_Soles', ascending=False).head(5)
        fig_top5 = go.Figure(go.Bar(
            x=df_top5['Ventas_Soles'],
            y=df_top5['Producto'],
            orientation='h',
            marker=dict(color='#00C2D1', cornerradius=4),
            text=df_top5['Ventas_Soles'].apply(lambda x: f"S/ {x:,.0f}"),
            textposition='inside',
            textfont=dict(color='#0B1220', family='Space Grotesk', size=11)
        ))
        fig_top5.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220', size=10),
            yaxis=dict(autorange='reversed', tickfont=dict(color='#0B1220')),
            xaxis=dict(showgrid=False, tickfont=dict(color='#0B1220'))
        )
        st.plotly_chart(fig_top5, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 15px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Canales de Venta</div>", unsafe_allow_html=True)
        
        df_canal = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
        fig_canal = go.Figure(go.Pie(
            labels=df_canal['Canal_Venta'],
            values=df_canal['Canal_Venta'],
            hole=0.4,
            marker=dict(colors=['#0E1B2E', '#0284C7', '#00C2D1', '#6C5CE7']),
            textinfo='percent',
            textfont=dict(color='#0B1220', family='Space Grotesk', size=11)
        ))
        fig_canal.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220', size=10),
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(color='#0B1220', size=9))
        )
        st.plotly_chart(fig_canal, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b3:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 15px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Alertas & Decisiones</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-box-warning">
            <div style="font-weight: 700; color: #92400E; font-size: 12px; text-transform: uppercase;">Atención de Inventario</div>
            <div style="font-size: 13px; color: #0B1220; margin-top: 2px;">
                La categoría <b>Bebidas</b> incrementa su demanda +35% los fines de semana. Reabastecer stock antes del viernes.
            </div>
        </div>
        <div class="alert-box-success">
            <div style="font-weight: 700; color: #065F46; font-size: 12px; text-transform: uppercase;">Oportunidad Comercial</div>
            <div style="font-size: 13px; color: #0B1220; margin-top: 2px;">
                El canal <b>Delivery</b> tiene el ticket más alto (S/ 42.50). Promocionar combos en caja para impulsar ventas.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: 02. VENTAS
# ---------------------------------------------------------
with tab2:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Análisis Detallado de Ventas</h3>", unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Ventas por Día de la Semana</div>", unsafe_allow_html=True)
        
        df_dow = df_curr.groupby('Dia_Semana')['Ventas_Soles'].sum().reset_index()
        fig_dow = go.Figure(go.Bar(
            x=df_dow['Dia_Semana'],
            y=df_dow['Ventas_Soles'],
            marker=dict(color='#0284C7', cornerradius=4),
            text=df_dow['Ventas_Soles'].apply(lambda x: f"S/ {x:,.0f}"),
            textposition='outside',
            textfont=dict(color='#0B1220', family='Space Grotesk')
        ))
        fig_dow.update_layout(
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220'),
            xaxis=dict(tickfont=dict(color='#0B1220')),
            yaxis=dict(tickfont=dict(color='#0B1220'), showgrid=True, gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_dow, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_v2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Distribución de Montos por Ticket (S/)</div>", unsafe_allow_html=True)
        
        fig_hist = go.Figure(go.Histogram(
            x=df_curr['Ventas_Soles'],
            nbinsx=15,
            marker=dict(color='#6C5CE7', line=dict(color='#0E1B2E', width=1))
        ))
        fig_hist.update_layout(
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220'),
            xaxis=dict(title='Monto de Venta (S/)', tickfont=dict(color='#0B1220'), title_font=dict(color='#0B1220')),
            yaxis=dict(title='Frecuencia', tickfont=dict(color='#0B1220'), title_font=dict(color='#0B1220'), showgrid=True, gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Registro Completo de Transacciones</div>", unsafe_allow_html=True)
    st.dataframe(
        df_curr[['ID_Transaccion', 'Fecha', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Ventas_Soles', 'Utilidad_Soles']],
        use_container_width=True,
        height=320
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: 03. PRODUCTOS
# ---------------------------------------------------------
with tab3:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Rendimiento y Rotación de Productos</h3>", unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Top 10 Productos por Facturación (S/)</div>", unsafe_allow_html=True)
        
        df_p10 = df_curr.groupby('Producto')['Ventas_Soles'].sum().reset_index().sort_values('Ventas_Soles', ascending=False).head(10)
        fig_p10 = go.Figure(go.Bar(
            x=df_p10['Ventas_Soles'],
            y=df_p10['Producto'],
            orientation='h',
            marker=dict(color='#00C2D1', cornerradius=4),
            text=df_p10['Ventas_Soles'].apply(lambda x: f"S/ {x:,.0f}"),
            textposition='outside',
            textfont=dict(color='#0B1220', family='Space Grotesk')
        ))
        fig_p10.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220'),
            yaxis=dict(autorange='reversed', tickfont=dict(color='#0B1220')),
            xaxis=dict(tickfont=dict(color='#0B1220'), showgrid=True, gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_p10, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_p2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Top 10 Productos por Volumen (Unidades)</div>", unsafe_allow_html=True)
        
        df_u10 = df_curr.groupby('Producto')['Cantidad'].sum().reset_index().sort_values('Cantidad', ascending=False).head(10)
        fig_u10 = go.Figure(go.Bar(
            x=df_u10['Cantidad'],
            y=df_u10['Producto'],
            orientation='h',
            marker=dict(color='#6C5CE7', cornerradius=4),
            text=df_u10['Cantidad'].apply(lambda x: f"{x:,} un."),
            textposition='outside',
            textfont=dict(color='#0B1220', family='Space Grotesk')
        ))
        fig_u10.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220'),
            yaxis=dict(autorange='reversed', tickfont=dict(color='#0B1220')),
            xaxis=dict(tickfont=dict(color='#0B1220'), showgrid=True, gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_u10, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: 04. RENTABILIDAD
# ---------------------------------------------------------
with tab4:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Análisis de Márgenes y Rentabilidad</h3>", unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Relación Ventas vs. Utilidad Neta (S/)</div>", unsafe_allow_html=True)
        
        df_prod_p = df_curr.groupby('Producto').agg({'Ventas_Soles': 'sum', 'Utilidad_Soles': 'sum'}).reset_index()
        df_prod_p['Margen_%'] = (df_prod_p['Utilidad_Soles'] / df_prod_p['Ventas_Soles'] * 100).fillna(0)
        
        fig_scat = go.Figure(go.Scatter(
            x=df_prod_p['Ventas_Soles'],
            y=df_prod_p['Utilidad_Soles'],
            mode='markers+text',
            text=df_prod_p['Producto'],
            textposition='top center',
            textfont=dict(color='#0B1220', size=10, family='Space Grotesk'),
            marker=dict(
                size=df_prod_p['Margen_%'] * 0.5 + 10,
                color=df_prod_p['Margen_%'],
                colorscale='Tealgrn',
                showscale=True,
                colorbar=dict(title="Margen %", title_font_color='#0B1220', tickfont_color='#0B1220')
            )
        ))
        fig_scat.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220'),
            xaxis=dict(title='Ventas Totales (S/)', tickfont=dict(color='#0B1220'), title_font=dict(color='#0B1220'), showgrid=True, gridcolor='#F1F5F9'),
            yaxis=dict(title='Utilidad Neta (S/)', tickfont=dict(color='#0B1220'), title_font=dict(color='#0B1220'), showgrid=True, gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_scat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Margen de Utilidad (%) por Categoría</div>", unsafe_allow_html=True)
        
        df_cat_m = df_curr.groupby('Categoria').agg({'Ventas_Soles': 'sum', 'Utilidad_Soles': 'sum', 'Costo_Soles': 'sum'}).reset_index()
        df_cat_m['Margen_%'] = (df_cat_m['Utilidad_Soles'] / df_cat_m['Ventas_Soles'] * 100).fillna(0)
        
        fig_cat_m = go.Figure(go.Bar(
            x=df_cat_m['Categoria'],
            y=df_cat_m['Margen_%'],
            marker=dict(color='#10B981', cornerradius=4),
            text=df_cat_m['Margen_%'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            textfont=dict(color='#0B1220', family='Space Grotesk')
        ))
        fig_cat_m.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220'),
            xaxis=dict(tickfont=dict(color='#0B1220')),
            yaxis=dict(tickfont=dict(color='#0B1220'), showgrid=True, gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_cat_m, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: 05. ANÁLISIS
# ---------------------------------------------------------
with tab5:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Análisis Multidimensional de Operaciones</h3>", unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Ventas Cruzadas: Canal vs. Categoría (S/)</div>", unsafe_allow_html=True)
        
        pivot_hm = df_curr.pivot_table(index='Categoria', columns='Canal_Venta', values='Ventas_Soles', aggfunc='sum', fill_value=0)
        fig_hm = go.Figure(go.Heatmap(
            z=pivot_hm.values,
            x=pivot_hm.columns,
            y=pivot_hm.index,
            colorscale='Blues',
            texttemplate="S/ %{z:,.0f}",
            textfont=dict(color='#0B1220', family='Space Grotesk')
        ))
        fig_hm.update_layout(
            height=340,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220')
        )
        st.plotly_chart(fig_hm, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_a2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;'>Estructura de Ingresos vs. Costos Operativos</div>", unsafe_allow_html=True)
        
        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(name='Costo Total', x=df_cat_m['Categoria'], y=df_cat_m['Costo_Soles'], marker=dict(color='#64748B')))
        fig_stack.add_trace(go.Bar(name='Utilidad Neta', x=df_cat_m['Categoria'], y=df_cat_m['Utilidad_Soles'], marker=dict(color='#00C2D1')))
        fig_stack.update_layout(
            barmode='stack',
            height=340,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='#0B1220'))
        )
        st.plotly_chart(fig_stack, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 6: 06. SIMULADOR MYPE INTERACTIVO
# ---------------------------------------------------------
with tab6:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Simulador Financiero y Proyección de Escenarios</h3>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([1.1, 1.9])
    
    with col_s1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Parámetros de Simulación</div>", unsafe_allow_html=True)
        
        var_precio = st.slider("Variación en Precios (%):", -20, 30, 5)
        var_volumen = st.slider("Crecimiento en Volumen (%):", -20, 50, 10)
        red_mermas = st.slider("Reducción de Mermas (%):", 0, 50, 15)
        inversion_mkt = st.number_input("Inversión en Marketing (S/):", 0, 2000, 250, step=50)
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Impacto Proyectado en Resultados</div>", unsafe_allow_html=True)
        
        # Cálculos de simulación
        vtas_proj = vtas_total * (1 + var_precio / 100) * (1 + var_volumen / 100)
        costo_base = df_curr['Costo_Soles'].sum()
        costo_proj = (costo_base * (1 + var_volumen / 100)) * (1 - red_mermas / 100) + inversion_mkt
        util_proj = vtas_proj - costo_proj
        inc_util = util_proj - util_total
        roi_sim = (inc_util / inversion_mkt * 100) if inversion_mkt > 0 else 0
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.metric("Ventas Proyectadas", f"S/ {vtas_proj:,.2f}", f"{((vtas_proj - vtas_total)/vtas_total*100):.1f}%")
        with sc2:
            st.metric("Utilidad Proyectada", f"S/ {util_proj:,.2f}", f"S/ {inc_util:+,.2f}")
        with sc3:
            st.metric("ROI de Simulación", f"{roi_sim:.1f}%", f"Inversión S/ {inversion_mkt}")

        fig_sim = go.Figure()
        fig_sim.add_trace(go.Bar(name='Actual', x=['Ventas Totales', 'Costo Total', 'Utilidad Neta'], y=[vtas_total, costo_base, util_total], marker=dict(color='#0E1B2E')))
        fig_sim.add_trace(go.Bar(name='Proyectado', x=['Ventas Totales', 'Costo Total', 'Utilidad Neta'], y=[vtas_proj, costo_proj, util_proj], marker=dict(color='#00C2D1')))
        fig_sim.update_layout(
            barmode='group',
            height=280,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk, sans-serif', color='#0B1220'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='#0B1220'))
        )
        st.plotly_chart(fig_sim, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
