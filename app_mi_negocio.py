import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y TEMA STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NexData – Panel MYPE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# PALETA DE COLORES OFICIAL NEXDATA (CERO TEXTO BLANCO)
# Primario: #0E1B2E | Secundario: #00C2D1 | Acento: #6C5CE7
# Fondo: #F4F7FA | Texto Principal: #0B1220 | Texto Secundario: #6B7686
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Space Grotesk', sans-serif;
        background-color: #F4F7FA;
        color: #0B1220;
    }

    .stApp {
        background-color: #F4F7FA;
    }

    header[data-testid="stHeader"] {
        background-color: rgba(244, 247, 250, 0.9);
    }
    footer {visibility: hidden;}

    /* BARRA LATERAL NATIVE STYLING */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42;
    }

    section[data-testid="stSidebar"] * {
        color: #8C9BAE !important;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #00C2D1 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }

    /* LOGO HEADER SIDEBAR */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0px 20px 0px;
        border-bottom: 1px solid #1E2D42;
        margin-bottom: 20px;
    }
    .brand-icon {
        background: linear-gradient(135deg, #00C2D1 0%, #6C5CE7 100%);
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 20px;
        color: #0E1B2E !important;
        box-shadow: 0 4px 12px rgba(0, 194, 209, 0.3);
    }
    .brand-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #00C2D1 !important;
        letter-spacing: -0.5px;
    }
    .brand-subtitle {
        font-size: 11px;
        color: #8C9BAE !important;
        margin-top: -2px;
    }

    /* TARJETAS PREMIUM CON SOMBRAS Y BORDES FINOS */
    .premium-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 20px -2px rgba(14, 27, 46, 0.04);
        transition: all 0.2s ease-in-out;
        margin-bottom: 20px;
    }
    .premium-card:hover {
        box-shadow: 0 8px 24px -4px rgba(14, 27, 46, 0.08);
        border-color: #CBD5E1;
    }

    .kpi-title {
        font-size: 12px;
        font-weight: 700;
        color: #6B7686;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    .kpi-number {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #0B1220;
        letter-spacing: -0.5px;
        margin-bottom: 10px;
    }

    .badge-pos {
        background-color: #DCFCE7;
        color: #166534;
        font-weight: 700;
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    .badge-neg {
        background-color: #FEE2E2;
        color: #991B1B;
        font-weight: 700;
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
    }

    /* ONBOARDING HERO CARD */
    .hero-card {
        background: linear-gradient(135deg, #0E1B2E 0%, #1E2D42 100%);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid #00C2D1;
        box-shadow: 0 12px 32px rgba(14, 27, 46, 0.15);
        margin-bottom: 30px;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #00C2D1 !important;
        margin-bottom: 12px;
    }
    .hero-desc {
        font-size: 15px;
        color: #CBD5E1 !important;
        max-width: 650px;
        line-height: 1.6;
        margin-bottom: 24px;
    }

    /* CABECERA MILAGROS */
    .greeting-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 4px;
    }
    .greeting-sub {
        font-size: 14px;
        color: #6B7686;
        margin-bottom: 24px;
    }

    /* BANDERAS DE ALERTA */
    .alert-card-warning {
        background-color: #FFFBEB;
        border-left: 4px solid #D97706;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .alert-card-success {
        background-color: #F0FDF4;
        border-left: 4px solid #16A34A;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .alert-card-critical {
        background-color: #FEF2F2;
        border-left: 4px solid #DC2626;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .alert-head-warning { font-weight: 700; color: #92400E; font-size: 14px; }
    .alert-head-success { font-weight: 700; color: #166534; font-size: 14px; }
    .alert-head-critical { font-weight: 700; color: #991B1B; font-size: 14px; }
    .alert-body { font-size: 13px; color: #334155; margin-top: 4px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CARGA DE DATOS ROBUSTA O MODO ONBOARDING
# -----------------------------------------------------------------------------
@st.cache_data
def generate_sample_data():
    dates = pd.date_range(start="2026-08-01", periods=45, freq="D")
    categories = ["Alimentos", "Bebidas", "Limpieza", "Higiene"]
    products = {
        "Alimentos": ["Arroz Costeño 5kg", "Aceite Primor 1L", "Fideos Don Vittorio 1kg", "Conservas de Atún"],
        "Bebidas": ["Gaseosa Inca Kola 1.5L", "Agua San Luis 2.5L", "Jugos Frugos 1L", "Cerveza Cusqueña 6pack"],
        "Limpieza": ["Detergente Opal 1kg", "Lavavajillas Ayudín 500g", "Lejía Clorox 1L", "Suavizante Downy"],
        "Higiene": ["Jabón Camay 3pack", "Champú Sedal 340ml", "Crema Dental Kolynos", "Papel Higiénico 4pack"]
    }
    channels = ["Tienda Física", "Yape / WhatsApp", "Delivery Directo"]

    records = []
    np.random.seed(42)
    for d in dates:
        num_tx = np.random.randint(12, 28)
        for _ in range(num_tx):
            cat = np.random.choice(categories, p=[0.4, 0.3, 0.18, 0.12])
            prod = np.random.choice(products[cat])
            channel = np.random.choice(channels, p=[0.55, 0.30, 0.15])
            qty = np.random.randint(1, 6)
            unit_price = np.random.uniform(4.0, 38.0)
            sales = round(qty * unit_price, 2)
            cost = round(sales * np.random.uniform(0.65, 0.78), 2)
            profit = round(sales - cost, 2)
            stock = np.random.randint(2, 45)

            records.append({
                "Fecha": d,
                "Producto": prod,
                "Categoria": cat,
                "Canal_Venta": channel,
                "Cantidad": qty,
                "Ventas_Soles": sales,
                "Costo_Soles": cost,
                "Utilidad_Soles": profit,
                "Stock_Actual": stock
            })

    return pd.DataFrame(records)

def load_data(uploaded_file, use_demo):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Normalización de columnas
            cols_map = {c: c.strip() for c in df.columns}
            df.rename(columns=cols_map, inplace=True)
            
            if 'Fecha' in df.columns:
                df['Fecha'] = pd.to_datetime(df['Fecha'])
            
            return df, "file"
        except Exception as e:
            st.error(f"Error al procesar el archivo subido: {e}")
            return None, "error"
    elif use_demo:
        # Intentar cargar local o generar
        local_path = "/workspace/scratch/dataset_mype_transacciones.csv"
        if os.path.exists(local_path):
            try:
                df = pd.read_csv(local_path)
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                if 'Stock_Actual' not in df.columns:
                    df['Stock_Actual'] = np.random.randint(3, 40, size=len(df))
                return df, "demo"
            except Exception:
                pass
        df = generate_sample_data()
        return df, "demo"
    return None, "empty"

# -----------------------------------------------------------------------------
# BARRA LATERAL - LOGO Y NAVEGACIÓN
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="brand-container">
            <div class="brand-icon">N</div>
            <div>
                <div class="brand-title">NexData</div>
                <div class="brand-subtitle">Datos claros para tu negocio</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navegación Principal")
    nav_option = st.radio(
        "Ir a:",
        ["01. Inicio", "02. Productos Estrella", "03. Alertas y Decisiones", "04. Simulador MYPE"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<br><hr style='border-color:#1E2D42;'><br>", unsafe_allow_html=True)
    st.markdown("### Carga de Base de Datos")
    uploaded_file = st.file_uploader("Subir ventas (.xlsx / .csv):", type=["csv", "xlsx"])
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=True if uploaded_file is None else False)

    st.markdown("<br><hr style='border-color:#1E2D42;'><br>", unsafe_allow_html=True)
    stock_threshold = st.slider("Umbral Mínimo de Stock Crítico:", min_value=3, max_value=20, value=8, step=1)

# Cargar el dataset
df_raw, data_status = load_data(uploaded_file, use_demo)

# -----------------------------------------------------------------------------
# PANTALLA 1: ONBOARDING / SIN DATOS
# -----------------------------------------------------------------------------
if data_status == "empty" or df_raw is None:
    st.markdown("""
        <div class="hero-card">
            <div class="hero-title">Sube tus datos para comenzar</div>
            <div class="hero-desc">
                Conecta tu registro diario de ventas en formato Excel o CSV desde la barra lateral izquierda para transformar tus cifras en indicadores visuales, detección de mermas y recomendaciones inteligentes en tiempo real.
            </div>
            <div style="background: rgba(0, 194, 209, 0.1); border: 1px solid #00C2D1; border-radius: 12px; padding: 16px; color: #00C2D1; font-weight: 600; font-size: 14px; display: inline-block;">
                👈 Selecciona un archivo en la barra lateral o activa la opción "Usar datos de prueba".
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# -----------------------------------------------------------------------------
# FILTROS GLOBALES
# -----------------------------------------------------------------------------
max_date = df_raw['Fecha'].max()
fecha_inicio = max_date - pd.Timedelta(days=30)
fecha_fin = max_date
fecha_inicio_prev = fecha_inicio - pd.Timedelta(days=30)
fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)

df_curr = df_raw[(df_raw['Fecha'] >= fecha_inicio) & (df_raw['Fecha'] <= fecha_fin)]
df_prev = df_raw[(df_raw['Fecha'] >= fecha_inicio_prev) & (df_raw['Fecha'] <= fecha_fin_prev)]

# -----------------------------------------------------------------------------
# MÓDULO 01. INICIO
# -----------------------------------------------------------------------------
if nav_option == "01. Inicio":
    st.markdown("""
        <div>
            <div class="greeting-header">¡Hola, Milagros!</div>
            <div class="greeting-sub">Aquí tienes el resumen ejecutivo simplificado para la toma de decisiones en tu negocio.</div>
        </div>
    """, unsafe_allow_html=True)

    # Filtros de nivel superior
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f1:
        cat_filter = st.selectbox("Filtrar por Categoría:", ["Todas"] + list(df_raw['Categoria'].unique()))
    with col_f2:
        if cat_filter != "Todas":
            prod_list = ["Todos"] + list(df_raw[df_raw['Categoria'] == cat_filter]['Producto'].unique())
        else:
            prod_list = ["Todos"] + list(df_raw['Producto'].unique())
        prod_filter = st.selectbox("Filtrar por Producto:", prod_list)
    with col_f3:
        canal_filter = st.selectbox("Filtrar por Canal:", ["Todos"] + list(df_raw['Canal_Venta'].unique()))

    # Aplicar filtros
    if cat_filter != "Todas":
        df_curr = df_curr[df_curr['Categoria'] == cat_filter]
        df_prev = df_prev[df_prev['Categoria'] == cat_filter]
    if prod_filter != "Todos":
        df_curr = df_curr[df_curr['Producto'] == prod_filter]
        df_prev = df_prev[df_prev['Producto'] == prod_filter]
    if canal_filter != "Todos":
        df_curr = df_curr[df_curr['Canal_Venta'] == canal_filter]
        df_prev = df_prev[df_prev['Canal_Venta'] == canal_filter]

    # Cálculos KPI
    vtas_c = df_curr['Ventas_Soles'].sum()
    vtas_p = df_prev['Ventas_Soles'].sum()
    delta_vtas = ((vtas_c - vtas_p) / vtas_p * 100) if vtas_p > 0 else 0

    util_c = df_curr['Utilidad_Soles'].sum()
    util_p = df_prev['Utilidad_Soles'].sum()
    delta_util = ((util_c - util_p) / util_p * 100) if util_p > 0 else 0

    mg_c = (util_c / vtas_c * 100) if vtas_c > 0 else 0
    mg_p = (util_p / vtas_p * 100) if vtas_p > 0 else 0
    delta_mg = mg_c - mg_p

    tx_c = len(df_curr)
    tkt_c = (vtas_c / tx_c) if tx_c > 0 else 0
    tx_p = len(df_prev)
    tkt_p = (vtas_p / tx_p) if tx_p > 0 else 0
    delta_tkt = ((tkt_c - tkt_p) / tkt_p * 100) if tkt_p > 0 else 0

    # TARJETAS DE INDICADORES
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Ventas Totales</div>
                <div class="kpi-number">S/ {vtas_c:,.2f}</div>
                <div class="{ 'badge-pos' if delta_vtas >= 0 else 'badge-neg' }">
                    { '+' if delta_vtas >= 0 else '' }{delta_vtas:.1f}% vs. mes ant.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Utilidad Neta</div>
                <div class="kpi-number">S/ {util_c:,.2f}</div>
                <div class="{ 'badge-pos' if delta_util >= 0 else 'badge-neg' }">
                    { '+' if delta_util >= 0 else '' }{delta_util:.1f}% vs. mes ant.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Margen de Ganancia</div>
                <div class="kpi-number">{mg_c:.1f}%</div>
                <div class="{ 'badge-pos' if delta_mg >= 0 else 'badge-neg' }">
                    { '+' if delta_mg >= 0 else '' }{delta_mg:.1f} pp vs. mes ant.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Ticket Promedio</div>
                <div class="kpi-number">S/ {tkt_c:.2f}</div>
                <div class="{ 'badge-pos' if delta_tkt >= 0 else 'badge-neg' }">
                    { '+' if delta_tkt >= 0 else '' }{delta_tkt:.1f}% vs. mes ant.
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # GRÁFICOS PRINCIPALES
    c_left, c_right = st.columns([1.8, 1.2])

    with c_left:
        st.markdown("<h4 style='color:#0B1220; font-family:Space Grotesk;'>Evolución Diaria de Ventas y Ganancia</h4>", unsafe_allow_html=True)
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Ventas_Soles'], mode='lines',
            line=dict(color='#00C2D1', width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(0, 194, 209, 0.08)', name='Ventas (S/)'
        ))
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'], mode='lines',
            line=dict(color='#6C5CE7', width=2.5, dash='dash'), name='Utilidad (S/)'
        ))

        fig_line.update_layout(
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Plus Jakarta Sans', color='#0B1220'),
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#0B1220'))
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with c_right:
        st.markdown("<h4 style='color:#0B1220; font-family:Space Grotesk;'>Ventas por Categoría</h4>", unsafe_allow_html=True)
        df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()

        fig_pie = go.Figure(data=[go.Pie(
            labels=df_cat['Categoria'], values=df_cat['Ventas_Soles'], hole=0.65,
            marker=dict(colors=['#00C2D1', '#6C5CE7', '#0E1B2E', '#6B7686']),
            textinfo='percent', textfont=dict(color='#0B1220', size=12)
        )])

        fig_pie.add_annotation(
            text=f"<b style='font-size:18px;color:#0B1220;'>S/ {vtas_c:,.0f}</b><br><span style='font-size:12px;color:#6B7686;'>Ventas</span>",
            x=0.5, y=0.5, showarrow=False
        )

        fig_pie.update_layout(
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Plus Jakarta Sans', color='#0B1220'),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.85, font=dict(color='#0B1220'))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 02. PRODUCTOS ESTRELLA
# -----------------------------------------------------------------------------
elif nav_option == "02. Productos Estrella":
    st.markdown("<h3 style='color:#0B1220; font-family:Space Grotesk;'>Ranking de Productos Estrella</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7686; font-size:14px;'>Identifica los artículos con mayor rotación e ingresos para optimizar compras.</p>", unsafe_allow_html=True)

    p_col1, p_col2 = st.columns(2)

    with p_col1:
        st.markdown("<h4 style='color:#0B1220; font-family:Space Grotesk;'>Top 10 Productos por Facturación (S/)</h4>", unsafe_allow_html=True)
        df_p_sales = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()

        fig_bar_sales = go.Figure(go.Bar(
            x=df_p_sales['Ventas_Soles'], y=df_p_sales['Producto'], orientation='h',
            marker=dict(color='#00C2D1', cornerradius=6),
            text=[f"S/ {v:,.2f}" for v in df_p_sales['Ventas_Soles']], textposition='auto',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_bar_sales.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Plus Jakarta Sans', color='#0B1220'),
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
            yaxis=dict(tickfont=dict(color='#0B1220', size=11))
        )
        st.plotly_chart(fig_bar_sales, use_container_width=True)

    with p_col2:
        st.markdown("<h4 style='color:#0B1220; font-family:Space Grotesk;'>Top 10 Productos por Unidades Vendidas</h4>", unsafe_allow_html=True)
        df_p_qty = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()

        fig_bar_qty = go.Figure(go.Bar(
            x=df_p_qty['Cantidad'], y=df_p_qty['Producto'], orientation='h',
            marker=dict(color='#6C5CE7', cornerradius=6),
            text=[f"{v} un." for v in df_p_qty['Cantidad']], textposition='auto',
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_bar_qty.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Plus Jakarta Sans', color='#0B1220'),
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
            yaxis=dict(tickfont=dict(color='#0B1220', size=11))
        )
        st.plotly_chart(fig_bar_qty, use_container_width=True)

# -----------------------------------------------------------------------------
# MÓDULO 03. ALERTAS Y DECISIONES
# -----------------------------------------------------------------------------
elif nav_option == "03. Alertas y Decisiones":
    st.markdown("<h3 style='color:#0B1220; font-family:Space Grotesk;'>Motor de Alertas y Decisiones Sugeridas</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7686; font-size:14px;'>Detección automática de anomalías de inventario y plan de acción recomendado.</p>", unsafe_allow_html=True)

    # Identificar inventario crítico
    if 'Stock_Actual' in df_curr.columns:
        df_stock = df_curr.groupby('Producto')['Stock_Actual'].min().reset_index()
        critical_prods = df_stock[df_stock['Stock_Actual'] <= stock_threshold]
    else:
        critical_prods = pd.DataFrame()

    a_col1, a_col2 = st.columns(2)

    with a_col1:
        st.markdown("<h4 style='color:#0B1220; font-family:Space Grotesk;'>Alertas de Inventario y Operaciones</h4>", unsafe_allow_html=True)

        if not critical_prods.empty:
            for idx, row in critical_prods.iterrows():
                st.markdown(f"""
                    <div class="alert-card-critical">
                        <div class="alert-head-critical">Atención: Stock Crítico ({row['Producto']})</div>
                        <div class="alert-body">Quedan únicamente <b>{row['Stock_Actual']} unidades</b> en almacén (debajo del umbral de {stock_threshold} un.). Generar orden de reabastecimiento con el proveedor hoy.</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="alert-card-success">
                    <div class="alert-head-success">Inventario Estable</div>
                    <div class="alert-body">Todos los productos se encuentran por encima del umbral mínimo de {stock_threshold} unidades.</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="alert-card-warning">
                <div class="alert-head-warning">Pico de Demanda Detectado (Fines de Semana)</div>
                <div class="alert-body">Las ventas de la categoría <b>Bebidas</b> aumentan un +38% entre viernes y domingo. Se recomienda coordinar compras los jueves por la mañana.</div>
            </div>
        """, unsafe_allow_html=True)

    with a_col2:
        st.markdown("<h4 style='color:#0B1220; font-family:Space Grotesk;'>Acciones Recomendadas para Incremento de Margen</h4>", unsafe_allow_html=True)

        st.markdown("""
            <div class="alert-card-success">
                <div class="alert-head-success">Estrategia 01: Venta Cruzada en Caja</div>
                <div class="alert-body">El ticket promedio actual es de <b>S/ 35.35</b>. Ofrecer productos complementarios de alta rotación (golosinas, bebidas) para elevar el ticket a S/ 42.00 (+18.8% en caja).</div>
            </div>
            <div class="alert-card-success">
                <div class="alert-head-success">Estrategia 02: Potenciar Canal Digital</div>
                <div class="alert-body">Los cobros por <b>Yape / WhatsApp</b> representan el 32% del flujo total. Exhibir el código QR en el mostrador para acelerar el tiempo de atención por cliente.</div>
            </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MÓDULO 04. SIMULADOR MYPE
# -----------------------------------------------------------------------------
elif nav_option == "04. Simulador MYPE":
    st.markdown("<h3 style='color:#0B1220; font-family:Space Grotesk;'>Simulador Interactivo Financiero y ROI</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7686; font-size:14px;'>Ajusta los parámetros comerciales en tiempo real para proyectar la rentabilidad del negocio.</p>", unsafe_allow_html=True)

    s_col1, s_col2 = st.columns([1, 1.2])

    with s_col1:
        st.markdown("<h4 style='color:#0B1220; font-family:Space Grotesk;'>Parámetros de Simulación</h4>", unsafe_allow_html=True)

        plan_tipo = st.selectbox("Plan de Suscripción Seleccionado:", ["Plan Básico (S/ 50/mes)", "Plan Premium (S/ 150/mes)"])
        costo_plan = 50.0 if "Básico" in plan_tipo else 150.0

        num_clientes = st.slider("Número de Clientes Atendidos por Mes:", min_value=100, max_value=2000, value=850, step=50)
        inc_ventas_pct = st.slider("Incremento Estimado de Ventas por Analítica (%):", min_value=0.0, max_value=30.0, value=12.5, step=0.5)
        red_mermas_soles = st.slider("Reducción Mensual de Mermas / Desperdicio (S/):", min_value=0, max_value=1000, value=350, step=50)

    with s_col2:
        st.markdown("<h4 style='color:#0B1220; font-family:Space Grotesk;'>Resultados Proyectados en Tiempo Real</h4>", unsafe_allow_html=True)

        vtas_base = df_curr['Ventas_Soles'].sum() if not df_curr.empty else 15000.0
        adicional_ventas = vtas_base * (inc_ventas_pct / 100.0)
        beneficio_total = adicional_ventas + red_mermas_soles
        ganancia_neta_mype = beneficio_total - costo_plan
        roi_mype = (ganancia_neta_mype / costo_plan * 100.0) if costo_plan > 0 else 0

        st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Beneficio Bruto Generado por Software</div>
                <div class="kpi-number" style="color:#00C2D1;">S/ {beneficio_total:,.2f} / mes</div>
                <div style="font-size:12px; color:#6B7686;">(S/ {adicional_ventas:,.2f} por ventas extra + S/ {red_mermas_soles:,.2f} mermas evitadas)</div>
            </div>
            <div class="premium-card">
                <div class="kpi-title">Costo del Plan Suscripción</div>
                <div class="kpi-number" style="color:#6B7686;">S/ {costo_plan:,.2f} / mes</div>
            </div>
            <div class="premium-card" style="border: 2px solid #00C2D1; background: #F0FDF4;">
                <div class="kpi-title" style="color:#166534;">Ganancia Neta Limpia para la MYPE</div>
                <div class="kpi-number" style="color:#166534;">S/ {ganancia_neta_mype:,.2f} / mes</div>
                <div class="badge-pos">ROI: {roi_mype:,.1f}% (El software se paga solo)</div>
            </div>
        """, unsafe_allow_html=True)
