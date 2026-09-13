import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as gg

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y FAVICON SVG
# ---------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
  <path d="M22 78 L52 48 L72 28" stroke="#00C2D1" stroke-width="10" stroke-linecap="round"/>
  <circle cx="22" cy="78" r="7" fill="#FFFFFF"/>
  <circle cx="52" cy="48" r="7" fill="#FFFFFF"/>
  <circle cx="72" cy="28" r="9" fill="#6C5CE7"/>
  <path d="M62 18 L84 18 L84 40 M84 18 L70 32" stroke="#6C5CE7" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>"""

st.set_page_config(
    page_title="NexData – Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar CSS global para la tipografía, alto contraste (CERO texto blanco sobre fondo claro) y orden
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F4F7FA !important;
        color: #0B1220 !important;
    }
    
    /* Header principal */
    .greeting-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 2px;
    }
    
    .greeting-subtitle {
        font-size: 15px;
        color: #6B7686;
        margin-bottom: 20px;
    }
    
    /* Tarjetas KPI Premium */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px 18px;
        box-shadow: 0 4px 16px rgba(14, 27, 46, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(14, 27, 46, 0.08);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }
    .kpi-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
    }
    .kpi-label {
        font-size: 13px;
        font-weight: 600;
        color: #6B7686;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 6px;
    }
    .kpi-delta-pos {
        font-size: 13px;
        font-weight: 700;
        color: #059669;
        background-color: #ECFDF5;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }
    .kpi-delta-neg {
        font-size: 13px;
        font-weight: 700;
        color: #DC2626;
        background-color: #FEF2F2;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }
    
    /* Contenedores de gráficos y secciones */
    .chart-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 4px 16px rgba(14, 27, 46, 0.04);
        margin-bottom: 20px;
    }
    .chart-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 4px;
    }
    .chart-subtitle {
        font-size: 13px;
        color: #6B7686;
        margin-bottom: 16px;
    }
    
    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
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
    
    /* Estilo de radio buttons en la barra lateral */
    div[data-testid="stRadio"] > label {
        color: #00C2D1 !important;
        font-weight: 700;
    }
    div[role="radiogroup"] label {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    div[role="radiogroup"] label:hover {
        background-color: rgba(0, 194, 209, 0.15);
    }
    div[role="radiogroup"] label[data-checked="true"] {
        background-color: #00C2D1 !important;
    }
    div[role="radiogroup"] label[data-checked="true"] span {
        color: #0E1B2E !important;
        font-weight: 800 !important;
    }
    
    /* Alertas */
    .alert-card-warning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }
    .alert-title-warning {
        font-weight: 700;
        color: #92400E;
        font-size: 14px;
    }
    .alert-desc-warning {
        font-size: 13px;
        color: #78350F;
    }
    
    .alert-card-success {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }
    .alert-title-success {
        font-weight: 700;
        color: #065F46;
        font-size: 14px;
    }
    .alert-desc-success {
        font-size: 13px;
        color: #047857;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL: LOGO VECTORIAL & FILTROS DE NAVEGACIÓN
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
        <svg width="44" height="44" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
            <path d="M22 78 L52 48 L72 28" stroke="#00C2D1" stroke-width="10" stroke-linecap="round"/>
            <circle cx="22" cy="78" r="7" fill="#FFFFFF"/>
            <circle cx="52" cy="48" r="7" fill="#FFFFFF"/>
            <circle cx="72" cy="28" r="9" fill="#6C5CE7"/>
            <path d="M62 18 L84 18 L84 40 M84 18 L70 32" stroke="#6C5CE7" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; line-height: 1;">
                <span style="color: #8C9BAE;">Nex</span><span style="color: #00C2D1;">Data</span>
            </div>
            <div style="font-size: 11px; color: #8C9BAE; margin-top: 3px;">Datos claros para tu negocio</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;'>Navegación</h3>", unsafe_allow_html=True)
    
    opciones_nav = [
        "01. Inicio",
        "02. Ventas",
        "03. Productos",
        "04. Rentabilidad",
        "05. Análisis",
        "06. Simulador"
    ]
    
    nav_sel = st.radio("Seleccionar Pantalla:", opciones_nav, label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;'>Carga de Datos</h3>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Subir ventas (Excel/CSV):", type=["csv", "xlsx"])
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=True)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;'>Filtros Globales</h3>", unsafe_allow_html=True)
    
    periodo_opt = st.selectbox("Periodo de Análisis:", ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Registro"])
    stock_threshold = st.slider("Umbral Stock Crítico (Unid.):", min_value=5, max_value=50, value=20)

# ---------------------------------------------------------
# CARGA Y PREPARACIÓN DE DATOS REPRODUCIBLE
# ---------------------------------------------------------
@st.cache_data
def get_default_data():
    dates = pd.date_range(end=datetime.date(2026, 4, 30), periods=90, freq='D')
    np.random.seed(42)
    
    cats = ['Alimentos', 'Bebidas', 'Limpieza', 'Higiene', 'Otros']
    cat_weights = [0.325, 0.248, 0.182, 0.126, 0.119]
    
    prods = {
        'Alimentos': [('Arroz 1kg', 4.5, 3.2), ('Aceite 1L', 8.5, 6.0), ('Fideos 500g', 2.8, 1.9), ('Galletas Pack', 3.5, 2.1)],
        'Bebidas': [('Gaseosa 1.5L', 6.0, 4.0), ('Agua Mineral 1L', 2.5, 1.2), ('Jugo Natural', 4.0, 2.5)],
        'Limpieza': [('Detergente 1kg', 9.0, 6.2), ('Lejía 1L', 3.2, 1.8), ('Jabón Líquido', 5.5, 3.5)],
        'Higiene': [('Shampoo 400ml', 12.0, 8.0), ('Crema Dental', 4.5, 2.8)],
        'Otros': [('Pilas AA', 5.0, 3.0), ('Bolsas Reutilizables', 2.0, 0.8)]
    }
    
    canales = ['Tienda física', 'Delivery', 'Online', 'Otros']
    canal_w = [0.45, 0.30, 0.15, 0.10]
    
    rows = []
    tx_id = 1000
    for d in dates:
        n_tx = np.random.randint(10, 25)
        for _ in range(n_tx):
            tx_id += 1
            cat = np.random.choice(cats, p=cat_weights)
            p_name, p_price, p_cost = prods[cat][np.random.randint(0, len(prods[cat]))]
            qty = np.random.randint(1, 5)
            canal = np.random.choice(canales, p=canal_w)
            
            vtas = round(qty * p_price, 2)
            csto = round(qty * p_cost, 2)
            util = round(vtas - csto, 2)
            
            rows.append({
                'ID_Transaccion': f'TX-{tx_id}',
                'Fecha': d,
                'Dia_Semana': d.strftime('%A'),
                'Categoria': cat,
                'Producto': p_name,
                'Canal_Venta': canal,
                'Cantidad': qty,
                'Precio_Unitario': p_price,
                'Ventas_Soles': vtas,
                'Costo_Soles': csto,
                'Utilidad_Soles': util
            })
            
    df = pd.DataFrame(rows)
    return df

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
        df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
    except Exception as e:
        st.error(f"Error al leer el archivo subido: {e}")
        df_raw = get_default_data()
elif use_demo:
    df_raw = get_default_data()
else:
    df_raw = None

# ---------------------------------------------------------
# PANTALLA DE BIENVENIDA (EMPTY STATE) O PANEL COMPLETO
# ---------------------------------------------------------
if df_raw is None:
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background-color: #FFFFFF; border-radius: 16px; border: 1px solid #E2E8F0; margin-top: 40px;">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#00C2D1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <h2 style="font-family: 'Space Grotesk', sans-serif; color: #0B1220; margin-top: 16px; font-size: 26px;">Sube tus datos para comenzar</h2>
        <p style="color: #6B7686; max-width: 480px; margin: 8px auto 24px auto; font-size: 15px;">
            Carga tu archivo de ventas en formato Excel o CSV desde el menú lateral para acceder al análisis interactivo en tiempo real de tu MYPE.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Filtrar según el periodo seleccionado
    max_d = df_raw['Fecha'].max()
    if periodo_opt == "Últimos 30 días":
        f_ini = max_d - pd.Timedelta(days=30)
    elif periodo_opt == "Este Mes":
        f_ini = max_d.replace(day=1)
    elif periodo_opt == "Mes Anterior":
        f_ini = (max_d.replace(day=1) - pd.Timedelta(days=1)).replace(day=1)
    else:
        f_ini = df_raw['Fecha'].min()
        
    df_curr = df_raw[df_raw['Fecha'] >= f_ini].copy()
    
    # Encabezado con saludo
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px;">
        <div>
            <div class="greeting-title">¡Hola, Milagros!</div>
            <div class="greeting-subtitle">Aquí tienes un resumen interactivo del rendimiento de tu negocio.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # FUNCIÓN AUXILIAR PARA ESTILIZAR GRÁFICOS PLOTLY DE ALTO CONTRASTE
    # ---------------------------------------------------------
    def apply_plotly_theme(fig, height=380):
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=height,
            margin=dict(l=30, r=30, t=40, b=30),
            font=dict(family='Plus Jakarta Sans', color='#0B1220', size=12),
            title_font=dict(family='Space Grotesk', color='#0B1220', size=16),
            legend=dict(font=dict(color='#0B1220', size=11)),
            hoverlabel=dict(bgcolor='#FFFFFF', font_color='#0B1220', font_family='Plus Jakarta Sans')
        )
        fig.update_xaxes(
            showgrid=True, gridcolor='#E2E8F0', gridwidth=1,
            tickfont=dict(color='#475569', size=11), title_font=dict(color='#0B1220', size=12)
        )
        fig.update_yaxes(
            showgrid=True, gridcolor='#E2E8F0', gridwidth=1,
            tickfont=dict(color='#475569', size=11), title_font=dict(color='#0B1220', size=12)
        )
        return fig

    # ---------------------------------------------------------
    # NAVEGACIÓN ENTRE PESTAÑAS
    # ---------------------------------------------------------
    
    # =========================================================
    # PESTAÑA 01. INICIO (Réplica exacta de la imagen APP)
    # =========================================================
    if nav_sel.startswith("01"):
        vtas_tot = df_curr['Ventas_Soles'].sum()
        prods_tot = df_curr['Cantidad'].sum()
        clients_tot = df_curr['ID_Transaccion'].nunique()
        profit_mg = (df_curr['Utilidad_Soles'].sum() / vtas_tot * 100) if vtas_tot > 0 else 0
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon" style="background-color: #E0F2FE;">🛒</div>
                    <div class="kpi-label">Ventas Totales</div>
                </div>
                <div class="kpi-value">S/ {vtas_tot:,.0f}</div>
                <div class="kpi-delta-pos">▲ +12.5% vs. mes anterior</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon" style="background-color: #F3E8FF;">📦</div>
                    <div class="kpi-label">Productos Vendidos</div>
                </div>
                <div class="kpi-value">{prods_tot:,}</div>
                <div class="kpi-delta-pos">▲ +8.3% vs. mes anterior</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon" style="background-color: #DCFCE7;">👤</div>
                    <div class="kpi-label">Clientes Atendidos</div>
                </div>
                <div class="kpi-value">{clients_tot:,}</div>
                <div class="kpi-delta-pos">▲ +15.7% vs. mes anterior</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-icon" style="background-color: #FEF3C7;">💰</div>
                    <div class="kpi-label">Rentabilidad</div>
                </div>
                <div class="kpi-value">{profit_mg:.1f}%</div>
                <div class="kpi-delta-pos">▲ +4.2% vs. mes anterior</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns([1.6, 1])
        
        with col_g1:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Evolución de Ventas</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-subtitle">Ventas diarias en los últimos 30 días</div>', unsafe_allow_html=True)
            
            df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)['Ventas_Soles'].sum().reset_index()
            fig_daily = gg.Figure()
            fig_daily.add_trace(gg.Scatter(
                x=df_daily['Fecha'], y=df_daily['Ventas_Soles'],
                mode='lines+markers',
                line=dict(color='#00C2D1', width=3, shape='spline'),
                marker=dict(size=6, color='#6C5CE7'),
                fill='tozeroy', fillcolor='rgba(0, 194, 209, 0.08)',
                name='Ventas (S/)'
            ))
            apply_plotly_theme(fig_daily, height=330)
            st.plotly_chart(fig_daily, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_g2:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Ventas por Categoría</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-subtitle">Distribución de ingresos por categoría</div>', unsafe_allow_html=True)
            
            df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
            fig_cat = gg.Figure(data=[gg.Pie(
                labels=df_cat['Categoria'], values=df_cat['Ventas_Soles'],
                hole=0.62,
                marker=dict(colors=['#00C2D1', '#6C5CE7', '#10B981', '#F59E0B', '#3B82F6']),
                textinfo='percent',
                textfont=dict(color='#0B1220', size=12)
            )])
            fig_cat.add_annotation(
                text=f"<b>S/ {vtas_tot:,.0f}</b><br><span style='font-size:11px;color:#6B7686;'>Total Ventas</span>",
                x=0.5, y=0.5, showarrow=False, font=dict(size=14, color='#0B1220', family='Space Grotesk')
            )
            apply_plotly_theme(fig_cat, height=330)
            st.plotly_chart(fig_cat, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        col_b1, col_b2, col_b3 = st.columns([1, 1, 1.2])
        
        with col_b1:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Productos Más Vendidos</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-subtitle">Top 5 por volumen de ventas</div>', unsafe_allow_html=True)
            
            df_top_p = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(5).reset_index()
            fig_top_p = gg.Figure(gg.Bar(
                x=df_top_p['Cantidad'], y=df_top_p['Producto'],
                orientation='h',
                marker=dict(color='#00C2D1', cornerradius=4),
                text=df_top_p['Cantidad'].apply(lambda x: f"{x} un."),
                textposition='outside',
                textfont=dict(color='#0B1220', size=11)
            ))
            apply_plotly_theme(fig_top_p, height=280)
            st.plotly_chart(fig_top_p, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_b2:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Canales de Venta</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-subtitle">Participación por canal comercial</div>', unsafe_allow_html=True)
            
            df_canal = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
            fig_canal = gg.Figure(gg.Pie(
                labels=df_canal['Canal_Venta'], values=df_canal['Ventas_Soles'],
                marker=dict(colors=['#00C2D1', '#10B981', '#6C5CE7', '#F59E0B']),
                textinfo='percent+label',
                textfont=dict(color='#0B1220', size=11)
            ))
            apply_plotly_theme(fig_canal, height=280)
            st.plotly_chart(fig_canal, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_b3:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Alertas y Recomendaciones</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-subtitle">Acciones clave detectadas en tu negocio</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="alert-card-warning">
                <div class="alert-title-warning">⚠️ Producto con baja rotación</div>
                <div class="alert-desc-warning">El producto 'Galletas Pack' ha disminuido su venta en un 25% en comparación con el periodo previo.</div>
            </div>
            <div class="alert-card-success">
                <div class="alert-title-success">✅ Oportunidad de crecimiento</div>
                <div class="alert-desc-success">La categoría 'Bebidas' muestra una tendencia al alza los fines de semana. Considera aumentar stock.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # PESTAÑA 02. VENTAS
    # =========================================================
    elif nav_sel.startswith("02"):
        st.markdown("<h2 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Análisis Detallado de Ventas</h2>", unsafe_allow_html=True)
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Ventas por Día de la Semana</div>', unsafe_allow_html=True)
            df_day = df_curr.groupby('Dia_Semana')['Ventas_Soles'].sum().reset_index()
            order_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df_day['Dia_Semana'] = pd.Categorical(df_day['Dia_Semana'], categories=order_days, ordered=True)
            df_day = df_day.sort_values('Dia_Semana')
            
            fig_day = gg.Figure(gg.Bar(
                x=['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                y=df_day['Ventas_Soles'],
                marker=dict(color='#00C2D1', cornerradius=4),
                text=df_day['Ventas_Soles'].apply(lambda x: f"S/ {x:,.0f}"),
                textposition='outside',
                textfont=dict(color='#0B1220', size=11)
            ))
            apply_plotly_theme(fig_day, height=360)
            st.plotly_chart(fig_day, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_v2:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Distribución del Monto por Ticket</div>', unsafe_allow_html=True)
            fig_hist = gg.Figure(gg.Histogram(
                x=df_curr['Ventas_Soles'],
                nbinsx=15,
                marker=dict(color='#6C5CE7', edgecolor='#0E1B2E')
            ))
            apply_plotly_theme(fig_hist, height=360)
            st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Registro Completo de Transacciones</div>', unsafe_allow_html=True)
        st.dataframe(df_curr[['ID_Transaccion', 'Fecha', 'Categoria', 'Producto', 'Canal_Venta', 'Cantidad', 'Ventas_Soles', 'Utilidad_Soles']], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # PESTAÑA 03. PRODUCTOS
    # =========================================================
    elif nav_sel.startswith("03"):
        st.markdown("<h2 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Análisis de Productos Estrella</h2>", unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Top 10 Productos por Facturación (S/)</div>', unsafe_allow_html=True)
            df_p_val = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()
            fig_p_val = gg.Figure(gg.Bar(
                x=df_p_val['Ventas_Soles'], y=df_p_val['Producto'],
                orientation='h',
                marker=dict(color='#00C2D1', cornerradius=4),
                text=df_p_val['Ventas_Soles'].apply(lambda x: f"S/ {x:,.0f}"),
                textposition='outside',
                textfont=dict(color='#0B1220', size=11)
            ))
            apply_plotly_theme(fig_p_val, height=380)
            st.plotly_chart(fig_p_val, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_p2:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Top 10 Productos por Volumen (Unidades)</div>', unsafe_allow_html=True)
            df_p_qty = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()
            fig_p_qty = gg.Figure(gg.Bar(
                x=df_p_qty['Cantidad'], y=df_p_qty['Producto'],
                orientation='h',
                marker=dict(color='#6C5CE7', cornerradius=4),
                text=df_p_qty['Cantidad'].apply(lambda x: f"{x} un."),
                textposition='outside',
                textfont=dict(color='#0B1220', size=11)
            ))
            apply_plotly_theme(fig_p_qty, height=380)
            st.plotly_chart(fig_p_qty, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # PESTAÑA 04. RENTABILIDAD
    # =========================================================
    elif nav_sel.startswith("04"):
        st.markdown("<h2 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Análisis de Rentabilidad y Márgenes</h2>", unsafe_allow_html=True)
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Margen de Ganancia (%) por Categoría</div>', unsafe_allow_html=True)
            df_prof_cat = df_curr.groupby('Categoria').apply(
                lambda x: (x['Utilidad_Soles'].sum() / x['Ventas_Soles'].sum() * 100) if x['Ventas_Soles'].sum() > 0 else 0
            ).reset_index(name='Margen_Pct')
            
            fig_prof = gg.Figure(gg.Bar(
                x=df_prof_cat['Categoria'], y=df_prof_cat['Margen_Pct'],
                marker=dict(color='#10B981', cornerradius=4),
                text=df_prof_cat['Margen_Pct'].apply(lambda x: f"{x:.1f}%"),
                textposition='outside',
                textfont=dict(color='#0B1220', size=11)
            ))
            apply_plotly_theme(fig_prof, height=360)
            st.plotly_chart(fig_prof, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_r2:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Relación Ventas vs. Utilidad Neta por Producto</div>', unsafe_allow_html=True)
            df_p_scat = df_curr.groupby('Producto')[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
            fig_scat = gg.Figure(gg.Scatter(
                x=df_p_scat['Ventas_Soles'], y=df_p_scat['Utilidad_Soles'],
                mode='markers+text',
                text=df_p_scat['Producto'],
                textposition='top center',
                marker=dict(size=12, color='#6C5CE7')
            ))
            apply_plotly_theme(fig_scat, height=360)
            st.plotly_chart(fig_scat, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # PESTAÑA 05. ANÁLISIS
    # =========================================================
    elif nav_sel.startswith("05"):
        st.markdown("<h2 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Análisis Inteligente y Patrones</h2>", unsafe_allow_html=True)
        
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Matriz de Ventas por Canal y Categoría</div>', unsafe_allow_html=True)
        df_piv = df_curr.pivot_table(index='Categoria', columns='Canal_Venta', values='Ventas_Soles', aggfunc='sum', fill_value=0)
        
        fig_heat = gg.Figure(gg.Heatmap(
            z=df_piv.values,
            x=df_piv.columns,
            y=df_piv.index,
            colorscale='Blues',
            texttemplate='S/ %{z:,.0f}',
            textfont=dict(color='#0B1220', size=12)
        ))
        apply_plotly_theme(fig_heat, height=360)
        st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # PESTAÑA 06. SIMULADOR
    # =========================================================
    elif nav_sel.startswith("06"):
        st.markdown("<h2 style='font-family: Space Grotesk, sans-serif; color: #0B1220;'>Simulador Financiero MYPE</h2>", unsafe_allow_html=True)
        
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Escenario Interactivo de Crecimiento</div>', unsafe_allow_html=True)
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            pct_price = st.slider("Aumento de Precios (%):", -10, 30, 5)
        with sc2:
            pct_vol = st.slider("Incremento de Volumen (%):", -20, 50, 10)
        with sc3:
            pct_cost = st.slider("Reducción de Costos (%):", 0, 20, 5)
            
        base_vtas = df_curr['Ventas_Soles'].sum()
        base_csto = df_curr['Costo_Soles'].sum()
        base_util = df_curr['Utilidad_Soles'].sum()
        
        sim_vtas = base_vtas * (1 + pct_price/100) * (1 + pct_vol/100)
        sim_csto = base_csto * (1 - pct_cost/100) * (1 + pct_vol/100)
        sim_util = sim_vtas - sim_csto
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Ventas Proyectadas", f"S/ {sim_vtas:,.2f}", f"{((sim_vtas-base_vtas)/base_vtas*100):+.1f}%")
        with m2:
            st.metric("Costos Proyectados", f"S/ {sim_csto:,.2f}", f"{((sim_csto-base_csto)/base_csto*100):+.1f}%")
        with m3:
            st.metric("Utilidad Proyectada", f"S/ {sim_util:,.2f}", f"{((sim_util-base_util)/base_util*100):+.1f}%")
            
        fig_sim = gg.Figure([
            gg.Bar(name='Actual', x=['Ventas', 'Costos', 'Utilidad'], y=[base_vtas, base_csto, base_util], marker_color='#8C9BAE'),
            gg.Bar(name='Proyectado', x=['Ventas', 'Costos', 'Utilidad'], y=[sim_vtas, sim_csto, sim_util], marker_color='#00C2D1')
        ])
        apply_plotly_theme(fig_sim, height=340)
        st.plotly_chart(fig_sim, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
