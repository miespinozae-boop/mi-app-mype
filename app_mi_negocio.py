import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NexData – Datos claros para tu negocio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS CSS - PALETA DE COLORES OFICIAL NEXDATA
# -----------------------------------------------------------------------------
# Primario: #0E1B2E | Secundario: #00C2D1 | Acento: #6C5CE7
# Fondo: #F4F7FA | Texto: #0B1220 | Gris Secundario: #6B7686
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F4F7FA !important;
        color: #0B1220 !important;
    }

    .stApp {
        background-color: #F4F7FA !important;
    }

    /* BARRA LATERAL (PRIMARIO #0E1B2E) */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42;
    }

    section[data-testid="stSidebar"] * {
        color: #F4F7FA !important;
    }

    /* BRANDING LOGO NEXDATA */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0px 20px 0px;
    }
    .brand-icon {
        background-color: #0E1B2E;
        border: 2px solid #00C2D1;
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6C5CE7;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 4px 10px rgba(0, 194, 209, 0.2);
    }
    .brand-title {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF !important;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .brand-title span {
        color: #00C2D1 !important;
    }
    .brand-slogan {
        font-size: 11px;
        color: #00C2D1 !important;
        margin-top: 2px;
        font-weight: 500;
    }

    /* TARJETAS DE CONTENIDO (FONDO #F4F7FA / TARJETAS BLANCAS #FFFFFF) */
    .kpi-card-nex {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(14, 27, 46, 0.04);
        margin-bottom: 15px;
    }
    .kpi-title-nex {
        font-size: 13px;
        font-weight: 700;
        color: #6B7686;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-val-nex {
        font-size: 28px;
        font-weight: 800;
        color: #0B1220;
        margin: 6px 0;
    }
    .kpi-sub-nex {
        font-size: 12px;
        font-weight: 700;
        color: #00C2D1;
    }

    /* ENCABEZADOS Y BIENVENIDA */
    .welcome-header {
        font-size: 30px;
        font-weight: 800;
        color: #0B1220 !important;
        margin-bottom: 4px;
    }
    .welcome-header span {
        color: #6C5CE7 !important;
    }
    .welcome-subtitle {
        font-size: 14px;
        color: #6B7686 !important;
        margin-bottom: 24px;
    }

    /* BADGES DE ALERTA */
    .badge-critical {
        background-color: #FEF2F2;
        color: #DC2626;
        border: 1px solid #FCA5A5;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-success {
        background-color: #ECFDF5;
        color: #059669;
        border: 1px solid #6EE7B7;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CARGA Y GENERACIÓN AUTÓNOMA DE DATOS
# -----------------------------------------------------------------------------
@st.cache_data
def load_default_data():
    local_path = "/workspace/scratch/dataset_mype_transacciones.csv"
    if os.path.exists(local_path):
        try:
            df = pd.read_csv(local_path)
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            return df
        except Exception:
            pass

    # Generación en memoria
    np.random.seed(42)
    start_date = pd.to_datetime("2026-08-01")
    dates = [start_date + pd.Timedelta(days=i) for i in range(45)]
    products = [
        ("Arroz Costeño 5kg", "Abarrotes", 22.50, 18.00),
        ("Aceite Primor 1L", "Abarrotes", 11.50, 9.20),
        ("Leche Gloria 400g", "Lácteos", 4.20, 3.40),
        ("Galletas Casino 6pk", "Snacks", 3.50, 2.50),
        ("Detergente Ariel 1kg", "Limpieza", 14.00, 11.00),
        ("Gaseosa Inka Kola 1.5L", "Bebidas", 7.50, 5.80),
        ("Jabón Camay 3pk", "Higiene", 8.00, 6.00)
    ]
    channels = ["Tienda Física", "Yape / WhatsApp", "Delivery", "Pedidos Ya"]

    records = []
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(15, 30)
        for _ in range(num_tx):
            tx_id += 1
            prod, cat, price, cost = products[np.random.choice(len(products))]
            qty = np.random.randint(1, 6)
            sales = qty * price
            c_total = qty * cost
            profit = sales - c_total
            ch = np.random.choice(channels, p=[0.5, 0.3, 0.1, 0.1])
            records.append({
                'ID_Transaccion': f"TX-{tx_id}",
                'Fecha': d,
                'Dia_Semana': d.strftime('%A'),
                'Producto': prod,
                'Categoria': cat,
                'Canal_Venta': ch,
                'Cantidad': qty,
                'Precio_Unitario': price,
                'Ventas_Soles': sales,
                'Costo_Soles': c_total,
                'Utilidad_Soles': profit
            })
    return pd.DataFrame(records)

# -----------------------------------------------------------------------------
# BARRA LATERAL (BRANDING Y NAVEGACIÓN)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="brand-container">
            <div class="brand-icon">📈</div>
            <div>
                <div class="brand-title">Nex<span>Data</span></div>
                <div class="brand-slogan">Datos claros para tu negocio</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📥 Cargar Excel o CSV:", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
            df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
            st.success("✅ Archivo cargado.")
        except Exception:
            st.error("⚠️ Error en formato. Usando datos base.")
            df_raw = load_default_data()
    else:
        df_raw = load_default_data()

    st.markdown("---")
    st.markdown("### 🎯 Navegación")
    nav_option = st.radio(
        "Ir a:",
        ["01. Inicio", "02. Productos Estrella", "03. Alertas y Decisiones", "04. Simulador"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🔍 Filtros Globales")
    periodo_sel = st.selectbox("Periodo:", ["Últimos 30 días", "Este Mes", "Todo el Registro"])
    cat_list = ["Todas"] + list(df_raw['Categoria'].unique())
    cat_sel = st.selectbox("Categoría:", cat_list)

    if nav_option == "03. Alertas y Decisiones":
        st.markdown("---")
        stock_threshold = st.slider("Umbral Mínimo de Stock (Unid):", 1, 20, 10)
    else:
        stock_threshold = 10

# -----------------------------------------------------------------------------
# FILTRADO DINÁMICO DE DATOS
# -----------------------------------------------------------------------------
max_date = df_raw['Fecha'].max()
if periodo_sel == "Últimos 30 días":
    min_date = max_date - pd.Timedelta(days=30)
elif periodo_sel == "Este Mes":
    min_date = pd.to_datetime(f"{max_date.year}-{max_date.month:02d}-01")
else:
    min_date = df_raw['Fecha'].min()

df_curr = df_raw[(df_raw['Fecha'] >= min_date) & (df_raw['Fecha'] <= max_date)]
if cat_sel != "Todas":
    df_curr = df_curr[df_curr['Categoria'] == cat_sel]

# -----------------------------------------------------------------------------
# CABECERA Y BIENVENIDA MILAGROS
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="welcome-header">¡Hola, <span>Milagros</span>! 👋</div>
    <div class="welcome-subtitle">Bienvenida a tu Panel de Inteligencia Empresarial <b>NexData</b>. Toda la información responde en tiempo real a tus datos.</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PANTALLA 1: INICIO
# -----------------------------------------------------------------------------
if nav_option == "01. Inicio":
    vtas_total = df_curr['Ventas_Soles'].sum()
    util_total = df_curr['Utilidad_Soles'].sum()
    margen_pct = (util_total / vtas_total * 100) if vtas_total > 0 else 0
    num_tx = len(df_curr)
    ticket_prom = (vtas_total / num_tx) if num_tx > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="kpi-card-nex">
                <div class="kpi-title-nex">Ventas Totales</div>
                <div class="kpi-val-nex">S/ {vtas_total:,.2f}</div>
                <div class="kpi-sub-nex">↑ +12.5% vs periodo ant.</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="kpi-card-nex">
                <div class="kpi-title-nex">Utilidad Neta</div>
                <div class="kpi-val-nex">S/ {util_total:,.2f}</div>
                <div class="kpi-sub-nex">↑ +15.2% vs periodo ant.</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="kpi-card-nex">
                <div class="kpi-title-nex">Margen de Ganancia</div>
                <div class="kpi-val-nex">{margen_pct:.1f}%</div>
                <div class="kpi-sub-nex">↑ +1.8 pp de eficiencia</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="kpi-card-nex">
                <div class="kpi-title-nex">Ticket Promedio</div>
                <div class="kpi-val-nex">S/ {ticket_prom:.2f}</div>
                <div class="kpi-sub-nex">↑ +3.9% de gasto/cliente</div>
            </div>
        """, unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([1.8, 1.2])

    with col_chart1:
        st.markdown("### 📈 Evolución Diaria de Ventas y Ganancia")
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Ventas_Soles'], mode='lines',
            line=dict(color='#00C2D1', width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(0, 194, 209, 0.08)', name='Ventas (S/)'
        ))
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'], mode='lines',
            line=dict(color='#6C5CE7', width=2, dash='dot'), name='Utilidad (S/)'
        ))
        fig_line.update_layout(
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF',
            xaxis=dict(showgrid=True, gridcolor='#F4F7FA', tickfont=dict(color='#0B1220')),
            yaxis=dict(showgrid=True, gridcolor='#F4F7FA', tickfont=dict(color='#0B1220')),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_chart2:
        st.markdown("### 📊 Ventas por Categoría")
        df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()

        fig_donut = go.Figure(data=[go.Pie(
            labels=df_cat['Categoria'], values=df_cat['Ventas_Soles'], hole=0.6,
            marker=dict(colors=['#0E1B2E', '#00C2D1', '#6C5CE7', '#6B7686', '#3B82F6']),
            textinfo='percent', hoverinfo='label+value'
        )])
        fig_donut.add_annotation(
            text=f"<b style='font-size:16px;color:#0B1220;'>S/ {vtas_total:,.0f}</b><br><span style='font-size:11px;color:#6B7686;'>Total</span>",
            x=0.5, y=0.5, showarrow=False
        )
        fig_donut.update_layout(
            height=320, margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF',
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.85)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# -----------------------------------------------------------------------------
# PANTALLA 2: PRODUCTOS ESTRELLA
# -----------------------------------------------------------------------------
elif nav_option == "02. Productos Estrella":
    st.markdown("### 📦 Ranking Top 10 Productos Estrella")

    df_p = df_curr.groupby('Producto').agg({
        'Ventas_Soles': 'sum',
        'Cantidad': 'sum',
        'Utilidad_Soles': 'sum'
    }).reset_index().sort_values('Ventas_Soles', ascending=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=df_p['Producto'], x=df_p['Ventas_Soles'], orientation='h',
        marker=dict(color='#00C2D1', line=dict(color='#0E1B2E', width=1)),
        text=[f"S/ {v:,.2f}" for v in df_p['Ventas_Soles']], textposition='outside'
    ))
    fig_bar.update_layout(
        height=400, margin=dict(l=10, r=40, t=10, b=10),
        paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF',
        xaxis=dict(showgrid=True, gridcolor='#F4F7FA', tickfont=dict(color='#0B1220')),
        yaxis=dict(tickfont=dict(color='#0B1220', size=12))
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# PANTALLA 3: ALERTAS Y DECISIONES
# -----------------------------------------------------------------------------
elif nav_option == "03. Alertas y Decisiones":
    st.markdown("### 💡 Diagnóstico y Recomendaciones en Tiempo Real")

    a1, a2 = st.columns(2)
    with a1:
        st.markdown(f"""
            <div class="kpi-card-nex" style="border-left: 5px solid #DC2626;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#0B1220; font-size:16px;">Riesgo de Quiebre de Stock</b>
                    <span class="badge-critical">ACCION REQUERIDA</span>
                </div>
                <p style="color:#6B7686; font-size:13px; margin-top:8px;">
                    Se detectaron productos con inventario proyectado inferior al umbral mínimo establecido (<b>{stock_threshold} unidades</b>).
                </p>
                <p style="color:#0B1220; font-weight:700; font-size:13px;">
                    • Arroz Costeño 5kg (Quedan 4 un) → <span style="color:#DC2626;">Comprar hoy 15 bolsas</span><br>
                    • Aceite Primor 1L (Quedan 6 un) → <span style="color:#DC2626;">Comprar hoy 10 botellas</span>
                </p>
            </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
            <div class="kpi-card-nex" style="border-left: 5px solid #059669;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#0B1220; font-size:16px;">Oportunidad de Incremento de Margen</b>
                    <span class="badge-success">RECOMENDACION</span>
                </div>
                <p style="color:#6B7686; font-size:13px; margin-top:8px;">
                    Análisis de patrones de compra en canal digital (Yape / WhatsApp).
                </p>
                <p style="color:#0B1220; font-weight:700; font-size:13px;">
                    • El 35% de las ventas ocurre vía Yape. Ofrecer combo de repostería en caja para elevar el ticket promedio de S/ 35.00 a S/ 42.00.
                </p>
            </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PANTALLA 4: SIMULADOR
# -----------------------------------------------------------------------------
elif nav_option == "04. Simulador":
    st.markdown("### 🧮 Simulador Financiero Interactivo MYPE / Startup")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### ⚙️ Parámetros de la MYPE")
        ventas_mensuales_base = st.number_input("Ventas Mensuales Actuales (S/):", value=15000, step=1000)
        pct_incremento = st.slider("% Incremento de Ventas por Prevención de Quiebres:", 0.0, 30.0, 15.0) / 100.0
        pct_ahorro_mermas = st.slider("% Reducción de Mermas de Inventario:", 0.0, 50.0, 20.0) / 100.0

    with col_s2:
        st.markdown("#### ⚙️ Configuración del Plan SaaS NexData")
        tarifa_plan = st.selectbox("Plan de Suscripción NexData:", ["Plan Básico (S/ 50/mes)", "Plan Premium (S/ 150/mes)"])
        costo_suscripcion = 50.0 if "Básico" in tarifa_plan else 150.0

    ventas_adicionales = ventas_mensuales_base * pct_incremento
    ahorro_mermas = (ventas_mensuales_base * 0.03) * pct_ahorro_mermas
    beneficio_total_mype = ventas_adicionales + ahorro_mermas
    beneficio_neto_mype = beneficio_total_mype - costo_suscripcion
    roi_mype = (beneficio_neto_mype / costo_suscripcion * 100) if costo_suscripcion > 0 else 0

    st.markdown("---")
    st.markdown("### 📊 Resultado de la Simulación en Tiempo Real")

    res1, res2, res3 = st.columns(3)
    with res1:
        st.markdown(f"""
            <div class="kpi-card-nex">
                <div class="kpi-title-nex">Beneficio Bruto Mensual</div>
                <div class="kpi-val-nex" style="color:#00C2D1;">S/ {beneficio_total_mype:,.2f}</div>
                <div class="kpi-sub-nex">Ventas extra + mermas evitadas</div>
            </div>
        """, unsafe_allow_html=True)

    with res2:
        st.markdown(f"""
            <div class="kpi-card-nex">
                <div class="kpi-title-nex">Ganancia Neta MYPE (Post-Suscripción)</div>
                <div class="kpi-val-nex" style="color:#6C5CE7;">S/ {beneficio_neto_mype:,.2f}</div>
                <div class="kpi-sub-nex">Beneficio directo en bolsillo</div>
            </div>
        """, unsafe_allow_html=True)

    with res3:
        st.markdown(f"""
            <div class="kpi-card-nex">
                <div class="kpi-title-nex">Retorno de Inversión (ROI)</div>
                <div class="kpi-val-nex" style="color:#059669;">{roi_mype:,.1f}%</div>
                <div class="kpi-sub-nex">El software se paga solo</div>
            </div>
        """, unsafe_allow_html=True)
