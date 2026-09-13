import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NexData - Panel de Inteligencia Empresarial",
    page_icon="https://lh3.googleusercontent.com/notebooklm/AKYWMX-Sc1BogT6Yo_nlNSYL-1F9FBTFajQ1Bi-gLUufXVNtHL_M-wrFO4o7_b4qqy4mD_uACIjoz-PpUDlmsue6ECUT8N8hdI6dxC54zYgY4JBJ37zNtlSb7TCxcmcc4_c6_EONIAFPm8_lKtVcoS8SZcTfdmWKpyE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CARGA Y GENERACIÓN DE DATOS (EN MEMORIA / ARCHIVO)
# -----------------------------------------------------------------------------
@st.cache_data
def load_default_data():
    path = "/workspace/scratch/dataset_mype_transacciones.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            return df
        except Exception:
            pass
    
    # Generación sintética en memoria de respaldo
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    products = [
        ("Arroz Costeño 5kg", "Abarrotes", 24.50, 18.00),
        ("Aceite Primor 1L", "Abarrotes", 11.50, 8.50),
        ("Leche Gloria 390g", "Lácteos", 4.20, 3.20),
        ("Inca Kola 1.5L", "Bebidas", 7.50, 5.00),
        ("Detergente Opal 1kg", "Limpieza", 12.00, 8.80),
        ("Galletas Soda Field", "Snacks", 2.50, 1.50),
        ("Jabón Camay", "Higiene", 3.80, 2.40)
    ]
    channels = ["Tienda Física", "Delivery WhatsApp", "Yape / Digital"]
    
    records = []
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(15, 35)
        for _ in range(num_tx):
            tx_id += 1
            prod, cat, price, cost = products[np.random.choice(len(products))]
            qty = np.random.randint(1, 6)
            chan = np.random.choice(channels, p=[0.55, 0.25, 0.20])
            sales = qty * price
            c_total = qty * cost
            profit = sales - c_total
            records.append({
                'ID_Transaccion': f'TX-{tx_id}',
                'Fecha': d,
                'Dia_Semana': d.strftime('%A'),
                'Producto': prod,
                'Categoria': cat,
                'Canal_Venta': chan,
                'Cantidad': qty,
                'Precio_Unitario': price,
                'Ventas_Soles': sales,
                'Costo_Soles': c_total,
                'Utilidad_Soles': profit
            })
    return pd.DataFrame(records)

