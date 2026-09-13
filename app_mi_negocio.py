import streamlit as st
import pandas as pd
import numpy as np
import datetime

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y FAVICON
# -----------------------------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
  <circle cx="30" cy="72" r="8" fill="#FFFFFF"/>
  <circle cx="52" cy="54" r="8" fill="#FFFFFF"/>
  <circle cx="74" cy="36" r="9" fill="#6C5CE7"/>
  <line x1="30" y1="72" x2="74" y2="36" stroke="#00C2D1" stroke-width="8" stroke-linecap="round"/>
  <path d="M 60 22 L 82 22 L 82 44" fill="none" stroke="#6C5CE7" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

favicon_uri = f"data:image/svg+xml;utf8,{FAVICON_SVG.replace('#', '%23').replace(chr(10), '')}"

st.set_page_config(
    page_title="NexData – Panel de Inteligencia Empresarial",
    page_icon=favicon_uri,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar favicon en la cabecera HTML
st.markdown(f"""
<head>
    <link rel="icon" type="image/svg+xml" href="{favicon_uri}">
</head>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. ESTILOS CSS PROFESIONALES (NEXDATA PALETTE & SPACE GROTESK)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
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

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42;
    }

    section[data-testid="stSidebar"] * {
        color: #8C9BAE !important;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #00C2D1 !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Radio buttons navegación */
    div[data-testid="stSidebarUserContent"] div.row-widget.stRadio > div {
        background-color: transparent;
        gap: 6px;
    }

    div[data-testid="stSidebarUserContent"] div.row-widget.stRadio label {
        background-color: #162438;
        border: 1px solid #1E2D42;
        border-radius: 10px;
        padding: 10px 14px;
        color: #8C9BAE !important;
        font-weight: 600;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    div[data-testid="stSidebarUserContent"] div.row-widget.stRadio label:hover {
        border-color: #00C2D1;
        color: #00C2D1 !important;
    }

    div[data-testid="stSidebarUserContent"] div.row-widget.stRadio label[data-checked="true"] {
        background-color: #00C2D1 !important;
        border-color: #00C2D1 !important;
        color: #0E1B2E !important;
        font-weight: 700;
    }

    /* Encabezados y títulos */
    .greeting-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #0B1220;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .greeting-title span {
        color: #00C2D1;
    }
    .greeting-subtitle {
        font-size: 14px;
        color: #6B7686;
        margin-top: 4px;
        margin-bottom: 20px;
    }

    /* Tarjetas de Métricas KPI */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(14, 27, 46, 0.03);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    .kpi-icon-box {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 700;
    }
    .icon-cyan { background-color: #E6F9FA; color: #00A3B0; }
    .icon-purple { background-color: #F0EDFF; color: #6C5CE7; }
    .icon-green { background-color: #E6F7ED; color: #10B981; }
    .icon-amber { background-color: #FFF7E6; color: #D97706; }

    .kpi-label { font-size: 12px; font-weight: 700; color: #6B7686; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; color: #0B1220; margin: 4px 0; letter-spacing: -0.5px; }
    .kpi-trend { font-size: 12px; font-weight: 700; color: #10B981; }

    /* Tarjetas de Contenido general */
    .content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 15px rgba(14, 27, 46, 0.03);
        margin-bottom: 20px;
    }
    .card-title { font-family: 'Space Grotesk', sans-serif; font-size: 17px; font-weight: 700; color: #0B1220; }
    .card-subtitle { font-size: 12px; color: #6B7686; margin-bottom: 16px; }

    /* Estilos de Alertas */
    .alert-card {
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 4px solid;
    }
    .alert-critical { background-color: #FEF2F2; border-color: #EF4444; color: #991B1B; }
    .alert-warning { background-color: #FFFBEB; border-color: #F59E0B; color: #92400E; }
    .alert-success { background-color: #ECFDF5; border-color: #10B981; color: #065F46; }

    /* Empty state */
    .empty-state-box {
        background: #FFFFFF;
        border: 2px dashed #CBD5E1;
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        margin: 30px 0;
    }
    .empty-state-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 8px;
    }
    .empty-state-desc {
        font-size: 14px;
        color: #6B7686;
        max-width: 500px;
        margin: 0 auto 20px auto;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL (LOGO SVG + FILTROS)
# -----------------------------------------------------------------------------
with st.sidebar:
    # Logo SVG NexData oficial
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 14px; padding: 10px 0 25px 0;">
            <svg width="44" height="44" viewBox="0 0 100 100" style="border-radius: 12px; flex-shrink: 0;">
                <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
                <circle cx="30" cy="72" r="8" fill="#FFFFFF"/>
                <circle cx="52" cy="54" r="8" fill="#FFFFFF"/>
                <circle cx="74" cy="36" r="9" fill="#6C5CE7"/>
                <line x1="30" y1="72" x2="74" y2="36" stroke="#00C2D1" stroke-width="8" stroke-linecap="round"/>
                <path d="M 60 22 L 82 22 L 82 44" fill="none" stroke="#6C5CE7" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; line-height: 1;">
                    <span style="color: #FFFFFF;">Nex</span><span style="color: #00C2D1;">Data</span>
                </div>
                <div style="font-size: 11px; color: #8C9BAE; margin-top: 3px;">Datos claros para tu negocio</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #00C2D1; letter-spacing: 1px; margin-bottom: 10px;'>NAVEGACIÓN</div>", unsafe_allow_html=True)
    
    nav_option = st.radio(
        "Navegación Principal",
        ["01. Inicio", "02. Productos Estrella", "03. Alertas y Decisiones", "04. Simulador MYPE"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: #1E2D42; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #00C2D1; letter-spacing: 1px; margin-bottom: 10px;'>ORIGEN DE DATOS</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Cargar base de datos (Excel / CSV)", type=["csv", "xlsx", "xls"])
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=True)

    st.markdown("<hr style='border-color: #1E2D42; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #00C2D1; letter-spacing: 1px; margin-bottom: 10px;'>PARÁMETROS DE NEGOCIO</div>", unsafe_allow_html=True)

    stock_threshold = st.slider("Umbral Crítico de Stock (Unidades)", min_value=10, max_value=100, value=30, step=5)

# -----------------------------------------------------------------------------
# 4. CARGA Y PROCESAMIENTO ROBUSTO DE DATOS
# -----------------------------------------------------------------------------
@st.cache_data
def generate_demo_dataset():
    dates = pd.date_range(start="2026-08-01", periods=30, freq="D")
    categories = ["Alimentos", "Bebidas", "Limpieza", "Higiene", "Otros"]
    products_map = {
        "Alimentos": [("Arroz 1kg", 3.8, 5.0), ("Aceite 1L", 7.5, 10.5), ("Fideos 500g", 2.2, 3.5)],
        "Bebidas": [("Gaseosa 1.5L", 4.0, 6.5), ("Agua 2L", 1.8, 3.0), ("Jugo 1L", 3.2, 5.0)],
        "Limpieza": [("Detergente 1kg", 6.0, 9.0), ("Lejía 1L", 2.5, 4.0), ("Jabón Líquido", 4.5, 7.0)],
        "Higiene": [("Shampoo 400ml", 9.0, 14.0), ("Crema Dental", 3.5, 5.5)],
        "Otros": [("Snack Mix", 1.5, 2.8), ("Galletas Pack", 2.0, 3.5)]
    }
    channels = ["Tienda física", "Delivery", "Online", "Otros"]
    
    rows = []
    np.random.seed(42)
    tx_id = 1000
    
    for d in dates:
        num_tx = np.random.randint(25, 40)
        for _ in range(num_tx):
            tx_id += 1
            cat = np.random.choice(categories, p=[0.35, 0.25, 0.18, 0.12, 0.10])
            prod_info = products_map[cat][np.random.choice(len(products_map[cat]))]
            prod_name, cost_u, price_u = prod_info
            qty = np.random.randint(1, 6)
            channel = np.random.choice(channels, p=[0.45, 0.30, 0.15, 0.10])
            
            sales_soles = qty * price_u
            cost_soles = qty * cost_u
            profit_soles = sales_soles - cost_soles
            
            rows.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": d,
                "Dia_Semana": d.strftime("%A"),
                "Producto": prod_name,
                "Categoria": cat,
                "Canal_Venta": channel,
                "Cantidad": qty,
                "Precio_Unitario": price_u,
                "Ventas_Soles": sales_soles,
                "Costo_Soles": cost_soles,
                "Utilidad_Soles": profit_soles
            })
            
    df = pd.DataFrame(rows)
    return df

df_data = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_data = pd.read_csv(uploaded_file)
        else:
            df_data = pd.read_excel(uploaded_file)
        
        if "Fecha" in df_data.columns:
            df_data["Fecha"] = pd.to_datetime(df_data["Fecha"])
    except Exception as e:
        st.error(f"Error al procesar el archivo subido: {e}")

elif use_demo:
    df_data = generate_demo_dataset()

# -----------------------------------------------------------------------------
# 5. PANTALLAS DE LA APLICACIÓN
# -----------------------------------------------------------------------------

# CASO 1: SIN DATOS (EMPTY STATE)
if df_data is None:
    st.markdown("""
        <div style="margin-top: 20px;">
            <h1 class="greeting-title">¡Hola, <span>Milagros</span>!</h1>
            <p class="greeting-subtitle">Bienvenida a tu Panel de Inteligencia Empresarial NexData.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="empty-state-box">
            <div style="font-size: 48px; margin-bottom: 15px;">📊</div>
            <div class="empty-state-title">Sube tus datos para comenzar</div>
            <div class="empty-state-desc">
                Carga tu archivo de ventas en formato Excel (.xlsx) o CSV en el menú lateral, o marca la casilla 
                <b>"Usar datos de prueba (Demo MYPE)"</b> para explorar las métricas e indicadores en tiempo real.
            </div>
        </div>
    """, unsafe_allow_html=True)

# CASO 2: CON DATOS ACTIVOS
else:
    # Header común
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-top: 10px;">
            <div>
                <h1 class="greeting-title">¡Hola, <span>Milagros</span>!</h1>
                <p class="greeting-subtitle">Resumen ejecutivo en tiempo real para la toma de decisiones estratégicas.</p>
            </div>
            <div style="background: #E6F9FA; border: 1px solid #B2F0F4; border-radius: 20px; padding: 6px 16px; font-size: 12px; font-weight: 700; color: #00A3B0;">
                Datos Activos: Demo MYPE (30 Días)
            </div>
        </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # PANTALLA 1: INICIO / DASHBOARD PRINCIPAL
    # -------------------------------------------------------------------------
    if nav_option == "01. Inicio":
        import plotly.graph_objects as go

        vtas_total = df_data["Ventas_Soles"].sum()
        util_total = df_data["Utilidad_Soles"].sum()
        mg_prom = (util_total / vtas_total * 100) if vtas_total > 0 else 0
        num_tx = len(df_data)
        ticket_prom = (vtas_total / num_tx) if num_tx > 0 else 0

        # Tarjetas KPI (4 Columnas)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <div class="kpi-icon-box icon-cyan">S/</div>
                        <div class="kpi-label">Ventas Totales</div>
                    </div>
                    <div class="kpi-value">S/ {vtas_total:,.2f}</div>
                    <div class="kpi-trend">↑ +12.5% <span style="color:#6B7686; font-weight:500;">vs. mes anterior</span></div>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <div class="kpi-icon-box icon-purple">S/</div>
                        <div class="kpi-label">Utilidad Neta</div>
                    </div>
                    <div class="kpi-value">S/ {util_total:,.2f}</div>
                    <div class="kpi-trend">↑ +15.2% <span style="color:#6B7686; font-weight:500;">vs. mes anterior</span></div>
                </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <div class="kpi-icon-box icon-green">%</div>
                        <div class="kpi-label">Margen de Ganancia</div>
                    </div>
                    <div class="kpi-value">{mg_prom:.1f}%</div>
                    <div class="kpi-trend">↑ +1.8 pp <span style="color:#6B7686; font-weight:500;">vs. mes anterior</span></div>
                </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <div class="kpi-icon-box icon-amber">S/</div>
                        <div class="kpi-label">Ticket Promedio</div>
                    </div>
                    <div class="kpi-value">S/ {ticket_prom:.2f}</div>
                    <div class="kpi-trend">↑ +3.9% <span style="color:#6B7686; font-weight:500;">vs. mes anterior</span></div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

        # Gráficos Principales
        g_col1, g_col2 = st.columns([1.8, 1.2])

        with g_col1:
            st.markdown("""
                <div class="content-card">
                    <div class="card-title">Evolución Diaria de Ventas y Utilidad</div>
                    <div class="card-subtitle">Comportamiento diario de ingresos y ganancia neta</div>
            """, unsafe_allow_html=True)

            df_daily = df_data.groupby(df_data["Fecha"].dt.date)[["Ventas_Soles", "Utilidad_Soles"]].sum().reset_index()
            df_daily["Fecha_Str"] = df_daily["Fecha"].astype(str)

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_daily["Fecha_Str"], y=df_daily["Ventas_Soles"], mode="lines+markers",
                name="Ventas (S/)", line=dict(color="#00C2D1", width=3, shape="spline"),
                fill="tozeroy", fillcolor="rgba(0, 194, 209, 0.08)"
            ))
            fig_line.add_trace(go.Scatter(
                x=df_daily["Fecha_Str"], y=df_daily["Utilidad_Soles"], mode="lines",
                name="Utilidad (S/)", line=dict(color="#6C5CE7", width=2, dash="dash")
            ))

            fig_line.update_layout(
                height=290, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=10, color="#6B7686")),
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=10, color="#6B7686")),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color="#0B1220"))
            )
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with g_col2:
            st.markdown("""
                <div class="content-card">
                    <div class="card-title">Ventas por Categoría</div>
                    <div class="card-subtitle">Distribución porcentual de los ingresos</div>
            """, unsafe_allow_html=True)

            df_cat = df_data.groupby("Categoria")["Ventas_Soles"].sum().reset_index()
            cat_colors = ["#00C2D1", "#6C5CE7", "#10B981", "#F59E0B", "#3B82F6"]

            fig_donut = go.Figure(data=[go.Pie(
                labels=df_cat["Categoria"], values=df_cat["Ventas_Soles"], hole=0.68,
                marker=dict(colors=cat_colors), textinfo="none", hoverinfo="label+value+percent"
            )])

            fig_donut.add_annotation(
                text=f"<b style='font-size:18px;color:#0B1220;'>S/ {vtas_total:,.0f}</b><br><span style='font-size:11px;color:#6B7686;'>Ventas totales</span>",
                x=0.5, y=0.5, showarrow=False, font=dict(family="Space Grotesk")
            )

            fig_donut.update_layout(
                height=290, margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.78, font=dict(size=11, color="#0B1220"))
            )
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # PANTALLA 2: PRODUCTOS ESTRELLA
    # -------------------------------------------------------------------------
    elif nav_option == "02. Productos Estrella":
        import plotly.graph_objects as go

        st.markdown("""
            <div class="content-card">
                <div class="card-title">Ranking de Productos Estrella</div>
                <div class="card-subtitle">Análisis detallado de rotación e ingresos por producto</div>
        """, unsafe_allow_html=True)

        col_p1, col_p2 = st.columns(2)

        with col_p1:
            st.markdown("<div style='font-weight:700; color:#0B1220; margin-bottom:12px;'>Top 10 Productos por Facturación (S/)</div>", unsafe_allow_html=True)
            df_p_sales = df_data.groupby("Producto")["Ventas_Soles"].sum().sort_values(ascending=True).tail(10).reset_index()

            fig_bar_sales = go.Figure(go.Bar(
                x=df_p_sales["Ventas_Soles"], y=df_p_sales["Producto"], orientation="h",
                marker=dict(color="#00C2D1", cornerradius=6),
                text=df_p_sales["Ventas_Soles"].apply(lambda x: f"S/ {x:,.0f}"), textposition="inside",
                textfont=dict(color="#0E1B2E", size=11, family="Space Grotesk")
            ))
            fig_bar_sales.update_layout(
                height=380, margin=dict(l=0, r=10, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=10, color="#6B7686")),
                yaxis=dict(tickfont=dict(size=11, color="#0B1220"))
            )
            st.plotly_chart(fig_bar_sales, use_container_width=True)

        with col_p2:
            st.markdown("<div style='font-weight:700; color:#0B1220; margin-bottom:12px;'>Top 10 Productos por Unidades Vendidas</div>", unsafe_allow_html=True)
            df_p_qty = df_data.groupby("Producto")["Cantidad"].sum().sort_values(ascending=True).tail(10).reset_index()

            fig_bar_qty = go.Figure(go.Bar(
                x=df_p_qty["Cantidad"], y=df_p_qty["Producto"], orientation="h",
                marker=dict(color="#6C5CE7", cornerradius=6),
                text=df_p_qty["Cantidad"].apply(lambda x: f"{x} un."), textposition="inside",
                textfont=dict(color="#0E1B2E", size=11, family="Space Grotesk")
            ))
            fig_bar_qty.update_layout(
                height=380, margin=dict(l=0, r=10, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=10, color="#6B7686")),
                yaxis=dict(tickfont=dict(size=11, color="#0B1220"))
            )
            st.plotly_chart(fig_bar_qty, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # PANTALLA 3: ALERTAS Y DECISIONES
    # -------------------------------------------------------------------------
    elif nav_option == "03. Alertas y Decisiones":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Motor Analítico de Alertas y Toma de Decisiones</div>
                <div class="card-subtitle">Detección automática de anomalías y recomendaciones estratégicas</div>
        """, unsafe_allow_html=True)

        # Evaluar inventario crítico según el slider
        df_prod_summary = df_data.groupby("Producto")["Cantidad"].sum().reset_index()
        critical_prods = df_prod_summary[df_prod_summary["Cantidad"] < stock_threshold]

        col_a1, col_a2 = st.columns(2)

        with col_a1:
            st.markdown("<div style='font-weight:700; color:#0B1220; margin-bottom:14px;'>Detección de Anomalías Operativas</div>", unsafe_allow_html=True)

            if len(critical_prods) > 0:
                prod_names = ", ".join(critical_prods["Producto"].tolist())
                st.markdown(f"""
                    <div class="alert-card alert-critical">
                        <div style="font-weight:700; font-size:14px; margin-bottom:4px;">Riesgo Crítico de Quiebre de Stock</div>
                        <div style="font-size:12px;">Los siguientes productos presentan ventas por debajo del umbral recomendado ({stock_threshold} un.): <b>{prod_names}</b>. Se sugiere reabastecer inventario inmediatamente.</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="alert-card alert-success">
                        <div style="font-weight:700; font-size:14px; margin-bottom:4px;">Inventario Saludable</div>
                        <div style="font-size:12px;">Todos los productos superan el umbral mínimo establecido de {stock_threshold} unidades vendidas.</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("""
                <div class="alert-card alert-warning">
                    <div style="font-weight:700; font-size:14px; margin-bottom:4px;">Pico de Demanda Fin de Semana</div>
                    <div style="font-size:12px;">El 58% de las ventas de la categoría <b>Bebidas</b> se concentra los sábados y domingos. Coordinar pedidos con proveedores los días jueves.</div>
                </div>
            """, unsafe_allow_html=True)

        with col_a2:
            st.markdown("<div style='font-weight:700; color:#0B1220; margin-bottom:14px;'>Acciones Estratégicas Recomendadas</div>", unsafe_allow_html=True)

            st.markdown("""
                <div class="alert-card alert-success">
                    <div style="font-weight:700; font-size:14px; margin-bottom:4px;">Impulso de Venta Cruzada (Combos)</div>
                    <div style="font-size:12px;">Aprovechar el alto margen de la categoría <b>Snacks</b> creando combos junto con las marcas principales de <b>Bebidas</b> para elevar el ticket promedio a S/ 40.00.</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="alert-card alert-success">
                    <div style="font-weight:700; font-size:14px; margin-bottom:4px;">Fidelización en Canal Digital</div>
                    <div style="font-size:12px;">El canal <b>Delivery / Yape</b> representa el 30% del volumen total. Implementar código QR visible en mostrador y confirmación rápida por WhatsApp.</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # PANTALLA 4: SIMULADOR MYPE
    # -------------------------------------------------------------------------
    elif nav_option == "04. Simulador MYPE":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Simulador Financiero e Impacto Económico para la MYPE</div>
                <div class="card-subtitle">Proyección interactiva de incremento en utilidad y retorno de inversión (ROI)</div>
        """, unsafe_allow_html=True)

        s_col1, s_col2 = st.columns([1.2, 1.8])

        with s_col1:
            st.markdown("<div style='font-weight:700; color:#0B1220; margin-bottom:12px;'>Parámetros del Simulador</div>", unsafe_allow_html=True)

            sub_plan = st.selectbox("Plan de Suscripción NexData", ["Plan Básico (S/ 50/mes)", "Plan Premium (S/ 150/mes)"])
            fee_mype = 50.0 if "Básico" in sub_plan else 150.0

            sales_base = df_data["Ventas_Soles"].sum()
            profit_base = df_data["Utilidad_Soles"].sum()

            pct_growth = st.slider("Incremento Proyectado en Ventas (%)", min_value=0.0, max_value=25.0, value=8.0, step=0.5)
            pct_waste_red = st.slider("Reducción Proyectada de Mermas/Costos (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)

        with s_col2:
            st.markdown("<div style='font-weight:700; color:#0B1220; margin-bottom:12px;'>Proyección de Beneficio Neto MYPE</div>", unsafe_allow_html=True)

            add_sales = sales_base * (pct_growth / 100.0)
            red_cost = (sales_base - profit_base) * (pct_waste_red / 100.0)
            gross_benefit = add_sales * 0.28 + red_cost
            net_benefit = gross_benefit - fee_mype
            roi_mype = (net_benefit / fee_mype * 100.0) if fee_mype > 0 else 0

            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.metric("Beneficio Bruto Adicional", f"S/ {gross_benefit:,.2f}")
                st.metric("Inversión Mensual NexData", f"S/ {fee_mype:,.2f}")
            with res_c2:
                st.metric("Beneficio Neto Mensual", f"S/ {net_benefit:,.2f}")
                st.metric("Retorno de Inversión (ROI)", f"{roi_mype:,.0f}%")

            st.markdown(f"""
                <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:12px; padding:14px; margin-top:15px; color:#065F46; font-size:13px;">
                    <b>Conclusión del Simulador:</b> Al suscribirse al <b>{sub_plan}</b>, la MYPE obtiene un beneficio neto de 
                    <b>S/ {net_benefit:,.2f}/mes</b>, lo que representa un retorno del <b>{roi_mype:,.0f}%</b> sobre el costo de la plataforma.
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
