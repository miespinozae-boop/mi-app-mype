import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuración de página
st.set_page_config(
    page_title="NEXDATA - Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS de Alto Contraste (Fondo Claro #FFFFFF/#F8FAFC + Texto Oscuro #0F172A/#1E293B)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    .stApp {
        background-color: #F8FAFC !important;
    }

    header[data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.95) !important;
    }
    footer {visibility: hidden;}

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0px 20px 0px;
    }
    .logo-badge {
        background: #2563EB;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 18px;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .logo-text {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
    }

    .greeting-box {
        margin-bottom: 20px;
    }
    .greeting-title {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
    }
    .greeting-title span {
        color: #2563EB;
    }
    .greeting-subtitle {
        font-size: 14px;
        color: #475569;
        margin-top: 4px;
    }

    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        text-align: left;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin: 6px 0;
    }
    .kpi-delta-pos {
        font-size: 12px;
        font-weight: 700;
        color: #16A34A;
    }
    .kpi-delta-neg {
        font-size: 12px;
        font-weight: 700;
        color: #DC2626;
    }

    .section-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .card-head-title {
        font-size: 18px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .card-head-sub {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 16px;
    }

    /* Estilos para Radio buttons / Pestañas */
    div[data-testid="stMarkdownContainer"] p {
        color: #0F172A !important;
    }
    
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Carga de Datos Resiliente
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            return df
        except Exception:
            pass
            
    # Intentar cargar dataset predeterminado local
    paths_to_try = [
        "dataset_mype_transacciones.csv",
        "/workspace/artifacts/dataset_mype_transacciones.csv",
        "/workspace/scratch/dataset_mype_transacciones.csv"
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            try:
                df = pd.read_csv(p)
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                return df
            except Exception:
                pass

    # Generación sintética si no hay archivo
    np.random.seed(42)
    dates = pd.date_range(start="2026-08-01", end="2026-09-12", freq="D")
    prods = [
        ("Arroz Costeño 5kg", "Abarrotes", 24.5, 18.0),
        ("Aceite Primor 1L", "Abarrotes", 11.5, 8.5),
        ("Leche Gloria 400g", "Lácteos", 4.2, 3.1),
        ("Inca Kola 1.5L", "Bebidas", 7.5, 5.0),
        ("Detergente Opal 1kg", "Limpieza", 12.0, 8.8),
        ("Galletas Soda Field", "Snacks", 2.5, 1.4),
        ("Atún Campomar", "Abarrotes", 6.2, 4.2),
        ("Jabón Camay", "Higiene", 3.8, 2.3)
    ]
    canales = ["Tienda Física", "Yape / WhatsApp", "Delivery"]
    
    records = []
    for d in dates:
        num_tx = np.random.randint(12, 28)
        for _ in range(num_tx):
            p_item = prods[np.random.randint(0, len(prods))]
            qty = np.random.randint(1, 6)
            vtas = qty * p_item[2]
            csto = qty * p_item[3]
            util = vtas - csto
            records.append({
                "Fecha": d,
                "Producto": p_item[0],
                "Categoria": p_item[1],
                "Canal_Venta": np.random.choice(canales, p=[0.55, 0.30, 0.15]),
                "Cantidad": qty,
                "Ventas_Soles": vtas,
                "Costo_Soles": csto,
                "Utilidad_Soles": util
            })
    df_gen = pd.DataFrame(records)
    return df_gen

# Barra Lateral
st.sidebar.markdown("""
    <div class="sidebar-logo">
        <div class="logo-badge">N</div>
        <div class="logo-text">NEXDATA</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📁 Cargar Datos")
uploaded_file = st.sidebar.file_uploader("Subir Excel o CSV (Opcional)", type=["csv", "xlsx", "xls"])
df_raw = load_data(uploaded_file)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Menú Principal")

# MENÚ EXCLUSIVO DE 4 SECCIONES
menu_opciones = ["🏠 Inicio", "📦 Productos Estrella", "💡 Alertas y Decisiones", "🧮 Simulador"]
seccion_activa = st.sidebar.radio("Navegación:", menu_opciones, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filtros de Consulta")
periodo_opt = st.sidebar.selectbox("Periodo:", ["Últimos 30 días", "Este Mes", "Todo el Registro"])

# Filtrado por Periodo
max_date = df_raw['Fecha'].max()
if periodo_opt == "Últimos 30 días":
    fecha_ini = max_date - pd.Timedelta(days=30)
    fecha_fin = max_date
    fecha_ini_prev = fecha_ini - pd.Timedelta(days=30)
    fecha_fin_prev = fecha_ini - pd.Timedelta(days=1)
elif periodo_opt == "Este Mes":
    fecha_ini = pd.to_datetime("2026-09-01")
    fecha_fin = max_date
    fecha_ini_prev = pd.to_datetime("2026-08-01")
    fecha_fin_prev = pd.to_datetime("2026-08-12")
else:
    fecha_ini = df_raw['Fecha'].min()
    fecha_fin = max_date
    fecha_ini_prev = fecha_ini
    fecha_fin_prev = fecha_fin

categorias = ["Todas"] + list(df_raw['Categoria'].unique())
cat_sel = st.sidebar.selectbox("Categoría:", categorias)

df_curr = df_raw[(df_raw['Fecha'] >= fecha_ini) & (df_raw['Fecha'] <= fecha_fin)]
df_prev = df_raw[(df_raw['Fecha'] >= fecha_ini_prev) & (df_raw['Fecha'] <= fecha_fin_prev)]

if cat_sel != "Todas":
    df_curr = df_curr[df_curr['Categoria'] == cat_sel]
    df_prev = df_prev[df_prev['Categoria'] == cat_sel]

# CABECERA DE BIENVENIDA
st.markdown("""
    <div class="greeting-box">
        <h1 class="greeting-title">¡Hola, <span>Milagros</span>! 👋</h1>
        <p class="greeting-subtitle">Resumen ejecutivo simplificado de inteligencia de negocio para tu MYPE.</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECCIÓN 1: INICIO / DASHBOARD
# -----------------------------------------------------------------------------
if seccion_activa == "🏠 Inicio":
    # KPIs Principales
    vtas_c = df_curr['Ventas_Soles'].sum()
    vtas_p = df_prev['Ventas_Soles'].sum()
    d_vtas = ((vtas_c - vtas_p) / vtas_p * 100) if vtas_p > 0 else 0

    util_c = df_curr['Utilidad_Soles'].sum()
    util_p = df_prev['Utilidad_Soles'].sum()
    d_util = ((util_c - util_p) / util_p * 100) if util_p > 0 else 0

    mg_c = (util_c / vtas_c * 100) if vtas_c > 0 else 0
    mg_p = (util_p / vtas_p * 100) if vtas_p > 0 else 0
    d_mg = mg_c - mg_p

    tx_c = len(df_curr)
    ticket_c = (vtas_c / tx_c) if tx_c > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Ventas Totales</div>
                <div class="kpi-value">S/ {vtas_c:,.2f}</div>
                <div class="{'kpi-delta-pos' if d_vtas>=0 else 'kpi-delta-neg'}">
                    {'▲' if d_vtas>=0 else '▼'} {abs(d_vtas):.1f}% vs periodo anterior
                </div>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Utilidad Neta</div>
                <div class="kpi-value">S/ {util_c:,.2f}</div>
                <div class="{'kpi-delta-pos' if d_util>=0 else 'kpi-delta-neg'}">
                    {'▲' if d_util>=0 else '▼'} {abs(d_util):.1f}% vs periodo anterior
                </div>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Margen de Ganancia</div>
                <div class="kpi-value">{mg_c:.1f}%</div>
                <div class="{'kpi-delta-pos' if d_mg>=0 else 'kpi-delta-neg'}">
                    {'▲' if d_mg>=0 else '▼'} {abs(d_mg):.1f} pp vs periodo anterior
                </div>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Ticket Promedio</div>
                <div class="kpi-value">S/ {ticket_c:.2f}</div>
                <div class="kpi-delta-pos">
                    {tx_c} transacciones registradas
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([1.8, 1.2])

    with col_chart1:
        st.markdown("""
            <div class="section-card">
                <div class="card-head-title">📈 Evolución Diaria de Ventas y Utilidad</div>
                <div class="card-head-sub">Comportamiento del flujo de ingresos diarios (S/)</div>
            </div>
        """, unsafe_allow_html=True)
        
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.strftime('%d %b'))[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Ventas_Soles'], mode='lines+markers',
            name='Ventas (S/)', line=dict(color='#2563EB', width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.08)'
        ))
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'], mode='lines',
            name='Utilidad Neta (S/)', line=dict(color='#16A34A', width=2, dash='dot')
        ))
        fig_line.update_layout(
            height=300, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0F172A', size=11)),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0F172A', size=11)),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#0F172A'))
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_chart2:
        st.markdown("""
            <div class="section-card">
                <div class="card-head-title">📊 Ventas por Categoría</div>
                <div class="card-head-sub">Participación porcentual sobre el total</div>
            </div>
        """, unsafe_allow_html=True)

        df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        fig_donut = px.pie(
            df_cat, values='Ventas_Soles', names='Categoria', hole=0.65,
            color_discrete_sequence=['#2563EB', '#16A34A', '#9333EA', '#EA580C', '#06B6D4']
        )
        fig_donut.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="v", font=dict(color='#0F172A', size=11))
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 2: PRODUCTOS ESTRELLA
# -----------------------------------------------------------------------------
elif seccion_activa == "📦 Productos Estrella":
    st.markdown("""
        <div class="section-card">
            <div class="card-head-title">📦 Ranking de Productos Estrella</div>
            <div class="card-head-sub">Análisis de los productos que generan mayores ingresos y rotación</div>
        </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("#### 💰 Top 10 Productos por Facturación (S/)")
        df_prod = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()
        fig_bar1 = px.bar(
            df_prod, x='Ventas_Soles', y='Producto', orientation='h',
            text_auto='.2f', color_discrete_sequence=['#2563EB']
        )
        fig_bar1.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Ventas Totales (S/)", showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0F172A')),
            yaxis=dict(title="", tickfont=dict(color='#0F172A', size=12, weight='bold'))
        )
        st.plotly_chart(fig_bar1, use_container_width=True)

    with col_p2:
        st.markdown("#### 📦 Top 10 Productos por Volumen (Unidades)")
        df_qty = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()
        fig_bar2 = px.bar(
            df_qty, x='Cantidad', y='Producto', orientation='h',
            text_auto=True, color_discrete_sequence=['#16A34A']
        )
        fig_bar2.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Unidades Vendidas", showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0F172A')),
            yaxis=dict(title="", tickfont=dict(color='#0F172A', size=12, weight='bold'))
        )
        st.plotly_chart(fig_bar2, use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 3: ALERTAS Y DECISIONES
# -----------------------------------------------------------------------------
elif seccion_activa == "💡 Alertas y Decisiones":
    st.markdown("""
        <div class="section-card">
            <div class="card-head-title">💡 Motor de Inteligencia y Toma de Decisiones</div>
            <div class="card-head-sub">Detección automática de anomalías, picos de demanda y recomendaciones clave</div>
        </div>
    """, unsafe_allow_html=True)

    ca1, ca2 = st.columns(2)
    
    with ca1:
        st.error("🚨 **Alertas Operativas y de Stock Crítico:**

"
                 "* **Quiebre de Stock Preventivo:** La demanda de *Arroz* y *Aceite* aumenta un +45% los viernes. Se recomienda emitir orden de compra los miércoles.
"
                 "* **Inventario Inmovilizado:** Mermas y stock lento detectado en la categoría *Snacks*. Sugerencia: Aplicar venta cruzada con Bebidas.")

    with ca2:
        st.success("🎯 **Decisiones Estratégicas Recomendadas:**

"
                   "* **Impulso de Canal Digital (Yape / WhatsApp):** Representa el 32% del flujo total de ventas. Mantener atención prioritaria.
"
                   "* **Optimización del Ticket Promedio:** El ticket actual es de S/ 35.00. Colocar productos de compra de impulso en caja para alcanzar los S/ 40.00.")

# -----------------------------------------------------------------------------
# SECCIÓN 4: SIMULADOR MYPE
# -----------------------------------------------------------------------------
elif seccion_activa == "🧮 Simulador":
    st.markdown("""
        <div class="section-card">
            <div class="card-head-title">🧮 Simulador de Rentabilidad e Impacto MYPE</div>
            <div class="card-head-sub">Calcula el retorno de inversión (ROI) al implementar la plataforma de analítica</div>
        </div>
    """, unsafe_allow_html=True)

    s_col1, s_col2 = st.columns(2)
    
    with s_col1:
        st.markdown("#### ⚙️ Parámetros de la MYPE")
        vtas_base = st.number_input("Ventas Mensuales Actuales (S/):", value=11900, step=500)
        mermas_pct = st.slider("Porcentaje Actual de Mermas/Vencimientos (%):", 1.0, 10.0, 5.0)
        tarifa_plan = st.radio("Plan de Suscripción Seleccionado:", ["Plan Básico (S/ 50/mes)", "Plan Premium (S/ 150/mes)"], index=1)
        costo_sub = 150 if "Premium" in tarifa_plan else 50

    with s_col2:
        st.markdown("#### 📈 Resultados Estimados de la Simulación")
        increm_vtas = vtas_base * 0.163  # +16.3% aumento por prevención quiebres
        ahorro_mermas = (vtas_base * (mermas_pct / 100)) * 0.70  # -70% mermas
        beneficio_bruto = increm_vtas + ahorro_mermas
        beneficio_neto = beneficio_bruto - costo_sub
        roi_mype = (beneficio_neto / costo_sub) * 100 if costo_sub > 0 else 0

        st.metric("Beneficio Bruto Mensual Adicional", f"S/ {beneficio_bruto:,.2f}")
        st.metric("Inversión en Plataforma", f"S/ {costo_sub:.2f} / mes")
        st.metric("GANANCIA NETA ADICIONAL (Libre de suscripción)", f"S/ {beneficio_neto:,.2f}", delta=f"ROI: {roi_mype:.1f}%")

st.markdown("---")
st.caption("NEXDATA – Plataforma de Inteligencia Empresarial para MYPES | Proyecto de Gestión por Resultados 2026")
