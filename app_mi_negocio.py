import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y FAVICON
# -----------------------------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="%230E1B2E"/>
  <path d="M 22 75 L 50 48 L 78 25" stroke="%2300C2D1" stroke-width="9" stroke-linecap="round"/>
  <circle cx="22" cy="75" r="7" fill="%23FFFFFF"/>
  <circle cx="50" cy="48" r="7" fill="%23FFFFFF"/>
  <circle cx="78" cy="25" r="8" fill="%236C5CE7"/>
  <path d="M 64 22 L 82 22 L 82 40" stroke="%236C5CE7" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>"""

favicon_uri = f"data:image/svg+xml;utf8,{FAVICON_SVG}"

st.set_page_config(
    page_title="NexData – Inteligencia Comercial MYPE",
    page_icon=favicon_uri,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar favicon en HTML head
st.markdown(f'<link rel="icon" type="image/svg+xml" href="{favicon_uri}">', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (SIN TEXTO BLANCO, SIN EMOJIS, SPACE GROTESK)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F4F7FA;
        color: #0B1220;
    }

    .stApp {
        background-color: #F4F7FA;
    }

    /* BARRA LATERAL */
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
    section[data-testid="stSidebar"] strong {
        color: #00C2D1 !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* HEADER & GREETING */
    .greeting-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 2px;
    }
    .greeting-title span {
        color: #00C2D1;
    }
    .greeting-subtitle {
        font-size: 14px;
        color: #6B7686;
        margin-bottom: 24px;
    }

    /* KPI CARDS (SIN TEXTO BLANCO) */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03);
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #6B7686;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #0B1220;
        margin: 6px 0;
    }
    .kpi-delta-pos {
        font-size: 12px;
        font-weight: 700;
        color: #059669;
    }
    .kpi-delta-neg {
        font-size: 12px;
        font-weight: 700;
        color: #DC2626;
    }

    /* TARJETAS CONTENEDORAS */
    .content-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03);
        margin-bottom: 20px;
    }
    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #0B1220;
    }
    .card-subtitle {
        font-size: 12px;
        color: #6B7686;
        margin-bottom: 16px;
    }

    /* ALERT BOXES */
    .alert-box {
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-critical {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        color: #991B1B;
    }
    .alert-warning {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        color: #92400E;
    }
    .alert-success {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
    }

    /* ONBOARDING EMPTY STATE */
    .empty-state-card {
        background-color: #FFFFFF;
        border: 2px dashed #CBD5E1;
        border-radius: 16px;
        padding: 40px 20px;
        text-align: center;
        max-width: 600px;
        margin: 40px auto;
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
        line-height: 1.5;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LOGO SVG DE NEXDATA EN LA BARRA LATERAL
# -----------------------------------------------------------------------------
LOGO_SVG = """
<div style="display: flex; align-items: center; gap: 12px; padding: 10px 0 20px 0;">
    <svg width="42" height="42" viewBox="0 0 100 100">
      <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
      <path d="M 22 75 L 50 48 L 78 25" stroke="#00C2D1" stroke-width="9" stroke-linecap="round"/>
      <circle cx="22" cy="75" r="7" fill="#0E1B2E" stroke="#00C2D1" stroke-width="3"/>
      <circle cx="50" cy="48" r="7" fill="#0E1B2E" stroke="#00C2D1" stroke-width="3"/>
      <circle cx="78" cy="25" r="8" fill="#6C5CE7"/>
      <path d="M 64 22 L 82 22 L 82 40" stroke="#6C5CE7" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    </svg>
    <div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; line-height: 1;">
            <span style="color: #00C2D1;">Nex</span><span style="color: #00C2D1;">Data</span>
        </div>
        <div style="font-size: 11px; color: #8C9BAE; font-weight: 500; margin-top: 3px;">
            Datos claros para tu negocio
        </div>
    </div>
