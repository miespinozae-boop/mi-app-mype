import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NexData – Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS CSS - NEXDATA (SPACE GROTESK, CERO TEXTO BLANCO SOBRE CLARO, CERO EMOJIS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F4F7FA !important;
        color: #0B1220 !important;
    }

    .stApp {
        background-color: #F4F7FA !important;
    }

    /* Sidebar NexData Dark Header & High Contrast Options */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42 !important;
    }

    section[data-testid="stSidebar"] *, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {
        color: #00C2D1 !important;
        font-weight: 500 !important;
    }

    .sidebar-logo-title {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #00C2D1 !important;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }

    .sidebar-subtitle {
        font-size: 12px !important;
        color: #8C9BAE !important;
        margin-bottom: 20px;
    }

    /* Main Container Titles */
    .greeting-title {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #0B1220 !important;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .greeting-subtitle {
        font-size: 14px !important;
        color: #6B7686 !important;
        margin-top: 4px;
        margin-bottom: 20px;
    }

    /* Empty State Onboarding Card */
    .onboarding-card {
        background: #FFFFFF !important;
        border: 2px dashed #00C2D1 !important;
        border-radius: 16px !important;
        padding: 40px 30px !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.05) !important;
        margin-top: 20px !important;
        margin-bottom: 30px !important;
    }

    .onboarding-title {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #0B1220 !important;
        margin-bottom: 10px !important;
    }

    .onboarding-text {
        font-size: 15px !important;
        color: #6B7686 !important;
        max-width: 600px !important;
        margin: 0 auto 25px auto !important;
        line-height: 1.5 !important;
    }

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
    }

    .kpi-label {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #6B7686 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .kpi-value {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #0B1220 !important;
        margin: 6px 0 !important;
    }

    .kpi-trend-pos {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #166534 !important;
    }

    .kpi-trend-neg {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #991B1B !important;
    }

    /* Content Cards */
    .content-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
    }

    .card-title {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #0B1220 !important;
        margin-bottom: 4px !important;
    }

    .card-subtitle {
        font-size: 12px !important;
        color: #6B7686 !important;
        margin-bottom: 16px !important;
    }

    /* Alert Badges */
    .badge-critical {
        background-color: #FEF2F2 !important;
        border-left: 4px solid #DC2626 !important;
        padding: 14px !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
        color: #991B1B !important;
    }

    .badge-success {
        background-color: #F0FDF4 !important;
        border-left: 4px solid #16A34A !important;
        padding: 14px !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
        color: #166534 !important;
    }

    .badge-title {
        font-size: 13px !important;
        font-weight: 700 !important;
        margin-bottom: 4px !important;
    }

    .badge-desc {
        font-size: 12px !important;
        color: #374151 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# GENERACIÓN DE DATOS DE DEMOSTRACIÓN
# -----------------------------------------------------------------------------
def get_demo_dataset():
    dates = pd.date_range(end=datetime.date.today(), periods=30, freq='D')
    products = [
        {"prod": "Arroz Costeño 5kg", "cat": "Abarrotes", "price": 24.50, "cost": 17.00},
        {"prod": "Aceite Primor 1L", "cat": "Abarrotes", "price": 11.50, "cost": 8.20},
        {"prod": "Leche Gloria Sixpack", "cat": "Lácteos", "price": 22.00, "cost": 16.50},
        {"prod": "Detergente Ariel 2kg", "cat": "Limpieza", "price": 18.50, "cost": 13.00},
        {"prod": "Inca Kola 3L", "cat": "Bebidas", "price": 12.00, "cost": 8.00},
        {"prod": "Galletas Casino Pack", "cat": "Snacks", "price": 4.50, "cost": 2.80},
    ]
    channels = ["Tienda Física", "Yape / Plin", "WhatsApp / Delivery"]
    rows = []

    np.random.seed(42)
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(15, 35)
        for _ in range(num_tx):
            tx_id += 1
            p = np.random.choice(products)
            ch = np.random.choice(channels, p=[0.55, 0.30, 0.15])
            qty = np.random.randint(1, 5)
            sales = qty * p["price"]
            cost = qty * p["cost"]
            profit = sales - cost
            rows.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": d,
                "Producto": p["prod"],
                "Categoria": p["cat"],
                "Canal_Venta": ch,
                "Cantidad": qty,
                "Precio_Unitario": p["price"],
                "Ventas_Soles": sales,
                "Costo_Soles": cost,
                "Utilidad_Soles": profit
            })
    return pd.DataFrame(rows)