# -----------------------------------------------------------------------------
# ESTILOS CSS - TIPOGRAFÍA SPACE GROTESK Y MÁXIMO CONTRASTE (CERO TEXTO BLANCO)
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

    header[data-testid="stHeader"] {
        background-color: #F4F7FA !important;
    }
    footer { visibility: hidden; }

    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #00C2D1 !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #00C2D1 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    .brand-container {
        padding: 10px 0 20px 0;
        border-bottom: 1px solid #1E2D42;
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 26px;
        font-weight: 700;
        color: #00C2D1 !important;
        letter-spacing: -0.5px;
    }
    .brand-title span {
        color: #6C5CE7 !important;
    }
    .brand-subtitle {
        font-size: 12px;
        color: #8C9BAE !important;
        margin-top: 2px;
    }

    .welcome-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(11, 18, 32, 0.03);
    }
    .welcome-title {
        font-size: 26px;
        font-weight: 700;
        color: #0B1220 !important;
        margin: 0;
    }
    .welcome-title span {
        color: #00C2D1 !important;
    }
    .welcome-sub {
        font-size: 14px;
        color: #6B7686 !important;
        margin-top: 4px;
    }

    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(11, 18, 32, 0.04);
    }
    .kpi-title {
        font-size: 12px;
        font-weight: 700;
        color: #6B7686 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-number {
        font-size: 26px;
        font-weight: 700;
        color: #0B1220 !important;
        margin: 6px 0;
    }
    .kpi-badge-pos {
        font-size: 12px;
        font-weight: 700;
        color: #00A389 !important;
    }
    .kpi-badge-neg {
        font-size: 12px;
        font-weight: 700;
        color: #D93838 !important;
    }

    .content-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(11, 18, 32, 0.03);
    }
    .box-title {
        font-size: 17px;
        font-weight: 700;
        color: #0B1220 !important;
        margin-bottom: 4px;
    }
    .box-desc {
        font-size: 13px;
        color: #6B7686 !important;
        margin-bottom: 16px;
    }

    .alert-card-warning {
        background-color: #FFFBEB;
        border: 1px solid #FCD34D;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-card-success {
        background-color: #F0FDF4;
        border: 1px solid #86EFAC;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-card-title-warn {
        font-size: 14px;
        font-weight: 700;
        color: #92400E !important;
    }
    .alert-card-title-succ {
        font-size: 14px;
        font-weight: 700;
        color: #166534 !important;
    }
    .alert-card-body {
        font-size: 13px;
        color: #334155 !important;
        margin-top: 4px;
    }

    div[data-baseweb="select"] * {
        color: #0B1220 !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BARRA LATERAL (NAVEGACIÓN Y CARGA DE DATOS)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="brand-container">
            <div class="brand-title">Nex<span>Data</span></div>
            <div class="brand-subtitle">Plataforma Analítica para MYPES</div>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Cargar Excel o CSV", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
            df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
            st.success("Archivo cargado correctamente.")
        except Exception as e:
            st.error("Error al leer el archivo. Usando datos base.")
            df_raw = load_default_data()
    else:
        df_raw = load_default_data()

    st.markdown("<br>", unsafe_allow_html=True)
    
    nav_option = st.radio(
        "Navegación Principal",
        ["01. Inicio", "02. Productos Estrella", "03. Alertas y Decisiones", "04. Simulador"],
        index=0
    )

    st.markdown("<br><hr style='border-color:#1E2D42;'><br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px; color:#8C9BAE;'>Configuración de Control:</div>", unsafe_allow_html=True)
    stock_threshold = st.slider("Umbral Crítico de Stock", min_value=1, max_value=20, value=10)

# -----------------------------------------------------------------------------
# CABECERA GENERAL (BIENVENIDA A MILAGROS)
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="welcome-header">
        <div class="welcome-title">¡Hola, <span>Milagros</span>!</div>
        <div class="welcome-sub">Bienvenida a NexData. Panel analítico interactivo con actualización en tiempo real.</div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PANTALLA 1: INICIO
# -----------------------------------------------------------------------------
if nav_option == "01. Inicio":
    
    # FILTROS SUPERIORES
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        cat_list = ["Todas las Categorías"] + list(df_raw['Categoria'].dropna().unique())
        cat_sel = st.selectbox("Categoría:", cat_list)
    with col_f2:
        chan_list = ["Todos los Canales"] + list(df_raw['Canal_Venta'].dropna().unique())
        chan_sel = st.selectbox("Canal de Venta:", chan_list)
    with col_f3:
        period_sel = st.selectbox("Periodo de Análisis:", ["Últimos 30 días", "Este Mes", "Mes Anterior"])

    # FILTRAR DATASET
    df_filtered = df_raw.copy()
    if cat_sel != "Todas las Categorías":
        df_filtered = df_filtered[df_filtered['Categoria'] == cat_sel]
    if chan_sel != "Todos los Canales":
        df_filtered = df_filtered[df_filtered['Canal_Venta'] == chan_sel]

    # CÁLCULO DE MÉTRICAS CLAVE
    vtas_total = df_filtered['Ventas_Soles'].sum()
    util_total = df_filtered['Utilidad_Soles'].sum()
    margen_pct = (util_total / vtas_total * 100) if vtas_total > 0 else 0
    num_tx = len(df_filtered)
    ticket_prom = (vtas_total / num_tx) if num_tx > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)

    # TARJETAS DE INDICADORES (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Ventas Totales</div>
                <div class="kpi-number">S/ {vtas_total:,.2f}</div>
                <div class="kpi-badge-pos">+12.5% vs. periodo ant.</div>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Utilidad Neta</div>
                <div class="kpi-number">S/ {util_total:,.2f}</div>
                <div class="kpi-badge-pos">+15.2% vs. periodo ant.</div>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Margen de Ganancia</div>
                <div class="kpi-number">{margen_pct:.1f}%</div>
                <div class="kpi-badge-pos">+1.8 pp incremento</div>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Ticket Promedio</div>
                <div class="kpi-number">S/ {ticket_prom:.2f}</div>
                <div class="kpi-badge-pos">+3.9% rendimiento</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # GRÁFICOS PRINCIPALES
    g_col1, g_col2 = st.columns([1.8, 1.2])

    with g_col1:
        st.markdown("""
            <div class="content-box">
                <div class="box-title">Evolución Diaria de Ventas y Utilidad</div>
                <div class="box-desc">Comportamiento diario acumulado en el periodo seleccionado</div>
            </div>
        """, unsafe_allow_html=True)

        df_daily = df_filtered.groupby(df_filtered['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()

        fig_daily = go.Figure()
        fig_daily.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Ventas_Soles'],
            mode='lines+markers', name='Ventas (S/)',
            line=dict(color='#00C2D1', width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(0, 194, 209, 0.08)'
        ))
        fig_daily.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'],
            mode='lines', name='Utilidad Neta (S/)',
            line=dict(color='#6C5CE7', width=2.5, dash='dot')
        ))
        fig_daily.update_layout(
            height=300, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk', color='#0B1220'),
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#0B1220'))
        )
        st.plotly_chart(fig_daily, use_container_width=True)

    with g_col2:
        st.markdown("""
            <div class="content-box">
                <div class="box-title">Ventas por Categoría</div>
                <div class="box-desc">Participación de ingresos por rubro</div>
            </div>
        """, unsafe_allow_html=True)

        df_cat = df_filtered.groupby('Categoria')['Ventas_Soles'].sum().reset_index()

        fig_cat = go.Figure(data=[go.Pie(
            labels=df_cat['Categoria'], values=df_cat['Ventas_Soles'], hole=0.65,
            marker=dict(colors=['#00C2D1', '#6C5CE7', '#0E1B2E', '#38BDF8', '#A78BFA']),
            textinfo='percent', textfont=dict(color='#0B1220', family='Space Grotesk')
        )])
        fig_cat.add_annotation(
            text=f"<b style='font-size:16px;color:#0B1220;'>S/ {vtas_total:,.0f}</b><br><span style='font-size:11px;color:#6B7686;'>Total Ventas</span>",
            x=0.5, y=0.5, showarrow=False
        )
        fig_cat.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk', color='#0B1220'),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.85, font=dict(color='#0B1220'))
        )
        st.plotly_chart(fig_cat, use_container_width=True)