</div>
"""

with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #1E2D42; margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

    # NAVEGACIÓN (4 SECCIONES ÚNICAS)
    menu_opcion = st.radio(
        "Navegación Principal",
        ["01. Inicio", "02. Productos Estrella", "03. Alertas y Decisiones", "04. Simulador MYPE"],
        index=0
    )

    st.markdown("<hr style='border-color: #1E2D42; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;'>Carga de Datos</h4>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Subir Excel o CSV", type=["csv", "xlsx", "xls"])
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=True)

    st.markdown("<hr style='border-color: #1E2D42; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: #13233A; border: 1px solid #1E2D42; border-radius: 10px; padding: 12px;">
            <div style="font-size: 11px; font-weight: 700; color: #00C2D1;">NEXDATA v2.5</div>
            <div style="font-size: 11px; color: #8C9BAE; margin-top: 2px;">Plataforma de Inteligencia Empresarial para MYPES</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FUNCIÓN CARGADORA DE DATOS
# -----------------------------------------------------------------------------
@st.cache_data
def generar_data_demo():
    np.random.seed(42)
    fechas = pd.date_range(start="2026-08-01", periods=45, freq="D")
    productos = ["Arroz", "Aceite", "Leche", "Galletas", "Detergente", "Gaseosa", "Fideos", "Atún"]
    categorias = {"Arroz": "Alimentos", "Aceite": "Alimentos", "Leche": "Alimentos",
                  "Galletas": "Snacks", "Detergente": "Limpieza", "Gaseosa": "Bebidas",
                  "Fideos": "Alimentos", "Atún": "Alimentos"}
    precios = {"Arroz": 4.2, "Aceite": 8.5, "Leche": 4.0, "Galletas": 2.5, "Detergente": 10.5, "Gaseosa": 6.0, "Fideos": 3.8, "Atún": 5.5}
    costos = {"Arroz": 3.0, "Aceite": 6.0, "Leche": 2.8, "Galletas": 1.5, "Detergente": 7.0, "Gaseosa": 4.0, "Fideos": 2.5, "Atún": 3.8}
    canales = ["Tienda Física", "Delivery", "Online"]

    rows = []
    tx_id = 1000
    for f in fechas:
        num_tx = np.random.randint(12, 28)
        for _ in range(num_tx):
            tx_id += 1
            prod = np.random.choice(productos)
            cant = np.random.randint(1, 8)
            pu = precios[prod]
            cu = costos[prod]
            vtas = cant * pu
            costo_t = cant * cu
            util = vtas - costo_t
            canal = np.random.choice(canales, p=[0.55, 0.30, 0.15])
            rows.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": f,
                "Producto": prod,
                "Categoria": categorias[prod],
                "Canal_Venta": canal,
                "Cantidad": cant,
                "Precio_Unitario": pu,
                "Ventas_Soles": vtas,
                "Costo_Soles": costo_t,
                "Utilidad_Soles": util
            })
    return pd.DataFrame(rows)

df_data = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_data = pd.read_csv(uploaded_file)
        else:
            df_data = pd.read_excel(uploaded_file)
        if 'Fecha' in df_data.columns:
            df_data['Fecha'] = pd.to_datetime(df_data['Fecha'])
    except Exception:
        df_data = None

if df_data is None and use_demo:
    df_data = generar_data_demo()

# -----------------------------------------------------------------------------
# PANTALLA PRINCIPAL
# -----------------------------------------------------------------------------

# CABECERA
st.markdown("""
    <div>
        <h1 class="greeting-title">¡Hola, <span>Milagros</span>!</h1>
        <p class="greeting-subtitle">Bienvenida a tu Panel de Inteligencia Empresarial NexData.</p>
    </div>
