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
  <path d="M 25 75 L 50 50 L 75 25" stroke="#00C2D1" stroke-width="8" stroke-linecap="round"/>
  <circle cx="25" cy="75" r="7" fill="#FFFFFF"/>
  <circle cx="50" cy="50" r="7" fill="#FFFFFF"/>
  <circle cx="75" cy="25" r="9" fill="#6C5CE7"/>
  <path d="M 60 25 L 75 25 L 75 40" stroke="#6C5CE7" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>"""

st.set_page_config(
    page_title="NexData – Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar CSS global de alto contraste, tipografía premium y favicon
st.markdown("""
<head>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='22' fill='%230E1B2E'/><path d='M 25 75 L 50 50 L 75 25' stroke='%2300C2D1' stroke-width='8' stroke-linecap='round'/><circle cx='25' cy='75' r='7' fill='%23FFFFFF'/><circle cx='50' cy='50' r='7' fill='%23FFFFFF'/><circle cx='75' cy='25' r='9' fill='%236C5CE7'/><path d='M 60 25 L 75 25 L 75 40' stroke='%236C5CE7' stroke-width='8' stroke-linecap='round' stroke-linejoin='round' fill='none'/></svg>">
</head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F4F7FA !important;
        color: #0B1220 !important;
    }
    
    /* Header principal */
    .user-greeting {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #0B1220 !important;
        margin-bottom: 2px !important;
    }
    .user-subtext {
        font-size: 15px !important;
        color: #6B7686 !important;
        margin-bottom: 20px !important;
    }

    /* Tarjetas de Métricas KPI */
    .kpi-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 20px 18px !important;
        box-shadow: 0 4px 15px rgba(14, 27, 46, 0.03) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        height: 100% !important;
    }
    .kpi-header {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        margin-bottom: 12px !important;
    }
    .kpi-icon-box {
        width: 42px !important;
        height: 42px !important;
        border-radius: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 20px !important;
    }
    .kpi-title {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #6B7686 !important;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #0B1220 !important;
        margin: 4px 0 8px 0 !important;
    }
    .kpi-delta-positive {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #16A34A !important;
    }

    /* Contenedores Generales */
    .content-box {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 22px !important;
        box-shadow: 0 4px 15px rgba(14, 27, 46, 0.03) !important;
        margin-bottom: 20px !important;
    }
    .box-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #0B1220 !important;
        margin-bottom: 4px !important;
    }
    .box-subtitle {
        font-size: 13px !important;
        color: #6B7686 !important;
        margin-bottom: 15px !important;
    }

    /* Lista de Productos Mas Vendidos */
    .top-product-item {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 10px 0 !important;
        border-bottom: 1px solid #F1F5F9 !important;
    }
    .top-product-rank {
        font-weight: 700 !important;
        color: #6B7686 !important;
        width: 24px !important;
    }
    .top-product-name {
        font-weight: 600 !important;
        color: #0B1220 !important;
        width: 110px !important;
    }
    .top-product-bar-bg {
        flex-grow: 1 !important;
        background-color: #F1F5F9 !important;
        height: 10px !important;
        border-radius: 6px !important;
        margin: 0 15px !important;
        overflow: hidden !important;
    }
    .top-product-bar-fill {
        height: 100% !important;
        border-radius: 6px !important;
    }
    .top-product-qty {
        font-weight: 700 !important;
        color: #0B1220 !important;
        font-size: 13px !important;
        min-width: 60px !important;
        text-align: right !important;
    }

    /* Tarjetas de Alerta */
    .alert-card-warning {
        background-color: #FFFBEB !important;
        border-left: 4px solid #F59E0B !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        margin-bottom: 12px !important;
    }
    .alert-card-success {
        background-color: #F0FDF4 !important;
        border-left: 4px solid #16A34A !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        margin-bottom: 12px !important;
    }
    .alert-title {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #0B1220 !important;
        margin-bottom: 4px !important;
    }
    .alert-desc {
        font-size: 12px !important;
        color: #6B7686 !important;
        line-height: 1.4 !important;
    }

    /* Barra Lateral Estilizada */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    .sidebar-logo-container {
        padding: 10px 0 20px 0 !important;
        border-bottom: 1px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
    }
    .sidebar-footer-card {
        background-color: #EFF6FF !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 14px !important;
        padding: 16px !important;
        margin-top: 30px !important;
    }
    .sidebar-footer-title {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #1E40AF !important;
    }
    .sidebar-footer-brand {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        color: #1E3A8A !important;
        margin-top: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CARGA DE DATOS ROBUTA CON DEMO PREDETERMINADA
# ---------------------------------------------------------
@st.cache_data
def get_demo_data():
    dates = pd.date_range(start="2026-04-01", end="2026-04-30")
    data = []
    products = [
        ("Arroz 5kg", "Alimentos", 32.0, 24.0),
        ("Aceite Vegetal 1L", "Alimentos", 12.5, 9.0),
        ("Leche Evaporada 400g", "Alimentos", 4.5, 3.2),
        ("Galletas Soda 6pk", "Alimentos", 3.8, 2.5),
        ("Detergente 1kg", "Limpieza", 14.0, 10.0),
        ("Gaseosa 2.25L", "Bebidas", 8.5, 5.8),
        ("Agua Mineral 2L", "Bebidas", 3.5, 2.1),
        ("Jabón de Tocador", "Higiene", 3.2, 2.0),
        ("Champú 400ml", "Higiene", 16.5, 11.5),
        ("Snack Papa Frita", "Otros", 4.5, 2.8)
    ]
    channels = ["Tienda física", "Delivery", "Online", "Otros"]
    channel_weights = [0.45, 0.30, 0.15, 0.10]
    
    np.random.seed(42)
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(15, 30)
        for _ in range(num_tx):
            tx_id += 1
            prod_info = products[np.random.choice(len(products))]
            p_name, p_cat, p_price, p_cost = prod_info
            qty = np.random.randint(1, 5)
            canal = np.random.choice(channels, p=channel_weights)
            
            sales = qty * p_price
            cost = qty * p_cost
            profit = sales - cost
            
            data.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": d,
                "Producto": p_name,
                "Categoria": p_cat,
                "Canal_Venta": canal,
                "Cantidad": qty,
                "Precio_Unitario": p_price,
                "Ventas_Soles": sales,
                "Costo_Soles": cost,
                "Utilidad_Soles": profit
            })
    return pd.DataFrame(data)