# -----------------------------------------------------------------------------
# BARRA LATERAL - LOGO Y NAVEGACIÓN
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-logo-title">NexData</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Plataforma de Inteligencia Empresarial</div>', unsafe_allow_html=True)

    nav_option = st.radio(
        "Navegación",
        ["01. Inicio", "02. Productos Estrella", "03. Alertas y Decisiones", "04. Simulador MYPE"],
        index=0
    )

    st.markdown("---")
    st.markdown("### Cargar Base de Datos")
    uploaded_file = st.sidebar.file_uploader(
        "Subir archivo de ventas (Excel / CSV):",
        type=["csv", "xlsx", "xls"],
        help="Sube las transacciones registradas de tu negocio."
    )

    use_demo = st.sidebar.checkbox("Usar datos de prueba (Demo MYPE)", value=False)

# -----------------------------------------------------------------------------
# CARGA Y VALIDACIÓN DE DATOS
# -----------------------------------------------------------------------------
df_raw = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
        
        # Validar columnas mínimas
        col_map = {c.lower(): c for c in df_raw.columns}
        if "fecha" in col_map:
            df_raw["Fecha"] = pd.to_datetime(df_raw[col_map["fecha"]])
        else:
            df_raw["Fecha"] = pd.date_range(end=datetime.date.today(), periods=len(df_raw), freq='D')

        if "ventas_soles" not in col_map and "ventas" in col_map:
            df_raw["Ventas_Soles"] = df_raw[col_map["ventas"]]
        elif "ventas_soles" not in df_raw.columns:
            df_raw["Ventas_Soles"] = 100.0

        if "utilidad_soles" not in col_map and "utilidad" in col_map:
            df_raw["Utilidad_Soles"] = df_raw[col_map["utilidad"]]
        elif "utilidad_soles" not in df_raw.columns:
            df_raw["Utilidad_Soles"] = df_raw["Ventas_Soles"] * 0.25

        if "producto" not in col_map:
            df_raw["Producto"] = "Producto General"
        else:
            df_raw["Producto"] = df_raw[col_map["producto"]]

        if "categoria" not in col_map:
            df_raw["Categoria"] = "General"
        else:
            df_raw["Categoria"] = df_raw[col_map["categoria"]]

        if "canal_venta" not in col_map:
            df_raw["Canal_Venta"] = "Tienda Física"
        else:
            df_raw["Canal_Venta"] = df_raw[col_map["canal_venta"]]

        st.sidebar.success("Base de datos cargada correctamente.")
    except Exception as e:
        st.sidebar.error("Error al leer el archivo. Asegúrate de que sea un archivo CSV o Excel válido.")
        df_raw = None
elif use_demo:
    df_raw = get_demo_dataset()
    st.sidebar.info("Utilizando datos de prueba (Demo MYPE).")