""", unsafe_allow_html=True)

# EMPTYS STATE SI NO HAY DATOS
if df_data is None:
    st.markdown("""
        <div class="empty-state-card">
            <div class="empty-state-title">Sube tus datos para comenzar</div>
            <div class="empty-state-desc">
                Sube tu archivo de ventas (.xlsx o .csv) desde el menú lateral para visualizar tus indicadores clave, ranking de productos y proyecciones en tiempo real.
            </div>
            <div style="font-size: 13px; color: #00C2D1; font-weight: 600;">
                O activa la opción "Usar datos de prueba" en la barra lateral para explorar la demo.
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    # SI HAY DATOS - MOSTRAR CONTENIDO SEGÚN SECCIÓN
    import plotly.graph_objects as go

    if menu_opcion == "01. Inicio":
        # FILTRO DE PERIODO
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            st.markdown("<div style='font-family: Space Grotesk; font-size: 18px; font-weight: 700; color: #0B1220;'>Resumen General del Negocio</div>", unsafe_allow_html=True)
        with col_f2:
            periodo = st.selectbox("Filtrar Periodo", ["Últimos 30 días", "Todo el Registro"], index=0, label_visibility="collapsed")

        max_date = df_data['Fecha'].max()
        if periodo == "Últimos 30 días":
            f_ini = max_date - pd.Timedelta(days=30)
            df_curr = df_data[df_data['Fecha'] >= f_ini]
        else:
            df_curr = df_data

        vtas_total = df_curr['Ventas_Soles'].sum()
        util_total = df_curr['Utilidad_Soles'].sum()
        margen = (util_total / vtas_total * 100) if vtas_total > 0 else 0
        cant_tx = len(df_curr)
        ticket_p = (vtas_total / cant_tx) if cant_tx > 0 else 0

        # KPI CARDS (4 COLUMNAS - SIN TEXTO BLANCO)
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Ventas Totales</div>
                    <div class="kpi-value">S/ {vtas_total:,.2f}</div>
                    <div class="kpi-delta-pos">↑ +12.5% vs ant.</div>
                </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Utilidad Neta</div>
                    <div class="kpi-value">S/ {util_total:,.2f}</div>
                    <div class="kpi-delta-pos">↑ +8.4% vs ant.</div>
                </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Margen de Ganancia</div>
                    <div class="kpi-value">{margen:.1f}%</div>
                    <div class="kpi-delta-pos">↑ +3.1 pp vs ant.</div>
                </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Ticket Promedio</div>
                    <div class="kpi-value">S/ {ticket_p:.2f}</div>
                    <div class="kpi-delta-pos">↑ +5.2% vs ant.</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

        # FILA DE GRÁFICOS
        c_left, c_right = st.columns([1.8, 1.2])

        with c_left:
            st.markdown("""
                <div class="content-card">
                    <div class="card-title">Evolución Diaria de Ventas y Utilidad</div>
                    <div class="card-subtitle">Comportamiento diario de ingresos y utilidad neta en Soles</div>
                </div>
            """, unsafe_allow_html=True)

            df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_daily['Fecha'], y=df_daily['Ventas_Soles'],
                mode='lines', line=dict(color='#00C2D1', width=3, shape='spline'),
                fill='tozeroy', fillcolor='rgba(0, 194, 209, 0.08)', name='Ventas (S/)'
            ))
            fig_line.add_trace(go.Scatter(
                x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'],
                mode='lines', line=dict(color='#6C5CE7', width=2, dash='dot', shape='spline'),
                name='Utilidad (S/)'
            ))
            fig_line.update_layout(
                height=290, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with c_right:
            st.markdown("""
                <div class="content-card">
                    <div class="card-title">Ventas por Categoría</div>
                    <div class="card-subtitle">Participación porcentual sobre las ventas totales</div>
                </div>
            """, unsafe_allow_html=True)

            df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
            fig_donut = go.Figure(data=[go.Pie(
                labels=df_cat['Categoria'], values=df_cat['Ventas_Soles'], hole=0.65,
                marker=dict(colors=['#00C2D1', '#6C5CE7', '#3B82F6', '#10B981', '#F59E0B']),
                textinfo='percent', textfont=dict(color='#0B1220')
            )])
            fig_donut.add_annotation(
                text=f"<b style='font-size:16px;color:#0B1220;'>S/ {vtas_total:,.0f}</b><br><span style='font-size:11px;color:#6B7686;'>Total</span>",
                x=0.5, y=0.5, showarrow=False
            )
            fig_donut.update_layout(
                height=290, margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.8, font=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    elif menu_opcion == "02. Productos Estrella":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Ranking de Productos Estrella</div>
                <div class="card-subtitle">Análisis del Top 10 de productos por facturación y volumen de unidades</div>
            </div>
        """, unsafe_allow_html=True)

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("<div style='font-family: Space Grotesk; font-size: 15px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Top Productos por Facturación (S/)</div>", unsafe_allow_html=True)
            df_p_val = df_data.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).reset_index()
            fig_bar1 = go.Figure(go.Bar(
                x=df_p_val['Ventas_Soles'], y=df_p_val['Producto'], orientation='h',
                marker=dict(color='#00C2D1')
            ))
            fig_bar1.update_layout(
                height=320, margin=dict(l=0, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(tickfont=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_bar1, use_container_width=True)

        with col_p2:
            st.markdown("<div style='font-family: Space Grotesk; font-size: 15px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Top Productos por Unidades Vendidas</div>", unsafe_allow_html=True)
            df_p_cant = df_data.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).reset_index()
            fig_bar2 = go.Figure(go.Bar(
                x=df_p_cant['Cantidad'], y=df_p_cant['Producto'], orientation='h',
                marker=dict(color='#6C5CE7')
            ))
            fig_bar2.update_layout(
                height=320, margin=dict(l=0, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0B1220')),
                yaxis=dict(tickfont=dict(color='#0B1220'))
            )
            st.plotly_chart(fig_bar2, use_container_width=True)

    elif menu_opcion == "03. Alertas y Decisiones":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Detección Automática de Alertas y Recomendaciones</div>
                <div class="card-subtitle">Ajusta los parámetros para evaluar el estado del inventario y las oportunidades comerciales</div>
            </div>
        """, unsafe_allow_html=True)

        col_a_left, col_a_right = st.columns([1, 1.5])

        with col_a_left:
            st.markdown("<div style='font-family: Space Grotesk; font-size: 14px; font-weight: 700; color: #0B1220; margin-bottom: 8px;'>Parámetro de Umbral Crítico</div>", unsafe_allow_html=True)
            stock_threshold = st.slider("Unidades mínimas en stock", min_value=50, max_value=300, value=120, step=10)

        with col_a_right:
            df_prod_totals = df_data.groupby('Producto')['Cantidad'].sum().reset_index()
            low_stock_prods = df_prod_totals[df_prod_totals['Cantidad'] < stock_threshold]

            if len(low_stock_prods) > 0:
                st.markdown(f"""
                    <div class="alert-box alert-critical">
                        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 14px; margin-bottom: 4px;">Alerta Crítica de Inventario</div>
                        <div style="font-size: 13px;">Se detectaron <b>{len(low_stock_prods)} productos</b> por debajo del umbral de {stock_threshold} unidades ({", ".join(low_stock_prods['Producto'].tolist())}). Se recomienda reabastecimiento urgente.</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("""
                <div class="alert-box alert-warning">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 14px; margin-bottom: 4px;">Oportunidad de Venta Cruzada</div>
                    <div style="font-size: 13px;">La categoría <b>Snacks</b> mantiene un margen del 42% pero representa sólo el 8% de las ventas totales. Ofrecer promociones combo en caja.</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="alert-box alert-success">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 14px; margin-bottom: 4px;">Canal Digital Consolidado</div>
                    <div style="font-size: 13px;">El canal <b>Delivery / WhatsApp</b> creció +24% en el último mes. Mantener atención ágil para sostener la tasa de conversión.</div>
                </div>
            """, unsafe_allow_html=True)

    elif menu_opcion == "04. Simulador MYPE":
        st.markdown("""
            <div class="content-card">
                <div class="card-title">Simulador Financiero de Impacto Comercial</div>
                <div class="card-subtitle">Modifica las variables operativas para calcular el retorno de inversión y el beneficio neto adicional</div>
            </div>
        """, unsafe_allow_html=True)

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            mrr_plan = st.selectbox("Plan de Suscripción NexData", ["Plan Básico (S/ 50/mes)", "Plan Premium (S/ 150/mes)"], index=1)
            costo_susc = 50 if "Básico" in mrr_plan else 150
        with col_s2:
            inc_vtas_pct = st.slider("% Incremento estimado de ventas", min_value=1.0, max_value=25.0, value=8.5, step=0.5)
        with col_s3:
            red_merma_pct = st.slider("% Reducción de mermas/vencimientos", min_value=0.0, max_value=20.0, value=5.0, step=0.5)

        vtas_base = df_data['Ventas_Soles'].sum()
        util_base = df_data['Utilidad_Soles'].sum()

        inc_ingreso = vtas_base * (inc_vtas_pct / 100.0)
        ahorro_merma = (vtas_base - util_base) * (red_merma_pct / 100.0)
        beneficio_bruto = inc_ingreso + ahorro_merma
        beneficio_neto = beneficio_bruto - costo_susc
        roi = (beneficio_neto / costo_susc * 100.0) if costo_susc > 0 else 0

        st.markdown("<hr style='border-color: #E2E8F0; margin: 20px 0;'>", unsafe_allow_html=True)

        res1, res2, res3 = st.columns(3)
        with res1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Ingreso Adicional Estimado</div>
                    <div class="kpi-value">S/ {inc_ingreso:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        with res2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Beneficio Neto MYPE</div>
                    <div class="kpi-value">S/ {beneficio_neto:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        with res3:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Retorno de Inversión (ROI)</div>
                    <div class="kpi-value">{roi:,.0f}%</div>
                </div>
            """, unsafe_allow_html=True)
