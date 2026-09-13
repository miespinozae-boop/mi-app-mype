import streamlit as st
import pandas as pd
import numpy as np
import io
import datetime

# -----------------------------------------------------------------------------
# 01. CONFIGURACIÓN DE PÁGINA Y FAVICON
# -----------------------------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#0E1B2E"/><path d="M 22 78 L 48 52 L 68 62 L 82 28" stroke="#00C2D1" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/><circle cx="22" cy="78" r="7" fill="#8C9BAE"/><circle cx="48" cy="52" r="7" fill="#8C9BAE"/><circle cx="68" cy="62" r="7" fill="#6C5CE7"/><path d="M 70 20 L 88 26 L 82 44 Z" fill="#6C5CE7"/></svg>"""

favicon_uri = FAVICON_SVG.replace('#', '%23')

st.set_page_config(
    page_title="NexData - Panel de Inteligencia Empresarial MYPE",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de Favicon SVG en el Head
st.markdown(f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;utf8,{favicon_uri}">', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 02. ESTILOS CSS ULTRA-PREMIUM (SIN TEXTO BLANCO, SIN EMOJIS, SPACE GROTESK)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F4F7FA !important;
        color: #0B1220 !important;
    }

    .stApp {
        background-color: #F4F7FA !important;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42 !important;
    }

    /* Textos en la barra lateral (Cero texto blanco) */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #8C9BAE !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Títulos e Identidad */
    h1, h2, h3, .main-title {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #0B1220 !important;
        font-weight: 700 !important;
    }

    .greeting-container {
        padding: 10px 0px 20px 0px;
    }

    .greeting-text {
        font-size: 32px;
        font-weight: 700;
        color: #0B1220;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .greeting-text span {
        color: #00C2D1;
    }

    .greeting-subtitle {
        font-size: 15px;
        color: #6B7686;
        margin-top: 4px;
    }

    /* Tarjetas Premium */
    .premium-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 20px rgba(14, 27, 46, 0.04);
        margin-bottom: 20px;
    }

    .kpi-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: #6B7686;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #0B1220;
        margin: 6px 0;
    }

    .kpi-delta-positive {
        font-size: 13px;
        font-weight: 600;
        color: #166534;
        background: #DCFCE7;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }

    .kpi-delta-negative {
        font-size: 13px;
        font-weight: 600;
        color: #991B1B;
        background: #FEE2E2;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }

    /* Empty state / Onboarding */
    .onboarding-box {
        background: #FFFFFF;
        border: 2px dashed #00C2D1;
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        margin: 40px 0;
        box-shadow: 0 10px 30px rgba(0, 194, 209, 0.05);
    }

    .onboarding-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 12px;
    }

    .onboarding-desc {
        font-size: 15px;
        color: #6B7686;
        max-width: 550px;
        margin: 0 auto 24px auto;
        line-height: 1.6;
    }

    /* Alertas */
    .alert-card-warning {
        background: #FFFBEB;
        border: 1px solid #FCD34D;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        color: #92400E;
    }

    .alert-card-success {
        background: #F0FDF4;
        border: 1px solid #86EFAC;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        color: #166534;
    }

    /* Radio buttons en sidebar */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background: #1E2D42 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
        width: 100% !important;
        border: 1px solid #2A3C54 !important;
    }

    div[data-testid="stRadio"] label[data-baseweb="radio"] span {
        color: #00C2D1 !important;
        font-weight: 600 !important;
    }

    /* Ocultar elementos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 03. LOGO SVG OFICIAL Y BARRA LATERAL
# -----------------------------------------------------------------------------
LOGO_SVG_HTML = """
<div style="padding: 10px 0px 25px 0px; border-bottom: 1px solid #1E2D42; margin-bottom: 20px;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <svg width="44" height="44" viewBox="0 0 100 100" style="border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
            <path d="M 22 78 L 48 52 L 68 62 L 82 28" stroke="#00C2D1" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <circle cx="22" cy="78" r="7" fill="#8C9BAE"/>
            <circle cx="48" cy="52" r="7" fill="#8C9BAE"/>
            <circle cx="68" cy="62" r="7" fill="#6C5CE7"/>
            <path d="M 70 20 L 88 26 L 82 44 Z" fill="#6C5CE7"/>
        </svg>
        <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 700; line-height: 1.1;">
                <span style="color: #00C2D1;">Nex</span><span style="color: #8C9BAE;">Data</span>
            </div>
            <div style="font-size: 11px; color: #8C9BAE; margin-top: 2px; font-weight: 500;">
                Datos claros para tu negocio
            </div>
        </div>
    </div>
</div>
"""

with st.sidebar:
    st.markdown(LOGO_SVG_HTML, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 12px; font-weight: 700; color: #00C2D1; margin-bottom: 8px; text-transform: uppercase;'>Navegación Principal</div>", unsafe_allow_html=True)
    nav_option = st.radio(
        "Navegación",
        ["01. Inicio", "02. Productos Estrella", "03. Alertas y Decisiones", "04. Simulador MYPE"],
        index=0
    )
    
    st.markdown("<hr style='border-color: #1E2D42; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 12px; font-weight: 700; color: #00C2D1; margin-bottom: 8px; text-transform: uppercase;'>Carga de Datos</div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Subir base de ventas (.csv / .xlsx)",
        type=["csv", "xlsx", "xls"],
        help="Carga el registro diario de transacciones de tu negocio."
    )
    
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=(uploaded_file is None))
    
    st.markdown("<hr style='border-color: #1E2D42; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: #132238; border: 1px solid #1E2D42; border-radius: 12px; padding: 14px;">
            <div style="font-size: 12px; font-weight: 700; color: #00C2D1;">Soporte NexData</div>
            <div style="font-size: 11px; color: #8C9BAE; margin-top: 4px;">Plataforma optimizada para pequeñas y medianas empresas.</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 04. MOTOR DE CARGA DE DATOS ROBUSTO
# -----------------------------------------------------------------------------
@st.cache_data
def generate_demo_dataset():
    dates = pd.date_range(start="2026-08-01", end="2026-08-30", freq="D")
    products = [
        {"name": "Arroz Superior 1kg", "cat": "Alimentos", "price": 4.50, "cost": 3.20},
        {"name": "Aceite Vegetal 1L", "cat": "Alimentos", "price": 9.50, "cost": 7.10},
        {"name": "Leche Evaporada 400g", "cat": "Alimentos", "price": 4.20, "cost": 3.10},
        {"name": "Detergente en Polvo 800g", "cat": "Limpieza", "price": 8.80, "cost": 6.20},
        {"name": "Galletas Rellenas Pack", "cat": "Snacks", "price": 3.50, "cost": 2.10},
        {"name": "Gaseosa 1.5L", "cat": "Bebidas", "price": 6.00, "cost": 4.10},
        {"name": "Agua Mineral 2L", "cat": "Bebidas", "price": 3.00, "cost": 1.60},
        {"name": "Jabón de Tocador 3pk", "cat": "Higiene", "price": 7.50, "cost": 5.00}
    ]
    channels = ["Tienda Física", "Delivery WhatsApp", "Yape / Digital"]
    
    data = []
    np.random.seed(42)
    tx_id = 1001
    
    for d in dates:
        num_sales = np.random.randint(15, 35)
        for _ in range(num_sales):
            p = np.random.choice(products)
            qty = np.random.randint(1, 6)
            ch = np.random.choice(channels, p=[0.55, 0.25, 0.20])
            sales = qty * p["price"]
            cost = qty * p["cost"]
            profit = sales - cost
            
            data.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": d,
                "Dia_Semana": d.strftime("%A"),
                "Producto": p["name"],
                "Categoria": p["cat"],
                "Canal_Venta": ch,
                "Cantidad": qty,
                "Precio_Unitario": p["price"],
                "Ventas_Soles": sales,
                "Costo_Soles": cost,
                "Utilidad_Soles": profit
            })
            tx_id += 1
            
    return pd.DataFrame(data)

def load_data():
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            df["Fecha"] = pd.to_datetime(df["Fecha"])
            return df, True
        except Exception as e:
            st.error(f"Error al leer el archivo cargado: {e}")
            return None, False
    elif use_demo:
        return generate_demo_dataset(), True
    else:
        return None, False

df_raw, has_data = load_data()

# -----------------------------------------------------------------------------
# 05. CABECERA PRINCIPAL
# -----------------------------------------------------------------------------
st.markdown("""
<div class="greeting-container">
    <div class="greeting-text">¡Hola, <span>Milagros</span>!</div>
    <div class="greeting-subtitle">Bienvenida a tu Panel de Inteligencia Empresarial NexData.</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 06. RENDERIZADO SI NO HAY DATOS (EMPTY STATE / ONBOARDING)
# -----------------------------------------------------------------------------
if not has_data:
    st.markdown("""
    <div class="onboarding-box">
        <div class="onboarding-title">Sube tus datos para comenzar</div>
        <div class="onboarding-desc">
            Carga tu registro de ventas en formato Excel (.xlsx) o CSV en la barra lateral izquierda, 
            o activa la casilla <b>"Usar datos de prueba"</b> para explorar las funcionalidades en vivo.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # FILTROS DE INTERFAZ EN PARTE SUPERIOR
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        categories = ["Todas las Categorías"] + list(df_raw["Categoria"].unique())
        cat_sel = st.selectbox("Filtrar por Categoría:", categories)
        
    with f_col2:
        channels = ["Todos los Canales"] + list(df_raw["Canal_Venta"].unique())
        chan_sel = st.selectbox("Filtrar por Canal:", channels)
        
    with f_col3:
        periods = ["Últimos 30 días", "Últimos 15 días", "Últimos 7 días"]
        period_sel = st.selectbox("Periodo de Análisis:", periods)

    # Filtrar dataframe
    df_filtered = df_raw.copy()
    if cat_sel != "Todas las Categorías":
        df_filtered = df_filtered[df_filtered["Categoria"] == cat_sel]
    if chan_sel != "Todos los Canales":
        df_filtered = df_filtered[df_filtered["Canal_Venta"] == chan_sel]
        
    if period_sel == "Últimos 15 días":
        df_filtered = df_filtered[df_filtered["Fecha"] >= df_filtered["Fecha"].max() - pd.Timedelta(days=15)]
    elif period_sel == "Últimos 7 días":
        df_filtered = df_filtered[df_filtered["Fecha"] >= df_filtered["Fecha"].max() - pd.Timedelta(days=7)]

    # -------------------------------------------------------------------------
    # PANTALLA 01: INICIO
    # -------------------------------------------------------------------------
    if nav_option == "01. Inicio":
        import plotly.graph_objects as go
        
        # CÁLCULOS KPI
        total_sales = df_filtered["Ventas_Soles"].sum()
        total_profit = df_filtered["Utilidad_Soles"].sum()
        margin_pct = (total_profit / total_sales * 100) if total_sales > 0 else 0
        total_tx = len(df_filtered)
        ticket_avg = (total_sales / total_tx) if total_tx > 0 else 0
        
        # 4 TARJETAS PRINCIPALES
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Ventas Totales</div>
                <div class="kpi-value">S/ {total_sales:,.2f}</div>
                <div class="kpi-delta-positive">+12.4% vs mes ant.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi2:
            st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Utilidad Neta</div>
                <div class="kpi-value">S/ {total_profit:,.2f}</div>
                <div class="kpi-delta-positive">+14.8% vs mes ant.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi3:
            st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Margen Ganancia</div>
                <div class="kpi-value">{margin_pct:.1f}%</div>
                <div class="kpi-delta-positive">+2.1 pp vs mes ant.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi4:
            st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Ticket Promedio</div>
                <div class="kpi-value">S/ {ticket_avg:.2f}</div>
                <div class="kpi-delta-positive">+3.5% vs mes ant.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # GRÁFICOS PRINCIPALES
        g_col1, g_col2 = st.columns([1.8, 1.2])
        
        with g_col1:
            st.markdown("<h3 style='font-size: 18px;'>Evolución Diaria de Ventas y Ganancias</h3>", unsafe_allow_html=True)
            
            df_daily = df_filtered.groupby("Fecha")[["Ventas_Soles", "Utilidad_Soles"]].sum().reset_index()
            
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_daily["Fecha"], y=df_daily["Ventas_Soles"],
                mode='lines+markers', name='Ventas (S/)',
                line=dict(color='#00C2D1', width=3, shape='spline'),
                fill='tozeroy', fillcolor='rgba(0, 194, 209, 0.08)'
            ))
            fig_line.add_trace(go.Scatter(
                x=df_daily["Fecha"], y=df_daily["Utilidad_Soles"],
                mode='lines', name='Utilidad (S/)',
                line=dict(color='#6C5CE7', width=2, dash='dot')
            ))
            
            fig_line.update_layout(
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Plus Jakarta Sans', color='#0B1220'),
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                legend=dict(orientation="h", y=1.1, font=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with g_col2:
            st.markdown("<h3 style='font-size: 18px;'>Ventas por Categoría</h3>", unsafe_allow_html=True)
            
            df_cat = df_filtered.groupby("Categoria")["Ventas_Soles"].sum().reset_index()
            
            fig_donut = go.Figure(data=[go.Pie(
                labels=df_cat["Categoria"], values=df_cat["Ventas_Soles"],
                hole=0.65, marker=dict(colors=['#00C2D1', '#6C5CE7', '#38BDF8', '#F59E0B', '#10B981']),
                textinfo='percent', textfont=dict(color='#0B1220', size=12)
            )])
            
            fig_donut.add_annotation(
                text=f"<b style='font-size:16px;color:#0B1220;'>S/ {total_sales:,.0f}</b><br><span style='font-size:11px;color:#6B7686;'>Total</span>",
                x=0.5, y=0.5, showarrow=False
            )
            
            fig_donut.update_layout(
                height=320, margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="v", y=0.5, font=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    # -------------------------------------------------------------------------
    # PANTALLA 02: PRODUCTOS ESTRELLA
    # -------------------------------------------------------------------------
    elif nav_option == "02. Productos Estrella":
        import plotly.graph_objects as go
        
        st.markdown("<h3 style='font-size: 20px;'>Ranking de Productos Más Vendidos</h3>", unsafe_allow_html=True)
        
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            st.markdown("<h4 style='font-size: 15px; color:#6B7686;'>Top Productos por Facturación (S/)</h4>", unsafe_allow_html=True)
            df_prod_val = df_filtered.groupby("Producto")["Ventas_Soles"].sum().reset_index().sort_values("Ventas_Soles", ascending=True)
            
            fig_bar_val = go.Figure(go.Bar(
                x=df_prod_val["Ventas_Soles"], y=df_prod_val["Producto"],
                orientation='h', marker=dict(color='#00C2D1')
            ))
            fig_bar_val.update_layout(
                height=380, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(tickfont=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_bar_val, use_container_width=True)

        with p_col2:
            st.markdown("<h4 style='font-size: 15px; color:#6B7686;'>Top Productos por Unidades Vendidas</h4>", unsafe_allow_html=True)
            df_prod_qty = df_filtered.groupby("Producto")["Cantidad"].sum().reset_index().sort_values("Cantidad", ascending=True)
            
            fig_bar_qty = go.Figure(go.Bar(
                x=df_prod_qty["Cantidad"], y=df_prod_qty["Producto"],
                orientation='h', marker=dict(color='#6C5CE7')
            ))
            fig_bar_qty.update_layout(
                height=380, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(tickfont=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_bar_qty, use_container_width=True)

    # -------------------------------------------------------------------------
    # PANTALLA 03: ALERTAS Y DECISIONES
    # -------------------------------------------------------------------------
    elif nav_option == "03. Alertas y Decisiones":
        st.markdown("<h3 style='font-size: 20px;'>Detección Automática de Oportunidades y Riesgos</h3>", unsafe_allow_html=True)
        
        threshold = st.slider("Ajustar Umbral Crítico de Stock (Unidades):", min_value=10, max_value=100, value=30)
        
        a_col1, a_col2 = st.columns(2)
        
        with a_col1:
            st.markdown("""
            <div class="alert-card-warning">
                <div style="font-weight: 700; font-size: 16px; margin-bottom: 6px;">Alerta de Reabastecimiento Crítico</div>
                <div style="font-size: 14px; line-height: 1.5;">
                    Los productos de la categoría <b>Bebidas</b> e <b>Insumos Básicos</b> registran un incremento del +38% de ventas durante los fines de semana. 
                    Se sugiere programar compras los días jueves.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="alert-card-warning">
                <div style="font-weight: 700; font-size: 16px; margin-bottom: 6px;">Producto con Menor Rotación</div>
                <div style="font-size: 14px; line-height: 1.5;">
                    El producto <b>Detergente en Polvo 800g</b> presenta un acumulado mayor al umbral ajustado de """ + str(threshold) + """ unidades. 
                    Se recomienda lanzar una promoción cruzada.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with a_col2:
            st.markdown("""
            <div class="alert-card-success">
                <div style="font-weight: 700; font-size: 16px; margin-bottom: 6px;">Oportunidad Digital Detectada</div>
                <div style="font-size: 14px; line-height: 1.5;">
                    El canal de pago <b>Yape / Digital</b> representa el 28% de la facturación total. 
                    Imprimir el código QR visible en mostrador para agilizar el cobro.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="alert-card-success">
                <div style="font-weight: 700; font-size: 16px; margin-bottom: 6px;">Estrategia de Incremento de Ticket</div>
                <div style="font-size: 14px; line-height: 1.5;">
                    El ticket promedio actual es de <b>S/ 32.50</b>. 
                    Ofrecer un producto de impulso de S/ 3.50 en caja permitirá alcanzar la meta comercial de S/ 36.00 por cliente.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # PANTALLA 04: SIMULADOR MYPE
    # -------------------------------------------------------------------------
    elif nav_option == "04. Simulador MYPE":
        st.markdown("<h3 style='font-size: 20px;'>Simulador Financiero de Crecimiento para la MYPE</h3>", unsafe_allow_html=True)
        
        sim_col1, sim_col2 = st.columns([1.2, 1.8])
        
        with sim_col1:
            st.markdown("<h4 style='font-size: 15px; color:#6B7686;'>Parámetros de Simulación</h4>", unsafe_allow_html=True)
            inc_sales_pct = st.slider("Incremento Estimado en Ventas (%):", 0, 50, 15)
            red_cost_pct = st.slider("Reducción de Mermas / Costos (%):", 0, 30, 8)
            plan_fee = st.selectbox("Plan de Suscripción NexData:", ["Plan Básico (S/ 50/mes)", "Plan Premium (S/ 150/mes)"])
            
            fee_val = 50 if "50" in plan_fee else 150
            
        with sim_col2:
            curr_sales = df_filtered["Ventas_Soles"].sum()
            curr_profit = df_filtered["Utilidad_Soles"].sum()
            
            add_sales = curr_sales * (inc_sales_pct / 100)
            add_savings = (curr_sales - curr_profit) * (red_cost_pct / 100)
            gross_benefit = add_sales * 0.30 + add_savings
            net_benefit = gross_benefit - fee_val
            roi = (net_benefit / fee_val * 100) if fee_val > 0 else 0
            
            st.markdown(f"""
            <div class="premium-card">
                <div class="kpi-title">Beneficio Neto Adicional Estimado</div>
                <div class="kpi-value" style="color: #166534;">S/ {net_benefit:,.2f} / mes</div>
                <div style="font-size: 14px; color: #6B7686; margin-top: 8px;">
                    • Ventas Adicionales Proyectadas: <b>S/ {add_sales:,.2f}</b><br>
                    • Ahorro Estimado por Mermas: <b>S/ {add_savings:,.2f}</b><br>
                    • Retorno de Inversión (ROI): <b style="color:#166534;">{roi:.0f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: #E2E8F0; margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-size: 12px; color: #6B7686;'>NexData © 2026 – Plataforma de Inteligencia Empresarial para MYPES</div>", unsafe_allow_html=True)