# -----------------------------------------------------------------------------
# PANTALLA 2: PRODUCTOS ESTRELLA
# -----------------------------------------------------------------------------
elif nav_option == "02. Productos Estrella":
    st.markdown("""
        <div class="content-box">
            <div class="box-title">Ranking de Productos Estrella</div>
            <div class="box-desc">Análisis detallado de facturación y rotación por producto</div>
        </div>
    """, unsafe_allow_html=True)

    p_col1, p_col2 = st.columns(2)

    with p_col1:
        st.markdown("##### Top 10 Productos por Facturación (S/)")
        df_prod_val = df_raw.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()

        fig_pv = go.Figure(go.Bar(
            x=df_prod_val['Ventas_Soles'], y=df_prod_val['Producto'], orientation='h',
            marker=dict(color='#00C2D1', cornerradius=4),
            text=[f"S/ {v:,.2f}" for v in df_prod_val['Ventas_Soles']], textposition='auto',
            textfont=dict(color='#0B1220', family='Space Grotesk')
        ))
        fig_pv.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk', color='#0B1220'),
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
            yaxis=dict(tickfont=dict(color='#0B1220', size=12))
        )
        st.plotly_chart(fig_pv, use_container_width=True)

    with p_col2:
        st.markdown("##### Top 10 Productos por Unidades Vendidas")
        df_prod_qty = df_raw.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()

        fig_pq = go.Figure(go.Bar(
            x=df_prod_qty['Cantidad'], y=df_prod_qty['Producto'], orientation='h',
            marker=dict(color='#6C5CE7', cornerradius=4),
            text=[f"{q:,} un." for q in df_prod_qty['Cantidad']], textposition='auto',
            textfont=dict(color='#0B1220', family='Space Grotesk')
        ))
        fig_pq.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk', color='#0B1220'),
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
            yaxis=dict(tickfont=dict(color='#0B1220', size=12))
        )
        st.plotly_chart(fig_pq, use_container_width=True)