# ---------------------------------------------------------
# BARRA LATERAL (LOGO, FILTROS Y NAVEGACIÓN)
# ---------------------------------------------------------
with st.sidebar:
    # Logo SVG NexData
    st.markdown("""
    <div class="sidebar-logo-container">
        <div style="display: flex; align-items: center; gap: 12px;">
            <svg width="38" height="38" viewBox="0 0 100 100" style="border-radius: 10px; background: #0E1B2E; padding: 4px;">
                <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
                <path d="M 25 75 L 50 50 L 75 25" stroke="#00C2D1" stroke-width="9" stroke-linecap="round"/>
                <circle cx="25" cy="75" r="7" fill="#FFFFFF"/>
                <circle cx="50" cy="50" r="7" fill="#FFFFFF"/>
                <circle cx="75" cy="25" r="9" fill="#6C5CE7"/>
                <path d="M 60 25 L 75 25 L 75 40" stroke="#6C5CE7" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            </svg>
            <div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; color: #0B1220; line-height: 1;">
                    Nex<span style="color: #00C2D1;">Data</span>
                </div>
                <div style="font-size: 11px; color: #6B7686; margin-top: 2px;">Datos claros para tu negocio</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navegación Principal
    st.markdown("<div style='font-size: 12px; font-weight: 700; color: #6B7686; text-transform: uppercase; margin-bottom: 10px;'>Navegación</div>", unsafe_allow_html=True)
    nav_option = st.radio(
        "Ir a:",
        ["Inicio", "Ventas", "Productos", "Rentabilidad", "Análisis", "Simulador"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 12px; font-weight: 700; color: #6B7686; text-transform: uppercase; margin-bottom: 10px;'>Carga de Datos</div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Subir dataset (Excel/CSV):", type=["csv", "xlsx"], help="Sube tu reporte de ventas para analizar")
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=True)

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
            df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
            st.success("Dataset cargado correctamente.")
        except Exception:
            st.warning("Estructura de archivo no válida. Cargando datos Demo MYPE.")
            df_raw = get_demo_data()
    else:
        df_raw = get_demo_data()

    # Footer Card en Barra Lateral
    st.markdown("""
    <div class="sidebar-footer-card">
        <div class="sidebar-footer-title">Tu negocio, en mejores decisiones</div>
        <div class="sidebar-footer-brand">NEXDATA</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PANTALLA PRINCIPAL: "INICIO" (DASHBOARD COMPLETO EXACTO)
# ---------------------------------------------------------
if nav_option == "Inicio":
    # Encabezado Principal y Selector de Periodo Superior
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown('<div class="user-greeting">¡Hola, Milagros!</div>', unsafe_allow_html=True)
        st.markdown('<div class="user-subtext">Aquí tienes un resumen del rendimiento de tu negocio.</div>', unsafe_allow_html=True)
    with head_col2:
        periodo_sel = st.selectbox("Periodo de análisis:", ["Últimos 30 días", "Este Mes", "Mes Anterior"], label_visibility="visible")

    # ---------------------------------------------------------
    # 1. FILA DE 4 TARJETAS KPI
    # ---------------------------------------------------------
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    # Cálculos reales sobre el dataset
    total_sales = df_raw['Ventas_Soles'].sum()
    total_qty = df_raw['Cantidad'].sum()
    total_clients = len(df_raw['ID_Transaccion'].unique())
    total_profit = df_raw['Utilidad_Soles'].sum()
    margin_pct = (total_profit / total_sales * 100) if total_sales > 0 else 0

    with kpi1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #E0F2FE; color: #0284C7;">🛒</div>
                <div class="kpi-title">Ventas Totales</div>
            </div>
            <div class="kpi-value">S/ {total_sales:,.0f}</div>
            <div class="kpi-delta-positive">▲ +12.5% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #F3E8FF; color: #9333EA;">📦</div>
                <div class="kpi-title">Productos Vendidos</div>
            </div>
            <div class="kpi-value">{total_qty:,.0f}</div>
            <div class="kpi-delta-positive">▲ +8.3% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #DCFCE7; color: #16A34A;">👤</div>
                <div class="kpi-title">Clientes Atendidos</div>
            </div>
            <div class="kpi-value">{total_clients:,.0f}</div>
            <div class="kpi-delta-positive">▲ +15.7% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #FFEDD5; color: #EA580C;">💰</div>
                <div class="kpi-title">Rentabilidad</div>
            </div>
            <div class="kpi-value">{margin_pct:.1f}%</div>
            <div class="kpi-delta-positive">▲ +4.2% vs. mes anterior</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. SECCIÓN CENTRAL: EVOLUCIÓN Y VENTAS POR CATEGORÍA
    # ---------------------------------------------------------
    col_chart_left, col_chart_right = st.columns([1.5, 1])

    with col_chart_left:
        st.markdown("""
        <div class="content-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="box-title">Evolución de Ventas</div>
                    <div class="box-subtitle">Ventas diarias en los últimos 30 días</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Gráfico Plotly de Evolución Diaria
        df_daily = df_raw.groupby(df_raw['Fecha'].dt.strftime('%d %b'))['Ventas_Soles'].sum().reset_index()
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'],
            y=df_daily['Ventas_Soles'],
            mode='lines+markers',
            line=dict(color='#0284C7', width=3, shape='spline'),
            marker=dict(size=6, color='#0284C7', line=dict(color='#FFFFFF', width=2)),
            fill='tozeroy',
            fillcolor='rgba(2, 132, 199, 0.08)',
            name='Ventas (S/)'
        ))
        fig_line.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#6B7686', size=11)),
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#6B7686', size=11), tickprefix='S/ '),
            showlegend=False
        )
        st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart_right:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">Ventas por Categoría</div>
            <div class="box-subtitle">Distribución de ventas por categoría</div>
        """, unsafe_allow_html=True)
        
        # Gráfico de Dona Plotly con Leyenda Lateral
        df_cat = df_raw.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        fig_donut = px.pie(
            df_cat,
            values='Ventas_Soles',
            names='Categoria',
            hole=0.65,
            color_discrete_sequence=['#0284C7', '#9333EA', '#16A34A', '#EA580C', '#64748B']
        )
        fig_donut.update_traces(
            textinfo='none',
            hovertemplate='%{label}: S/ %{value:,.2f} (%{percent})'
        )
        fig_donut.add_annotation(
            text=f"<b>S/ {total_sales:,.0f}</b><br><span style='font-size: 11px; color: #6B7686;'>Total ventas</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color='#0B1220')
        )
        fig_donut.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                font=dict(color='#0B1220', size=12)
            )
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. SECCIÓN INFERIOR: TRES PANELES (PRODUCTOS, CANALES, ALERTAS)
    # ---------------------------------------------------------
    b_col1, b_col2, b_col3 = st.columns([1, 1, 1.2])

    with b_col1:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">Productos Más Vendidos</div>
            <div class="box-subtitle">Top 5 por volumen de ventas</div>
            
            <div class="top-product-item">
                <span class="top-product-rank">1.</span>
                <span class="top-product-name">Arroz</span>
                <div class="top-product-bar-bg"><div class="top-product-bar-fill" style="width: 100%; background-color: #0284C7;"></div></div>
                <span class="top-product-qty">320 un.</span>
            </div>
            <div class="top-product-item">
                <span class="top-product-rank">2.</span>
                <span class="top-product-name">Aceite</span>
                <div class="top-product-bar-bg"><div class="top-product-bar-fill" style="width: 85%; background-color: #16A34A;"></div></div>
                <span class="top-product-qty">280 un.</span>
            </div>
            <div class="top-product-item">
                <span class="top-product-rank">3.</span>
                <span class="top-product-name">Leche</span>
                <div class="top-product-bar-bg"><div class="top-product-bar-fill" style="width: 70%; background-color: #9333EA;"></div></div>
                <span class="top-product-qty">220 un.</span>
            </div>
            <div class="top-product-item">
                <span class="top-product-rank">4.</span>
                <span class="top-product-name">Galletas</span>
                <div class="top-product-bar-bg"><div class="top-product-bar-fill" style="width: 55%; background-color: #EA580C;"></div></div>
                <span class="top-product-qty">180 un.</span>
            </div>
            <div class="top-product-item" style="border-bottom: none;">
                <span class="top-product-rank">5.</span>
                <span class="top-product-name">Detergente</span>
                <div class="top-product-bar-bg"><div class="top-product-bar-fill" style="width: 45%; background-color: #00C2D1;"></div></div>
                <span class="top-product-qty">160 un.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with b_col2:
        st.markdown("""
        <div class="content-box">
            <div class="box-title">Canales de Venta</div>
            <div class="box-subtitle">Participación por canal</div>
        """, unsafe_allow_html=True)
        
        df_channel = df_raw.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
        fig_channel = px.pie(
            df_channel,
            values='Ventas_Soles',
            names='Canal_Venta',
            hole=0.4,
            color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B', '#64748B']
        )
        fig_channel.update_traces(
            textposition='inside',
            textinfo='percent',
            insidetextfont=dict(color='#FFFFFF', size=12, weight='bold')
        )
        fig_channel.update_layout(
            height=200,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(orientation="v", x=1.0, y=0.5, font=dict(color='#0B1220', size=11))
        )
        st.plotly_chart(fig_channel, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    with b_col3:
        st.markdown("""
        <div class="content-box">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <div class="box-title">Alertas y Recomendaciones</div>
                <a href="#" style="font-size: 12px; font-weight: 700; color: #0284C7; text-decoration: none;">Ver todas →</a>
            </div>
            <div class="box-subtitle">Notificaciones automáticas del negocio</div>
            
            <div class="alert-card-warning">
                <div class="alert-title">⚠️ Producto con baja rotación</div>
                <div class="alert-desc">El producto "Galletas" ha disminuido su venta en un 35% en comparación con el mes anterior.</div>
            </div>
            
            <div class="alert-card-success">
                <div class="alert-title">✅ Oportunidad de crecimiento</div>
                <div class="alert-desc">La categoría de Bebidas muestra una tendencia al alza. Considera aumentar el stock.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# OTRAS PESTAÑAS (SIMULADOR Y MÓDULOS)
# ---------------------------------------------------------
elif nav_option == "Simulador":
    st.title("🧮 Simulador MYPE NexData")
    st.write("Calcula la proyección de ROI y beneficio neto adicional para tu negocio.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        fee_plan = st.selectbox("Plan de suscripción:", ["Básico (S/ 50/mes)", "Premium (S/ 150/mes)"])
        num_mypes = st.slider("Número de MYPES activas:", 10, 500, 50)
    with col_s2:
        ticket_val = 50 if "Básico" in fee_plan else 150
        mrr = num_mypes * ticket_val
        st.metric("MRR Proyectado", f"S/ {mrr:,.2f}")
        st.success(f"Logro de meta empresarial: {(mrr/5500)*100:.1f}%")

else:
    st.title(f"📊 Módulo: {nav_option}")
    st.info(f"Visualizando el análisis detallado para la sección de {nav_option}.")
