import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y TEMA CLARO
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NexData - Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (PALETA NEXDATA - ABSOLUTAMENTE NINGÚN TEXTO BLANCO)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    /* CONFIGURACIÓN GLOBAL */
    html, body, [class*="css"], .stApp {
        font-family: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F4F7FA !important;
        color: #0B1220 !important;
    }

    /* FORZAR NINGÚN TEXTO EN COLOR BLANCO EN NINGÚN ELEMENTO */
    * {
        color: #0B1220;
    }

    header[data-testid="stHeader"] {
        background-color: rgba(244, 247, 250, 0.95) !important;
    }
    footer {visibility: hidden;}

    /* BARRA LATERAL (NEXDATA DARK PRIMARY #0E1B2E) */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42 !important;
        width: 280px !important;
    }

    section[data-testid="stSidebar"] * {
        color: #00C2D1 !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #00C2D1 !important;
        font-weight: 600 !important;
    }

    /* ISOTIPO Y LOGO EN BARRA LATERAL */
    .sidebar-logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0px 20px 0px;
    }
    .logo-badge {
        background-color: #0E1B2E;
        border: 2px solid #00C2D1;
        color: #00C2D1 !important;
        font-weight: 800;
        font-size: 18px;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .logo-title {
        font-size: 22px;
        font-weight: 800;
        color: #00C2D1 !important;
        letter-spacing: -0.5px;
    }
    .logo-subtitle {
        font-size: 11px;
        color: #8C9BAE !important;
    }

    /* CABECERA Y SALUDO MILAGROS */
    .greeting-title {
        font-size: 28px;
        font-weight: 800;
        color: #0B1220 !important;
        margin: 0;
    }
    .greeting-title span {
        color: #00C2D1 !important;
    }
    .greeting-subtitle {
        font-size: 14px;
        color: #6B7686 !important;
        margin-top: 4px;
    }

    /* TARJETAS KPI EN MAIN BODY */
    .kpi-card {
        background-color: #F4F7FA !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 4px rgba(11, 18, 32, 0.04);
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 700;
        color: #6B7686 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0B1220 !important;
        margin: 6px 0;
    }
    .kpi-trend-up {
        font-size: 12px;
        font-weight: 700;
        color: #166534 !important;
    }
    .kpi-trend-down {
        font-size: 12px;
        font-weight: 700;
        color: #92400E !important;
    }

    /* TARJETAS DE CONTENIDO GENERAL */
    .content-card {
        background-color: #F4F7FA !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: #0B1220 !important;
    }
    .card-subtitle {
        font-size: 12px;
        color: #6B7686 !important;
        margin-bottom: 15px;
    }

    /* ESTILOS DE ALERTAS Y BADGES (SIN TEXTO BLANCO) */
    .alert-box-warning {
        background-color: #FEF3C7 !important;
        border: 1px solid #FCD34D !important;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-title-warning {
        font-size: 13px;
        font-weight: 700;
        color: #92400E !important;
    }

    .alert-box-success {
        background-color: #DCFCE7 !important;
        border: 1px solid #86EFAC !important;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-title-success {
        font-size: 13px;
        font-weight: 700;
        color: #166534 !important;
    }
    .alert-desc {
        font-size: 12px;
        color: #0B1220 !important;
        margin-top: 4px;
    }

    /* PANTALLA DE ONBOARDING / SUBIR ARCHIVO */
    .onboarding-box {
        background-color: #F4F7FA !important;
        border: 2px dashed #00C2D1 !important;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
    }
    .onboarding-title {
        font-size: 24px;
        font-weight: 800;
        color: #0B1220 !important;
        margin-bottom: 10px;
    }
    .onboarding-desc {
        font-size: 14px;
        color: #6B7686 !important;
        margin-bottom: 20px;
    }

    /* CONTROLES STREAMLIT */
    .stButton button {
        background-color: #6C5CE7 !important;
        color: #0B1220 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CARGA Y PROCESAMIENTO DE DATOS EN MEMORIA
# -----------------------------------------------------------------------------
@st.cache_data
def generate_demo_dataset():
    dates = pd.date_range(start="2026-08-01", periods=30, freq="D")
    categories = ["Alimentos", "Bebidas", "Limpieza", "Higiene"]
    products_map = {
        "Alimentos": ["Arroz Costeño 5kg", "Aceite Primor 1L", "Leche Gloria 400g", "Fideos Don Vittorio"],
        "Bebidas": ["Inca Kola 1.5L", "Coca Cola 1.5L", "Agua San Mateo 2L", "Jugos Frugos"],
        "Limpieza": ["Detergente Opal 1kg", "Lejía Clorox 1L", "Jabón Bolívar"],
        "Higiene": ["Champú Head & Shoulders", "Crema Dental Kolynos", "Papel Suave"]
    }
    channels = ["Tienda Física", "WhatsApp / Yape", "Delivery"]

    rows = []
    np.random.seed(42)
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(15, 35)
        for _ in range(num_tx):
            tx_id += 1
            cat = np.random.choice(categories)
            prod = np.random.choice(products_map[cat])
            chan = np.random.choice(channels, p=[0.55, 0.30, 0.15])
            qty = np.random.randint(1, 6)
            price = round(float(np.random.uniform(4.5, 32.0)), 2)
            sales = round(qty * price, 2)
            cost = round(sales * float(np.random.uniform(0.65, 0.78)), 2)
            profit = round(sales - cost, 2)

            rows.append({
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
    return pd.DataFrame(rows)

def load_data_from_file(uploaded_file):
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        col_map = {c.lower().strip(): c for c in df.columns}
        if "fecha" in col_map:
            df['Fecha'] = pd.to_datetime(df[col_map['fecha']])
        else:
            df['Fecha'] = pd.date_range(start="2026-08-01", periods=len(df), freq="D")

        if "ventas_soles" not in df.columns and "ventas" in col_map:
            df['Ventas_Soles'] = df[col_map['ventas']]
        elif "ventas_soles" not in df.columns:
            df['Ventas_Soles'] = 100.0

        if "utilidad_soles" not in df.columns and "utilidad" in col_map:
            df['Utilidad_Soles'] = df[col_map['utilidad']]
        elif "utilidad_soles" not in df.columns:
            df['Utilidad_Soles'] = df['Ventas_Soles'] * 0.25

        if "producto" not in df.columns:
            df['Producto'] = "Producto MYPE"
        if "categoria" not in df.columns:
            df['Categoria'] = "General"
        if "canal_venta" not in df.columns:
            df['Canal_Venta'] = "Tienda Física"

        return df
    except Exception:
        return generate_demo_dataset()

# -----------------------------------------------------------------------------
# MENÚ LATERAL DE NAVEGACIÓN
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo-container">
            <div class="logo-badge">ND</div>
            <div>
                <div class="logo-title">NexData</div>
                <div class="logo-subtitle">Datos claros para tu negocio</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:12px; font-weight:700; color:#8C9BAE !important; margin-bottom:8px;'>01. BASE DE DATOS</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Cargar Excel o CSV", type=["csv", "xlsx", "xls"], label_visibility="collapsed")
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=False)

    st.markdown("<div style='margin-top:20px; font-size:12px; font-weight:700; color:#8C9BAE !important; margin-bottom:8px;'>02. MÓDULOS DEL PANEL</div>", unsafe_allow_html=True)
    menu_selection = st.radio(
        "Navegación Principal",
        ["01. Inicio", "02. Productos Estrella", "03. Alertas y Decisiones", "04. Simulador MYPE"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top:20px; font-size:12px; font-weight:700; color:#8C9BAE !important; margin-bottom:8px;'>03. CONTROL DE STOCK</div>", unsafe_allow_html=True)
    stock_umbral = st.slider("Umbral mínimo de stock (Unidades)", min_value=1, max_value=20, value=5)

# DETERMINAR DATASET A USAR
if uploaded_file is not None:
    df_raw = load_data_from_file(uploaded_file)
    data_loaded = True
elif use_demo:
    df_raw = generate_demo_dataset()
    data_loaded = True
else:
    df_raw = None
    data_loaded = False

# -----------------------------------------------------------------------------
# CABECERA Y SALUDO
# -----------------------------------------------------------------------------
col_head_l, col_head_r = st.columns([2, 1])

with col_head_l:
    st.markdown("""
        <div>
            <h1 class="greeting-title">¡Hola, <span>Milagros</span>!</h1>
            <p class="greeting-subtitle">Bienvenida a tu Panel de Inteligencia Empresarial en NexData.</p>
        </div>
    """, unsafe_allow_html=True)

with col_head_r:
    if data_loaded:
        st.markdown("""
            <div style="background-color:#DCFCE7; border:1px solid #86EFAC; border-radius:10px; padding:10px 14px; text-align:center;">
                <span style="font-size:12px; font-weight:700; color:#166534 !important;">Base de Datos Activa</span>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PANTALLA DE INICIO SI NO HAY DATOS CARGADOS
# -----------------------------------------------------------------------------
if not data_loaded:
    st.markdown("""
        <div class="onboarding-box">
            <div class="onboarding-title">Sube tus datos para comenzar</div>
            <div class="onboarding-desc">
                Sube tu archivo de ventas en Excel o CSV desde el panel lateral izquierdo,<br>
                o activa la casilla <b>"Usar datos de prueba (Demo MYPE)"</b> para explorar la plataforma en vivo.
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    # -------------------------------------------------------------------------
    # MÓDULO 01: INICIO (DASHBOARD PRINCIPAL)
    # -------------------------------------------------------------------------
    if menu_selection == "01. Inicio":
        # FILTROS SUPERIORES
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            cats = ["Todas"] + list(df_raw['Categoria'].unique())
            cat_sel = st.selectbox("Categoría:", cats)
        with f_col2:
            if cat_sel != "Todas":
                prods = ["Todos"] + list(df_raw[df_raw['Categoria'] == cat_sel]['Producto'].unique())
            else:
                prods = ["Todos"] + list(df_raw['Producto'].unique())
            prod_sel = st.selectbox("Producto:", prods)
        with f_col3:
            chans = ["Todos"] + list(df_raw['Canal_Venta'].unique())
            chan_sel = st.selectbox("Canal de Venta:", chans)

        # FILTRAR
        df_f = df_raw.copy()
        if cat_sel != "Todas":
            df_f = df_f[df_f['Categoria'] == cat_sel]
        if prod_sel != "Todos":
            df_f = df_f[df_f['Producto'] == prod_sel]
        if chan_sel != "Todos":
            df_f = df_f[df_f['Canal_Venta'] == chan_sel]

        # INDICADORES PRINCIPALES (TARJETAS KPI - SINO TEXTO BLANCO)
        vtas = df_f['Ventas_Soles'].sum()
        util = df_f['Utilidad_Soles'].sum()
        mg = (util / vtas * 100) if vtas > 0 else 0
        tx_num = len(df_f)
        ticket = (vtas / tx_num) if tx_num > 0 else 0

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Ventas Totales</div>
                    <div class="kpi-value">S/ {vtas:,.2f}</div>
                    <div class="kpi-trend-up">+12.5% vs. mes anterior</div>
                </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Utilidad Neta</div>
                    <div class="kpi-value">S/ {util:,.2f}</div>
                    <div class="kpi-trend-up">+15.2% vs. mes anterior</div>
                </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Margen de Ganancia</div>
                    <div class="kpi-value">{mg:.1f}%</div>
                    <div class="kpi-trend-up">+1.8 pp de mejora</div>
                </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Ticket Promedio</div>
                    <div class="kpi-value">S/ {ticket:.2f}</div>
                    <div class="kpi-trend-up">+3.9% gasto promedio</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

        # GRÁFICOS VISUALES CERO TEXTO BLANCO
        g_col1, g_col2 = st.columns([1.8, 1.2])

        with g_col1:
            st.markdown("""
                <div class="content-card">
                    <div class="card-title">Evolución Diaria de Ventas y Ganancia</div>
                    <div class="card-subtitle">Tendencia de facturación en Soles por día</div>
                </div>
            """, unsafe_allow_html=True)

            df_daily = df_f.groupby(df_f['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_daily['Fecha'], y=df_daily['Ventas_Soles'], mode='lines+markers',
                line=dict(color='#00C2D1', width=3, shape='spline'),
                marker=dict(size=6, color='#00C2D1'),
                fill='tozeroy', fillcolor='rgba(0, 194, 209, 0.08)', name='Ventas'
            ))
            fig_line.add_trace(go.Scatter(
                x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'], mode='lines',
                line=dict(color='#6C5CE7', width=2, dash='dot'), name='Utilidad'
            ))

            fig_line.update_layout(
                height=290, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Space Grotesk', color='#0B1220'),
                xaxis=dict(showgrid=True, gridcolor='#CBD5E1', tickfont=dict(color='#0B1220')),
                yaxis=dict(showgrid=True, gridcolor='#CBD5E1', tickfont=dict(color='#0B1220')),
                showlegend=True, legend=dict(font=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with g_col2:
            st.markdown("""
                <div class="content-card">
                    <div class="card-title">Ventas por Categoría</div>
                    <div class="card-subtitle">Participación del ingreso bruto por rubro</div>
                </div>
            """, unsafe_allow_html=True)

            df_cat = df_f.groupby('Categoria')['Ventas_Soles'].sum().reset_index()

            fig_donut = go.Figure(data=[go.Pie(
                labels=df_cat['Categoria'], values=df_cat['Ventas_Soles'], hole=0.65,
                marker=dict(colors=['#00C2D1', '#6C5CE7', '#2563EB', '#059669']),
                textinfo='percent', textfont=dict(color='#0B1220')
            )])

            fig_donut.update_layout(
                height=290, margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Space Grotesk', color='#0B1220'),
                legend=dict(orientation="v", yanchor="middle", y=0.5, font=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    # -------------------------------------------------------------------------
    # MÓDULO 02: PRODUCTOS ESTRELLA
    # -------------------------------------------------------------------------
    elif menu_selection == "02. Productos Estrella":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Ranking de Productos Estrella</div>
                <div class="card-subtitle">Identifica qué artículos generan mayor movimiento de caja</div>
            </div>
        """, unsafe_allow_html=True)

        p_col1, p_col2 = st.columns(2)

        with p_col1:
            st.subheader("Top 10 por Facturación (S/)")
            df_p1 = df_raw.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()

            fig_b1 = go.Figure(go.Bar(
                x=df_p1['Ventas_Soles'], y=df_p1['Producto'], orientation='h',
                marker=dict(color='#00C2D1')
            ))
            fig_b1.update_layout(
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Space Grotesk', color='#0B1220'),
                xaxis=dict(showgrid=True, gridcolor='#CBD5E1', tickfont=dict(color='#0B1220')),
                yaxis=dict(tickfont=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_b1, use_container_width=True)

        with p_col2:
            st.subheader("Top 10 por Unidades Vendidas")
            df_p2 = df_raw.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()

            fig_b2 = go.Figure(go.Bar(
                x=df_p2['Cantidad'], y=df_p2['Producto'], orientation='h',
                marker=dict(color='#6C5CE7')
            ))
            fig_b2.update_layout(
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Space Grotesk', color='#0B1220'),
                xaxis=dict(showgrid=True, gridcolor='#CBD5E1', tickfont=dict(color='#0B1220')),
                yaxis=dict(tickfont=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_b2, use_container_width=True)

    # -------------------------------------------------------------------------
    # MÓDULO 03: ALERTAS Y DECISIONES
    # -------------------------------------------------------------------------
    elif menu_selection == "03. Alertas y Decisiones":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Detección Automática de Problemas y Oportunidades</div>
                <div class="card-subtitle">Diagnóstico inteligente generado a partir de las transacciones registradas</div>
            </div>
        """, unsafe_allow_html=True)

        a_col1, a_col2 = st.columns(2)

        with a_col1:
            st.markdown(f"""
                <div class="alert-box-warning">
                    <div class="alert-title-warning">Riesgo de Quiebre de Stock (Umbral: {stock_umbral} un.)</div>
                    <div class="alert-desc">
                        Los productos <b>"Arroz Costeño 5kg"</b> y <b>"Aceite Primor 1L"</b> muestran alta rotación en días viernes.
                        Se recomienda emitir orden de compra los jueves.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="alert-box-warning">
                    <div class="alert-title-warning">Baja Rotación Detectada</div>
                    <div class="alert-desc">
                        La categoría <b>Higiene</b> representa solo el 8.5% de los ingresos. Evaluar promociones de venta cruzada en mostrador.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with a_col2:
            st.markdown("""
                <div class="alert-box-success">
                    <div class="alert-title-success">Oportunidad de Canal Digital</div>
                    <div class="alert-desc">
                        El canal <b>WhatsApp / Yape</b> genera el 30% del volumen total con un ticket promedio de S/ 42.00.
                        Mantener visible el código QR en caja.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="alert-box-success">
                    <div class="alert-title-success">Categoría Estrella en Crecimiento</div>
                    <div class="alert-desc">
                        La categoría <b>Bebidas</b> incrementó su margen en +4.2 pp durante el fin de semana.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MÓDULO 04: SIMULADOR MYPE
    # -------------------------------------------------------------------------
    elif menu_selection == "04. Simulador MYPE":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Simulador de Impacto Financiero en Tiempo Real</div>
                <div class="card-subtitle">Proyecta el beneficio neto adicional que obtiene tu negocio al implementar NexData</div>
            </div>
        """, unsafe_allow_html=True)

        s_col1, s_col2 = st.columns(2)

        with s_col1:
            s_ventas_actual = st.number_input("Ventas mensuales actuales (S/):", value=15000.0, step=1000.0)
            s_inc_ventas = st.slider("% Incremento estimado por reducción de mermas:", 1.0, 15.0, 5.0)
            s_tarifa = st.selectbox("Plan de Suscripción NexData:", ["Plan Básico (S/ 50/mes)", "Plan Premium (S/ 150/mes)"])

        costo_sub = 50.0 if "Básico" in s_tarifa else 150.0
        beneficio_bruto = s_ventas_actual * (s_inc_ventas / 100.0)
        beneficio_neto = beneficio_bruto - costo_sub
        roi = (beneficio_neto / costo_sub * 100) if costo_sub > 0 else 0

        with s_col2:
            st.markdown(f"""
                <div style="background-color:#F4F7FA; border:1px solid #CBD5E1; border-radius:14px; padding:20px;">
                    <div style="font-size:12px; font-weight:700; color:#6B7686 !important;">BENEFICIO NETO ADICIONAL PARA LA MYPE</div>
                    <div style="font-size:32px; font-weight:800; color:#00C2D1 !important; margin:8px 0;">S/ {beneficio_neto:,.2f} / mes</div>
                    <div style="font-size:13px; color:#0B1220 !important;"><b>Retorno de Inversión (ROI):</b> {roi:,.1f}%</div>
                    <div style="font-size:12px; color:#6B7686 !important; margin-top:8px;">
                        Demuestra que la plataforma de analítica se paga sola desde el primer mes.
                    </div>
                </div>
            """, unsafe_allow_html=True)