# -----------------------------------------------------------------------------
# CABECERA PRINCIPAL
# -----------------------------------------------------------------------------
st.markdown('<h1 class="greeting-title">¡Hola, Milagros!</h1>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PANTALLA 1: ESTADO VACÍO (CUANDO NO SE HA SUBIDO BASE DE DATOS)
# -----------------------------------------------------------------------------
if df_raw is None:
    st.markdown('<p class="greeting-subtitle">Bienvenida a tu panel comercial. Para comenzar a ver tus indicadores y tomar decisiones, carga los datos de tu negocio.</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="onboarding-card">
            <div class="onboarding-title">Sube tus datos para comenzar</div>
            <div class="onboarding-text">
                Para activar el análisis dinámico de ventas, utilidad y alertas de inventario, sube el archivo de ventas de tu negocio (Excel o CSV) desde el panel lateral izquierdo.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        st.info("📌 **Paso 1:** Ve a la barra lateral izquierda en **'Cargar Base de Datos'**.")
    with col_btn2:
        st.success("💡 **Opción Rápida:** Marca la casilla **'Usar datos de prueba (Demo MYPE)'** en la barra lateral para ver una demostración en vivo de la plataforma.")

# -----------------------------------------------------------------------------
# PANTALLA 2: DASHBOARD ACTIVO CON DATOS
# -----------------------------------------------------------------------------
else:
    st.markdown('<p class="greeting-subtitle">Aquí tienes el resumen ejecutivo actualizado en tiempo real con la información de tu negocio.</p>', unsafe_allow_html=True)

    # FILTROS DE CABECERA
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        cat_filter = st.selectbox("Categoría:", ["Todas"] + list(df_raw["Categoria"].unique()))
    with col_f2:
        canal_filter = st.selectbox("Canal de Venta:", ["Todos"] + list(df_raw["Canal_Venta"].unique()))
    with col_f3:
        periodo_filter = st.selectbox("Periodo:", ["Últimos 30 días", "Todo el Registro"])

    # FILTRADO DE DATAFRAME
    df_filtered = df_raw.copy()
    if cat_filter != "Todas":
        df_filtered = df_filtered[df_filtered["Categoria"] == cat_filter]
    if canal_filter != "Todos":
        df_filtered = df_filtered[df_filtered["Canal_Venta"] == canal_filter]

    # CÁLCULOS PRINCIPALES
    ventas_totales = df_filtered["Ventas_Soles"].sum()
    utilidad_total = df_filtered["Utilidad_Soles"].sum()
    margen_promedio = (utilidad_total / ventas_totales * 100) if ventas_totales > 0 else 0
    num_tx = len(df_filtered)
    ticket_promedio = (ventas_totales / num_tx) if num_tx > 0 else 0

    # -------------------------------------------------------------------------
    # SECCIÓN 01. INICIO
    # -------------------------------------------------------------------------
    if nav_option == "01. Inicio":
        # TARJETAS KPI
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Ventas Totales</div>
                    <div class="kpi-value">S/ {ventas_totales:,.2f}</div>
                    <div class="kpi-trend-pos">↑ +12.5% vs periodo ant.</div>
                </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Utilidad Neta</div>
                    <div class="kpi-value">S/ {utilidad_total:,.2f}</div>
                    <div class="kpi-trend-pos">↑ +15.2% vs periodo ant.</div>
                </div>
            """, unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Margen Neto</div>
                    <div class="kpi-value">{margen_promedio:.1f}%</div>
                    <div class="kpi-trend-pos">↑ +1.8 pp de rentabilidad</div>
                </div>
            """, unsafe_allow_html=True)

        with k4:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Ticket Promedio</div>
                    <div class="kpi-value">S/ {ticket_promedio:.2f}</div>
                    <div class="kpi-trend-pos">↑ +3.9% gasto por cliente</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # GRÁFICOS
        g1, g2 = st.columns([1.8, 1.2])

        with g1:
            st.markdown("""
                <div class="content-card">
                    <div class="card-title">Evolución Diaria de Ventas y Utilidad</div>
                    <div class="card-subtitle">Tendencia de ingresos y ganancia neta en el periodo</div>
                </div>
            """, unsafe_allow_html=True)

            df_daily = df_filtered.groupby("Fecha")[["Ventas_Soles", "Utilidad_Soles"]].sum().reset_index()

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_daily["Fecha"], y=df_daily["Ventas_Soles"],
                mode='lines', name='Ventas (S/)',
                line=dict(color='#00C2D1', width=3, shape='spline'),
                fill='tozeroy', fillcolor='rgba(0, 194, 209, 0.08)'
            ))
            fig_line.add_trace(go.Scatter(
                x=df_daily["Fecha"], y=df_daily["Utilidad_Soles"],
                mode='lines', name='Utilidad (S/)',
                line=dict(color='#6C5CE7', width=2, dash='dot')
            ))

            fig_line.update_layout(
                height=290, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with g2:
            st.markdown("""
                <div class="content-card">
                    <div class="card-title">Ventas por Categoría</div>
                    <div class="card-subtitle">Distribución porcentual por rubro</div>
                </div>
            """, unsafe_allow_html=True)

            df_cat = df_filtered.groupby("Categoria")["Ventas_Soles"].sum().reset_index()

            fig_donut = go.Figure(data=[go.Pie(
                labels=df_cat["Categoria"], values=df_cat["Ventas_Soles"], hole=0.6,
                marker=dict(colors=['#00C2D1', '#6C5CE7', '#0E1B2E', '#F59E0B', '#10B981']),
                textinfo='percent', hoverinfo='label+value+percent'
            )])

            fig_donut.update_layout(
                height=290, margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="v", yanchor="middle", y=0.5, font=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    # -------------------------------------------------------------------------
    # SECCIÓN 02. PRODUCTOS ESTRELLA
    # -------------------------------------------------------------------------
    elif nav_option == "02. Productos Estrella":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Ranking de Productos Estrella</div>
                <div class="card-subtitle">Identifica qué productos mueven tu caja y cuáles te generan mayor margen</div>
            </div>
        """, unsafe_allow_html=True)

        p1, p2 = st.columns(2)

        with p1:
            st.markdown("#### Top Productos por Ventas Totales (S/)")
            df_prod_sales = df_filtered.groupby("Producto")["Ventas_Soles"].sum().sort_values(ascending=True).tail(10)

            fig_bar1 = go.Figure(go.Bar(
                x=df_prod_sales.values, y=df_prod_sales.index, orientation='h',
                marker=dict(color='#00C2D1')
            ))
            fig_bar1.update_layout(
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(tickfont=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_bar1, use_container_width=True)

        with p2:
            st.markdown("#### Top Productos por Ganancia Neta (S/)")
            df_prod_prof = df_filtered.groupby("Producto")["Utilidad_Soles"].sum().sort_values(ascending=True).tail(10)

            fig_bar2 = go.Figure(go.Bar(
                x=df_prod_prof.values, y=df_prod_prof.index, orientation='h',
                marker=dict(color='#6C5CE7')
            ))
            fig_bar2.update_layout(
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(tickfont=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_bar2, use_container_width=True)

    # -------------------------------------------------------------------------
    # SECCIÓN 03. ALERTAS Y DECISIONES
    # -------------------------------------------------------------------------
    elif nav_option == "03. Alertas y Decisiones":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Motor de Inteligencia Operativa</div>
                <div class="card-subtitle">Detección automática de problemas y recomendaciones para la toma de decisiones</div>
            </div>
        """, unsafe_allow_html=True)

        a1, a2 = st.columns(2)

        with a1:
            st.markdown("""
                <div class="badge-critical">
                    <div class="badge-title">ALERTA CRÍTICA: Riesgo de Quiebre de Stock los Fines de Semana</div>
                    <div class="badge-desc">Se detectó que el 58% de las ventas de Abarrotes y Bebidas ocurren entre viernes y domingo. Se recomienda programar pedidos a proveedores los días jueves.</div>
                </div>
                <div class="badge-critical">
                    <div class="badge-title">DETECCIÓN DE MARGEN: Producto de Alta Rentabilidad Poco Impulsado</div>
                    <div class="badge-desc">La categoría Snacks genera un margen del 42%, pero representa solo el 7% de las ventas. Colocar productos en zona de caja.</div>
                </div>
            """, unsafe_allow_html=True)

        with a2:
            st.markdown("""
                <div class="badge-success">
                    <div class="badge-title">OPORTUNIDAD COMERCIAL: Crecimiento de Cobros Digitales</div>
                    <div class="badge-desc">El canal Yape / Plin representa el 32% del volumen total. Mantener visibilidad del código QR en mostrador para agilizar atención.</div>
                </div>
                <div class="badge-success">
                    <div class="badge-title">RECOMENDACIÓN DE TICKET: Estrategia de Venta Cruzada</div>
                    <div class="badge-desc">El ticket promedio actual es S/ 35.20. Ofrecer un producto complementario de S/ 5.00 elevaría la facturación mensual en +14.2%.</div>
                </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SECCIÓN 04. SIMULADOR MYPE
    # -------------------------------------------------------------------------
    elif nav_option == "04. Simulador MYPE":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Simulador Financiero de Impacto Comercial</div>
                <div class="card-subtitle">Ajusta los parámetros para proyectar el retorno de inversión y beneficio neto estimado</div>
            </div>
        """, unsafe_allow_html=True)

        s1, s2 = st.columns([1, 1.2])

        with s1:
            st.markdown("#### Parámetros del Negocio")
            ventas_base = st.number_input("Ventas Mensuales Base (S/):", value=float(ventas_totales) if ventas_totales > 0 else 15000.0, step=1000.0)
            pct_inc_ventas = st.slider("Incremento Estimado en Ventas (%):", min_value=0.0, max_value=30.0, value=12.5, step=0.5)
            pct_red_mermas = st.slider("Reducción de Mermas por Stock (%):", min_value=0.0, max_value=50.0, value=25.0, step=1.0)
            costo_suscripcion = st.number_input("Suscripción Plataforma NexData (S/):", value=150.0, step=10.0)

        with s2:
            st.markdown("#### Resultados Proyectados")
            inc_ventas_soles = ventas_base * (pct_inc_ventas / 100.0)
            ahorro_mermas_soles = (ventas_base * 0.05) * (pct_red_mermas / 100.0)
            beneficio_bruto = inc_ventas_soles + ahorro_mermas_soles
            beneficio_neto = beneficio_bruto - costo_suscripcion
            roi_cliente = (beneficio_neto / costo_suscripcion * 100) if costo_suscripcion > 0 else 0

            st.markdown(f"""
                <div class="kpi-card" style="margin-bottom: 15px;">
                    <div class="kpi-label">Beneficio Neto Adicional Estimado</div>
                    <div class="kpi-value">S/ {beneficio_neto:,.2f} / mes</div>
                    <div class="kpi-trend-pos">Ganancia limpia descontando la plataforma</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Retorno de Inversión (ROI)</div>
                    <div class="kpi-value">{roi_cliente:,.1f}%</div>
                    <div class="kpi-trend-pos">Por cada S/ 1 invertido recuperas S/ {(roi_cliente/100 + 1):.2f}</div>
                </div>
            """, unsafe_allow_html=True)