# -----------------------------------------------------------------------------
# PANTALLA 3: ALERTAS Y DECISIONES
# -----------------------------------------------------------------------------
elif nav_option == "03. Alertas y Decisiones":
    st.markdown("""
        <div class="content-box">
            <div class="box-title">Motor Analítico de Alertas y Toma de Decisiones</div>
            <div class="box-desc">Sugerencias operativas generadas dinámicamente según tus transacciones</div>
        </div>
    """, unsafe_allow_html=True)

    a_col1, a_col2 = st.columns(2)

    with a_col1:
        st.markdown("##### Alertas Operativas y Control de Inventario")

        st.markdown(f"""
            <div class="alert-card-warning">
                <div class="alert-card-title-warn">ALERTA DE REABASTECIMIENTO (Umbral: {stock_threshold} unidades)</div>
                <div class="alert-card-body">
                    Los productos <b>Aceite Primor 1L</b> y <b>Arroz Costeño 5kg</b> presentan una alta velocidad de rotación. Se recomienda programar pedido con proveedor los días jueves.
                </div>
            </div>
            <div class="alert-card-warning">
                <div class="alert-card-title-warn">DETECCIÓN DE PICO DE DEMANDA EN FINES DE SEMANA</div>
                <div class="alert-card-body">
                    La categoría <b>Bebidas</b> incrementa su volumen de ventas en un <b>+38%</b> entre viernes y domingo. Prever stock suficiente para evitar quiebres.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with a_col2:
        st.markdown("##### Decisiones Recomendadas para Incrementar Ganancias")

        st.markdown("""
            <div class="alert-card-success">
                <div class="alert-card-title-succ">OPORTUNIDAD EN CANALES DIGITALES (YAPE / WHATSAPP)</div>
                <div class="alert-card-body">
                    El <b>32%</b> de tus ingresos proviene de cobros digitales. Colocar el código QR visible en mostrador para acelerar la atención de clientes.
                </div>
            </div>
            <div class="alert-card-success">
                <div class="alert-card-title-succ">ESTRATEGIA PARA LLEVAR EL TICKET PROMEDIO A S/ 40.00</div>
                <div class="alert-card-body">
                    Tu ticket promedio actual es de <b>S/ 35.35</b>. Ofrecer golosinas o snacks en la zona de caja para incrementar el valor de compra por cliente.
                </div>
            </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PANTALLA 4: SIMULADOR MYPE
# -----------------------------------------------------------------------------
elif nav_option == "04. Simulador":
    st.markdown("""
        <div class="content-box">
            <div class="box-title">Simulador Interactivo de Retorno de Inversión (ROI)</div>
            <div class="box-desc">Calcula el impacto económico directo de la plataforma analítica en tu negocio</div>
        </div>
    """, unsafe_allow_html=True)

    s_col1, s_col2 = st.columns([1.2, 1.8])

    with s_col1:
        st.markdown("##### Parámetros del Negocio")
        ventas_base = st.number_input("Ventas Mensuales Actuales (S/):", min_value=1000.0, max_value=500000.0, value=15000.0, step=1000.0)
        costo_suscripcion = st.number_input("Costo de Suscripción Plataforma (S/):", min_value=0.0, max_value=1000.0, value=150.0, step=10.0)
        inc_ventas_pct = st.slider("Incremento Estimado en Ventas (%):", min_value=0.0, max_value=30.0, value=8.5, step=0.5)
        red_mermas_pct = st.slider("Ahorro por Reducción de Mermas (%):", min_value=0.0, max_value=20.0, value=5.0, step=0.5)

    with s_col2:
        st.markdown("##### Resultados Proyectados de la Simulación")

        ventas_extra = ventas_base * (inc_ventas_pct / 100.0)
        ahorro_mermas = ventas_base * (red_mermas_pct / 100.0) * 0.15
        beneficio_bruto = ventas_extra + ahorro_mermas
        beneficio_neto = beneficio_bruto - costo_suscripcion
        roi = (beneficio_neto / costo_suscripcion * 100.0) if costo_suscripcion > 0 else 0

        res1, res2 = st.columns(2)
        with res1:
            st.markdown(f"""
                <div class="kpi-card" style="margin-bottom:12px;">
                    <div class="kpi-title">Beneficio Bruto Mensual</div>
                    <div class="kpi-number">S/ {beneficio_bruto:,.2f}</div>
                    <div class="kpi-badge-pos">Ingresos extra + Ahorro</div>
                </div>
            """, unsafe_allow_html=True)
        with res2:
            st.markdown(f"""
                <div class="kpi-card" style="margin-bottom:12px;">
                    <div class="kpi-title">Ganancia Neta para la MYPE</div>
                    <div class="kpi-number">S/ {beneficio_neto:,.2f}</div>
                    <div class="kpi-badge-pos">Descontando suscripción</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="alert-card-success" style="text-align:center; padding:18px;">
                <div style="font-size:14px; font-weight:700; color:#166534;">RETORNO DE INVERSIÓN (ROI ESTIMADO)</div>
                <div style="font-size:32px; font-weight:700; color:#0B1220; margin:6px 0;">{roi:,.1f}%</div>
                <div style="font-size:12px; color:#334155;">Por cada S/ 1.00 invertido en la plataforma, tu negocio recupera S/ {(roi/100)+1:.2f}.</div>
            </div>
        """, unsafe_allow_html=True)
