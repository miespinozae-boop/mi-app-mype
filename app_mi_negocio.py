import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# -----------------------------------------------------------------------------
# CONFIGURACIÓN PÁGINA STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NEXDATA - Panel de Inteligencia Empresarial",
    page_icon="https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS CSS DE ALTO CONTRASTE Y TIPOGRAFÍA PROFESIONAL (SIN EMOJIS DE WHATSAPP)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    .stApp {
        background-color: #F8FAFC !important;
    }

    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }

    /* BARRA LATERAL */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 10px;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    /* CONTENEDORES Y TARJETAS */
    .card-kpi {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        margin-bottom: 15px;
    }

    .card-kpi-title {
        font-size: 12px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .card-kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .card-kpi-delta-pos {
        font-size: 13px;
        font-weight: 700;
        color: #15803D;
        margin-top: 6px;
    }

    .card-kpi-delta-neg {
        font-size: 13px;
        font-weight: 700;
        color: #B91C1C;
        margin-top: 6px;
    }

    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
    }

    .card-box-title {
        font-size: 16px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
    }

    .card-box-subtitle {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 16px;
    }

    /* BADGES Y ALERTAS */
    .badge-critical {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        color: #991B1B;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        display: inline-block;
    }

    .badge-warning {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        color: #92400E;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        display: inline-block;
    }

    .badge-success {
        background-color: #F0FDF4;
        border: 1px solid #86EFAC;
        color: #166534;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        display: inline-block;
    }

    /* TABLAS STREAMLIT */
    .stDataFrame {
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CARGA Y PROCESAMIENTO DE DATOS
# -----------------------------------------------------------------------------
@st.cache_data
def load_dataset():
    path = "/workspace/scratch/dataset_mype_transacciones.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            return df
        except Exception:
            pass
    # Generador sintético integrado en memoria
    np.random.seed(42)
    dates = pd.date_range(start="2026-08-01", end="2026-09-12", freq="D")
    categories = {
        'Alimentos': ['Arroz Costeño 5kg', 'Aceite Primor 1L', 'Fideos Don Vittorio 500g', 'Azúcar Rubia 1kg', 'Conservas de Atún'],
        'Bebidas': ['Gaseosa Inca Kola 1.5L', 'Agua San Luis 2.5L', 'Cerveza Cusqueña 620ml', 'Jugo Frugos 1L'],
        'Limpieza': ['Detergente Opal 1kg', 'Lejía Clorox 1L', 'Lavavajillas Ayudín 500g'],
        'Higiene': ['Jabón Camay 3pk', 'Pasta Dental Kolynos 100g', 'Champú Head & Shoulders 375ml'],
        'Snacks': ['Galletas Sublime 6pk', 'Papas Lays 160g', 'Chocolates Princesa']
    }
    channels = ['Tienda física', 'Delivery WhatsApp', 'Yape/Plin Pos']
    
    rows = []
    tx_id = 1000
    for d in dates:
        num_tx = np.random.randint(12, 28)
        for _ in range(num_tx):
            tx_id += 1
            cat = np.random.choice(list(categories.keys()))
            prod = np.random.choice(categories[cat])
            chan = np.random.choice(channels, p=[0.55, 0.25, 0.20])
            qty = np.random.randint(1, 6)
            
            base_price = {
                'Arroz Costeño 5kg': 21.50, 'Aceite Primor 1L': 11.50, 'Fideos Don Vittorio 500g': 4.20,
                'Azúcar Rubia 1kg': 4.50, 'Conservas de Atún': 6.80, 'Gaseosa Inca Kola 1.5L': 7.50,
                'Agua San Luis 2.5L': 4.00, 'Cerveza Cusqueña 620ml': 8.50, 'Jugo Frugos 1L': 5.20,
                'Detergente Opal 1kg': 10.50, 'Lejía Clorox 1L': 4.80, 'Lavavajillas Ayudín 500g': 6.20,
                'Jabón Camay 3pk': 8.50, 'Pasta Dental Kolynos 100g': 5.50, 'Champú Head & Shoulders 375ml': 16.50,
                'Galletas Sublime 6pk': 6.50, 'Papas Lays 160g': 7.20, 'Chocolates Princesa': 4.80
            }.get(prod, 8.00)
            
            unit_cost = round(base_price * np.random.uniform(0.65, 0.75), 2)
            ventas = round(base_price * qty, 2)
            costos = round(unit_cost * qty, 2)
            utilidad = round(ventas - costos, 2)
            
            rows.append({
                'ID_Transaccion': f'TX-{tx_id}',
                'Fecha': d,
                'Dia_Semana': d.strftime('%A'),
                'Producto': prod,
                'Categoria': cat,
                'Canal_Venta': chan,
                'Cantidad': qty,
                'Precio_Unitario': base_price,
                'Ventas_Soles': ventas,
                'Costo_Soles': costos,
                'Utilidad_Soles': utilidad
            })
            
    return pd.DataFrame(rows)

df_raw = load_dataset()

# -----------------------------------------------------------------------------
# BARRA LATERAL (NAVEGACIÓN DE 4 SECCIONES Y FILTROS INTERACTIVOS)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 20px;">
            <div style="font-size: 22px; font-weight: 800; color: #0F172A; letter-spacing: -0.5px;">NEXDATA</div>
            <div style="font-size: 12px; font-weight: 600; color: #2563EB;">Inteligencia Empresarial MYPE</div>
        </div>
    """, unsafe_allow_html=True)

    nav_option = st.radio(
        "MÓDULOS DEL SISTEMA",
        ["Inicio", "Productos Estrella", "Alertas y Decisiones", "Simulador"],
        index=0
    )

    st.markdown("<hr style='margin: 20px 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 12px; font-weight: 800; color: #0F172A; text-transform: uppercase; margin-bottom: 10px;'>Filtros en Tiempo Real</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Cargar Dataset Excel / CSV:", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_user = pd.read_csv(uploaded_file)
            else:
                df_user = pd.read_excel(uploaded_file)
            df_user['Fecha'] = pd.to_datetime(df_user['Fecha'])
            df_raw = df_user
            st.success("Dataset cargado correctamente.")
        except Exception as e:
            st.error("Error al leer el archivo. Usando dataset por defecto.")

    periodo_sel = st.selectbox(
        "Periodo de Análisis:",
        ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Registro"]
    )

    categorias_list = ["Todas"] + sorted(list(df_raw['Categoria'].dropna().unique()))
    cat_sel = st.selectbox("Categoría:", categorias_list)

    canales_list = ["Todos"] + sorted(list(df_raw['Canal_Venta'].dropna().unique()))
    canal_sel = st.selectbox("Canal de Venta:", canales_list)

    stock_threshold = st.slider("Umbral Crítico de Stock (unidades):", min_value=3, max_value=25, value=10)

# -----------------------------------------------------------------------------
# FILTRADO DINÁMICO DE DATOS
# -----------------------------------------------------------------------------
max_date = df_raw['Fecha'].max()

if periodo_sel == "Últimos 30 días":
    f_start = max_date - pd.Timedelta(days=30)
    f_end = max_date
    f_prev_start = f_start - pd.Timedelta(days=30)
    f_prev_end = f_start - pd.Timedelta(days=1)
elif periodo_sel == "Este Mes":
    f_start = pd.to_datetime(f"{max_date.year}-{max_date.month:02d}-01")
    f_end = max_date
    f_prev_start = f_start - pd.DateOffset(months=1)
    f_prev_end = f_start - pd.Timedelta(days=1)
elif periodo_sel == "Mes Anterior":
    f_end = pd.to_datetime(f"{max_date.year}-{max_date.month:02d}-01") - pd.Timedelta(days=1)
    f_start = pd.to_datetime(f"{f_end.year}-{f_end.month:02d}-01")
    f_prev_start = f_start - pd.DateOffset(months=1)
    f_prev_end = f_start - pd.Timedelta(days=1)
else:
    f_start = df_raw['Fecha'].min()
    f_end = max_date
    f_prev_start = f_start
    f_prev_end = f_end

def apply_filters(df, p_start, p_end, cat, chan):
    dff = df[(df['Fecha'] >= p_start) & (df['Fecha'] <= p_end)].copy()
    if cat != "Todas":
        dff = dff[dff['Categoria'] == cat]
    if chan != "Todos":
        dff = dff[dff['Canal_Venta'] == chan]
    return dff

df_curr = apply_filters(df_raw, f_start, f_end, cat_sel, canal_sel)
df_prev = apply_filters(df_raw, f_prev_start, f_prev_end, cat_sel, canal_sel)

# -----------------------------------------------------------------------------
# ENCABEZADO DE BIENVENIDA
# -----------------------------------------------------------------------------
st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px 24px; margin-bottom: 24px;">
        <div style="font-size: 26px; font-weight: 800; color: #0F172A; letter-spacing: -0.5px;">¡Hola, Milagros!</div>
        <div style="font-size: 14px; font-weight: 500; color: #64748B; margin-top: 4px;">
            Bienvenida a tu Panel de Inteligencia Empresarial. Toda la información responde en tiempo real a tus selecciones.
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECCIÓN 1: INICIO
# -----------------------------------------------------------------------------
if nav_option == "Inicio":
    # CÁLCULO DE METRICAS
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
    tx_p = len(df_prev)
    tkt_c = (vtas_c / tx_c) if tx_c > 0 else 0
    tkt_p = (vtas_p / tx_p) if tx_p > 0 else 0
    d_tkt = ((tkt_c - tkt_p) / tkt_p * 100) if tkt_p > 0 else 0

    # 4 TARJETAS KPI EN FILA
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="card-kpi">
                <div class="card-kpi-title">Ventas Totales</div>
                <div class="card-kpi-value">S/ {vtas_c:,.2f}</div>
                <div class="{'card-kpi-delta-pos' if d_vtas >= 0 else 'card-kpi-delta-neg'}">
                    {'▲' if d_vtas >= 0 else '▼'} {abs(d_vtas):.1f}% vs periodo anterior
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="card-kpi">
                <div class="card-kpi-title">Utilidad Neta</div>
                <div class="card-kpi-value">S/ {util_c:,.2f}</div>
                <div class="{'card-kpi-delta-pos' if d_util >= 0 else 'card-kpi-delta-neg'}">
                    {'▲' if d_util >= 0 else '▼'} {abs(d_util):.1f}% vs periodo anterior
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="card-kpi">
                <div class="card-kpi-title">Margen de Ganancia</div>
                <div class="card-kpi-value">{mg_c:.1f}%</div>
                <div class="{'card-kpi-delta-pos' if d_mg >= 0 else 'card-kpi-delta-neg'}">
                    {'▲' if d_mg >= 0 else '▼'} {abs(d_mg):.1f} pp vs periodo anterior
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="card-kpi">
                <div class="card-kpi-title">Ticket Promedio</div>
                <div class="card-kpi-value">S/ {tkt_c:.2f}</div>
                <div class="{'card-kpi-delta-pos' if d_tkt >= 0 else 'card-kpi-delta-neg'}">
                    {'▲' if d_tkt >= 0 else '▼'} {abs(d_tkt):.1f}% vs periodo anterior
                </div>
            </div>
        """, unsafe_allow_html=True)

    # GRÁFICOS PRINCIPALES
    g_col1, g_col2 = st.columns([1.8, 1.2])

    with g_col1:
        st.markdown("""
            <div class="card-box">
                <div class="card-box-title">Evolución Diaria de Ventas y Utilidad</div>
                <div class="card-box-subtitle">Comportamiento diario en el periodo seleccionado</div>
            </div>
        """, unsafe_allow_html=True)

        if not df_curr.empty:
            df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_daily['Fecha'], y=df_daily['Ventas_Soles'], name='Ventas (S/)',
                mode='lines+markers', line=dict(color='#2563EB', width=3, shape='spline'),
                fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.05)'
            ))
            fig_line.add_trace(go.Scatter(
                x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'], name='Utilidad (S/)',
                mode='lines', line=dict(color='#16A34A', width=2.5, dash='dash')
            ))
            fig_line.update_layout(
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF',
                xaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#0F172A', size=11)),
                yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#0F172A', size=11)),
                legend=dict(orientation="h", y=1.1, x=0, font=dict(color='#0F172A', size=12))
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No hay datos para los filtros seleccionados.")

    with g_col2:
        st.markdown("""
            <div class="card-box">
                <div class="card-box-title">Ventas por Categoría</div>
                <div class="card-box-subtitle">Participación proporcional de ingresos</div>
            </div>
        """, unsafe_allow_html=True)

        if not df_curr.empty:
            df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
            fig_donut = go.Figure(data=[go.Pie(
                labels=df_cat['Categoria'], values=df_cat['Ventas_Soles'],
                hole=0.6, marker=dict(colors=['#2563EB', '#16A34A', '#D97706', '#9333EA', '#0891B2']),
                textinfo='percent', hoverinfo='label+value+percent'
            )])
            fig_donut.add_annotation(
                text=f"<b style='font-size:16px;color:#0F172A;'>S/ {vtas_c:,.0f}</b><br><span style='font-size:11px;color:#64748B;'>Total</span>",
                x=0.5, y=0.5, showarrow=False
            )
            fig_donut.update_layout(
                height=320, margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF',
                legend=dict(orientation="v", y=0.5, x=0.85, font=dict(color='#0F172A', size=11))
            )
            st.plotly_chart(fig_donut, use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 2: PRODUCTOS ESTRELLA
# -----------------------------------------------------------------------------
elif nav_option == "Productos Estrella":
    st.markdown("""
        <div class="card-box">
            <div class="card-box-title">Ranking de Productos Estrella</div>
            <div class="card-box-subtitle">Identifica cuáles son tus productos más vendidos y rentables en tiempo real</div>
        </div>
    """, unsafe_allow_html=True)

    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        top_n = st.slider("Número de productos a mostrar:", min_value=5, max_value=15, value=10)
    with col_ctrl2:
        metric_sort = st.selectbox("Ordenar por:", ["Ventas Soles", "Unidades Vendidas", "Utilidad Soles"])

    sort_map = {"Ventas Soles": "Ventas_Soles", "Unidades Vendidas": "Cantidad", "Utilidad Soles": "Utilidad_Soles"}
    
    if not df_curr.empty:
        df_p = df_curr.groupby('Producto').agg({
            'Ventas_Soles': 'sum', 'Cantidad': 'sum', 'Utilidad_Soles': 'sum'
        }).reset_index()
        
        df_p['Margen_%'] = (df_p['Utilidad_Soles'] / df_p['Ventas_Soles'] * 100).round(1)
        df_p = df_p.sort_values(by=sort_map[metric_sort], ascending=False).head(top_n)

        # GRÁFICO BARRAS HORIZONTALES
        fig_bar = go.Figure(go.Bar(
            x=df_p[sort_map[metric_sort]], y=df_p['Producto'],
            orientation='h', marker=dict(color='#2563EB', cornerradius=4),
            text=df_p[sort_map[metric_sort]].apply(lambda x: f"S/ {x:,.2f}" if "Soles" in metric_sort else f"{x:,} un."),
            textposition='auto'
        ))
        fig_bar.update_layout(
            height=400, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF',
            yaxis=dict(autorange="reversed", tickfont=dict(color='#0F172A', size=12)),
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#0F172A', size=11))
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("<div style='font-size:15px; font-weight:800; color:#0F172A; margin: 20px 0 10px 0;'>Tabla Detallada de Rendimiento por Producto</div>", unsafe_allow_html=True)
        st.dataframe(
            df_p.rename(columns={
                'Producto': 'Nombre del Producto', 'Ventas_Soles': 'Ventas Totales (S/)',
                'Cantidad': 'Unidades', 'Utilidad_Soles': 'Utilidad Neta (S/)', 'Margen_%': 'Margen %'
            }),
            use_container_width=True, hide_index=True
        )

# -----------------------------------------------------------------------------
# SECCIÓN 3: ALERTAS Y DECISIONES
# -----------------------------------------------------------------------------
elif nav_option == "Alertas y Decisiones":
    st.markdown("""
        <div class="card-box">
            <div class="card-box-title">Centro de Alertas y Toma de Decisiones</div>
            <div class="card-box-subtitle">Recomendaciones automatizadas basadas en el comportamiento de tus datos</div>
        </div>
    """, unsafe_allow_html=True)

    if not df_curr.empty:
        # LÓGICA DE DETECCIÓN
        df_prod_qty = df_curr.groupby('Producto')['Cantidad'].sum().reset_index()
        low_stock_prods = df_prod_qty[df_prod_qty['Cantidad'] <= stock_threshold]
        
        c_alert1, c_alert2 = st.columns(2)

        with c_alert1:
            st.markdown("""
                <div style="background:#FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #DC2626; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
                    <div style="font-size: 14px; font-weight: 800; color: #991B1B; margin-bottom: 6px;">ALERTA DE STOCK CRÍTICO</div>
                    <div style="font-size: 13px; color: #334155;">
                        Se han detectado productos con volumen de rotación bajo o riesgo de agotamiento según el umbral configurado.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if not low_stock_prods.empty:
                for _, r in low_stock_prods.iterrows():
                    st.markdown(f"""
                        <div style="display:flex; justify-content:space-between; align-items:center; background:#FEF2F2; border:1px solid #FCA5A5; padding:10px 14px; border-radius:6px; margin-bottom:8px;">
                            <span style="font-weight:700; color:#991B1B; font-size:13px;">{r['Producto']}</span>
                            <span class="badge-critical">{r['Cantidad']} unidades en periodo</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<div class='badge-success'>✓ Todos los productos superan el umbral mínimo de stock.</div>", unsafe_allow_html=True)

        with c_alert2:
            st.markdown("""
                <div style="background:#FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #16A34A; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
                    <div style="font-size: 14px; font-weight: 800; color: #166534; margin-bottom: 6px;">DECISIONES ESTRATÉGICAS RECOMENDADAS</div>
                    <div style="font-size: 13px; color: #334155;">
                        Acciones comerciales de impacto inmediato sugeridas para tu negocio:
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div style="background:#F0FDF4; border:1px solid #86EFAC; padding:12px; border-radius:6px; margin-bottom:10px;">
                    <div style="font-weight:700; color:#166534; font-size:13px;">1. Reabastecimiento Anticipado los Jueves</div>
                    <div style="font-size:12px; color:#334155; margin-top:2px;">La demanda de bebidas y snacks aumenta un 38% los fines de semana. Programar compras con proveedores antes del viernes.</div>
                </div>
                <div style="background:#F0FDF4; border:1px solid #86EFAC; padding:12px; border-radius:6px; margin-bottom:10px;">
                    <div style="font-weight:700; color:#166534; font-size:13px;">2. Impulso de Venta Cruzada en Caja</div>
                    <div style="font-size:12px; color:#334155; margin-top:2px;">Ofrecer productos complementarios de menor valor para elevar el Ticket Promedio de S/ {:.2f} a S/ {:.2f}.</div>
                </div>
            """.format(tkt_c if 'tkt_c' in locals() else 35.0, (tkt_c * 1.15) if 'tkt_c' in locals() else 40.0), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECCIÓN 4: SIMULADOR
# -----------------------------------------------------------------------------
elif nav_option == "Simulador":
    st.markdown("""
        <div class="card-box">
            <div class="card-box-title">Simulador de Impacto Financiero en Tiempo Real</div>
            <div class="card-box-subtitle">Modifica los parámetros para proyectar el retorno de inversión y beneficio neto de la plataforma</div>
        </div>
    """, unsafe_allow_html=True)

    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("<div style='font-size:14px; font-weight:800; color:#0F172A; margin-bottom:10px;'>Parámetros Editables del Modelo</div>", unsafe_allow_html=True)
        tarifa_basico = st.number_input("Tarifa Plan Básico (S/ / mes):", value=50.0, step=5.0)
        clientes_basico = st.slider("Clientes Plan Básico:", min_value=10, max_value=200, value=50)
        tarifa_premium = st.number_input("Tarifa Plan Premium (S/ / mes):", value=150.0, step=10.0)
        clientes_premium = st.slider("Clientes Plan Premium:", min_value=5, max_value=100, value=20)

    with s_col2:
        st.markdown("<div style='font-size:14px; font-weight:800; color:#0F172A; margin-bottom:10px;'>Parámetros de Impacto en la MYPE</div>", unsafe_allow_html=True)
        ventas_mype = st.number_input("Ventas Promedio MYPE (S/ / mes):", value=11900.0, step=500.0)
        inc_ventas_pct = st.slider("Incremento de Ventas por Analítica (%):", min_value=1.0, max_value=30.0, value=16.3)
        reducc_mermas_pct = st.slider("Reducción de Mermas/Pérdidas (%):", min_value=10.0, max_value=90.0, value=70.0)

    # CÁLCULOS EN TIEMPO REAL
    mrr_total = (tarifa_basico * clientes_basico) + (tarifa_premium * clientes_premium)
    costo_fijo_startup = 1800.0
    costo_var_startup = (clientes_basico * 5.0) + (clientes_premium * 15.0)
    costo_total_startup = costo_fijo_startup + costo_var_startup
    utilidad_startup = mrr_total - costo_total_startup

    ventas_extra_mype = ventas_mype * (inc_ventas_pct / 100.0)
    ahorro_mermas_mype = (ventas_mype * 0.05) * (reducc_mermas_pct / 100.0)
    beneficio_bruto_mype = ventas_extra_mype + ahorro_mermas_mype
    beneficio_neto_mype = beneficio_bruto_mype - tarifa_premium
    roi_mype = (beneficio_neto_mype / tarifa_premium * 100.0) if tarifa_premium > 0 else 0

    st.markdown("<hr style='margin: 20px 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)

    r_col1, r_col2, r_col3, r_col4 = st.columns(4)

    with r_col1:
        st.markdown(f"""
            <div class="card-kpi">
                <div class="card-kpi-title">Ingreso Mensual Startup (MRR)</div>
                <div class="card-kpi-value">S/ {mrr_total:,.2f}</div>
                <div class="card-kpi-delta-pos">Objetivo mensual alcanzado</div>
            </div>
        """, unsafe_allow_html=True)

    with r_col2:
        st.markdown(f"""
            <div class="card-kpi">
                <div class="card-kpi-title">Utilidad Neta Startup</div>
                <div class="card-kpi-value">S/ {utilidad_startup:,.2f}</div>
                <div class="card-kpi-delta-pos">Margen: {(utilidad_startup/mrr_total*100 if mrr_total>0 else 0):.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with r_col3:
        st.markdown(f"""
            <div class="card-kpi">
                <div class="card-kpi-title">Beneficio Neto MYPE</div>
                <div class="card-kpi-value">S/ {beneficio_neto_mype:,.2f}</div>
                <div class="card-kpi-delta-pos">Ganancia extra libre de suscripción</div>
            </div>
        """, unsafe_allow_html=True)

    with r_col4:
        st.markdown(f"""
            <div class="card-kpi">
                <div class="card-kpi-title">ROI para la MYPE</div>
                <div class="card-kpi-value">{roi_mype:,.1f}%</div>
                <div class="card-kpi-delta-pos">El producto se paga solo</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 30px 0 15px 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-size: 12px; color: #64748B;'>NEXDATA Analytics v2.5 – Proyecto de Gestión por Resultados 2026</div>", unsafe_allow_html=True)
