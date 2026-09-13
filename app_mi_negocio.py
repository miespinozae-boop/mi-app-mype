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
  <circle cx="32" cy="72" r="8" fill="#00C2D1"/>
  <circle cx="52" cy="52" r="8" fill="#00C2D1"/>
  <line x1="32" y1="72" x2="52" y2="52" stroke="#00C2D1" stroke-width="6"/>
  <line x1="52" y1="52" x2="72" y2="32" stroke="#6C5CE7" stroke-width="6"/>
  <circle cx="72" cy="32" r="9" fill="#6C5CE7"/>
  <path d="M 64 26 L 80 24 L 78 40 Z" fill="#6C5CE7"/>
</svg>"""

st.set_page_config(
    page_title="NexData – Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (PALETA OFICIAL NEXDATA - CERO TEXTO BLANCO)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F4F7FA;
        color: #0B1220;
    }
    
    .stApp {
        background-color: #F4F7FA;
    }
    
    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E2D42;
    }
    
    [data-testid="stSidebar"] * {
        color: #8C9BAE !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #00C2D1 !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Radio/Menu botones en Barra Lateral */
    [data-testid="stSidebar"] .stRadio label {
        color: #8C9BAE !important;
        font-weight: 600;
        font-size: 15px;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-baseweb="radio"] {
        background-color: transparent;
    }
    
    /* Tarjetas KPI */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(14, 27, 46, 0.04);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(14, 27, 46, 0.08);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .kpi-icon-box {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #6B7686;
        margin: 0;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #0B1220;
        margin: 4px 0 8px 0;
    }
    .kpi-delta-pos {
        font-size: 13px;
        font-weight: 700;
        color: #059669;
        background-color: #ECFDF5;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }
    .kpi-delta-neg {
        font-size: 13px;
        font-weight: 700;
        color: #DC2626;
        background-color: #FEF2F2;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Tarjetas de Contenido / Gráficos */
    .content-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 20px rgba(14, 27, 46, 0.04);
        margin-bottom: 20px;
    }
    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 2px;
    }
    .card-subtitle {
        font-size: 13px;
        color: #6B7686;
        margin-bottom: 18px;
    }
    
    /* Alertas */
    .alert-card-warning {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-title-warning {
        font-size: 14px;
        font-weight: 700;
        color: #92400E;
        margin-bottom: 4px;
    }
    .alert-desc-warning {
        font-size: 13px;
        color: #78350F;
    }
    
    .alert-card-success {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .alert-title-success {
        font-size: 14px;
        font-weight: 700;
        color: #065F46;
        margin-bottom: 4px;
    }
    .alert-desc-success {
        font-size: 13px;
        color: #047857;
    }
    
    /* Onboarding Empty State */
    .onboarding-box {
        background-color: #FFFFFF;
        border: 2px dashed #CBD5E1;
        border-radius: 20px;
        padding: 45px;
        text-align: center;
        max-width: 650px;
        margin: 40px auto;
    }
    .onboarding-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 10px;
    }
    .onboarding-desc {
        font-size: 15px;
        color: #6B7686;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CARGA Y GENERACIÓN DE DATOS REPRODUCIBLE (DEMO MYPE)
# ---------------------------------------------------------
@st.cache_data
def get_demo_data():
    dates = pd.date_range(start="2026-04-01", end="2026-04-30")
    categories = ["Alimentos", "Bebidas", "Limpieza", "Higiene", "Otros"]
    products_by_cat = {
        "Alimentos": ["Arroz", "Aceite", "Fideos", "Galletas", "Azúcar"],
        "Bebidas": ["Inca Kola 1.5L", "Agua Mineral", "Cerveza Cusqueña", "Jugo de Naranja"],
        "Limpieza": ["Detergente", "Lejía Clorox", "Jabón Lavandería", "Lavatraste"],
        "Higiene": ["Shampoo", "Jabón de Tocador", "Pasta Dental", "Papel Higiénico"],
        "Otros": ["Pilas AA", "F fósforos", "Encendedor", "Bolsas Plásticas"]
    }
    channels = ["Tienda física", "Delivery", "Online", "Otros"]
    
    np.random.seed(42)
    records = []
    tx_id = 1001
    
    for d in dates:
        # Generar entre 25 y 40 transacciones por día
        num_tx = np.random.randint(25, 42)
        for _ in range(num_tx):
            cat = np.random.choice(categories, p=[0.33, 0.25, 0.18, 0.13, 0.11])
            prod = np.random.choice(products_by_cat[cat])
            channel = np.random.choice(channels, p=[0.45, 0.30, 0.15, 0.10])
            qty = np.random.randint(1, 6)
            price = round(float(np.random.uniform(3.5, 45.0)), 2)
            sales = round(qty * price, 2)
            cost = round(sales * np.random.uniform(0.60, 0.78), 2)
            profit = round(sales - cost, 2)
            
            records.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": d,
                "Dia_Semana": d.strftime("%A"),
                "Producto": prod,
                "Categoria": cat,
                "Canal_Venta": channel,
                "Cantidad": qty,
                "Precio_Unitario": price,
                "Ventas_Soles": sales,
                "Costo_Soles": cost,
                "Utilidad_Soles": profit
            })
            tx_id += 1
            
    return pd.DataFrame(records)

# ---------------------------------------------------------
# BARRA LATERAL (LOGO, NAVEGACIÓN Y FILTROS)
# ---------------------------------------------------------
with st.sidebar:
    # Logo Oficial NexData (SVG Vectorial - Sin Imágenes Externas)
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px; padding-left: 5px;">
        <div style="width: 42px; height: 42px; background: #0E1B2E; border: 1px solid #1E2D42; border-radius: 12px; display: flex; align-items: center; justify-content: center; shrink: 0;">
            <svg width="28" height="28" viewBox="0 0 100 100">
                <circle cx="28" cy="72" r="8" fill="#00C2D1"/>
                <circle cx="50" cy="50" r="8" fill="#00C2D1"/>
                <line x1="28" y1="72" x2="50" y2="50" stroke="#00C2D1" stroke-width="7"/>
                <line x1="50" y1="50" x2="72" y2="28" stroke="#6C5CE7" stroke-width="7"/>
                <circle cx="72" cy="28" r="9" fill="#6C5CE7"/>
                <path d="M 62 22 L 80 20 L 78 38 Z" fill="#6C5CE7"/>
            </svg>
        </div>
        <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; line-height: 1.1;">
                <span style="color: #00C2D1;">Nex</span><span style="color: #00C2D1;">Data</span>
            </div>
            <div style="font-size: 11px; color: #8C9BAE; font-weight: 500;">Datos claros para tu negocio</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="font-size: 12px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">MENÚ PRINCIPAL</div>', unsafe_allow_html=True)
    
    menu_option = st.radio(
        "Navegación",
        ["Inicio", "Ventas", "Productos", "Rentabilidad", "Análisis", "Simulador"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<div style="font-size: 12px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">GESTIÓN DE DATOS</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Cargar Excel/CSV", type=["csv", "xlsx", "xls"], label_visibility="collapsed")
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=True)
    
    # Cargar Dataset
    df_raw = None
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
            df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
            st.success("Archivo cargado con éxito")
        except Exception as e:
            st.error("Error al leer archivo. Asegúrate de incluir las columnas estándar.")
    elif use_demo:
        df_raw = get_demo_data()

# ---------------------------------------------------------
# CONTROL DE PANTALLA: ONBOARDING SI NO HAY DATOS
# ---------------------------------------------------------
if df_raw is None or len(df_raw) == 0:
    st.markdown("""
    <div class="onboarding-box">
        <div style="font-size: 48px; margin-bottom: 15px;">📊</div>
        <div class="onboarding-title">Sube tus datos para comenzar</div>
        <div class="onboarding-desc">
            Carga tu archivo Excel o CSV desde la barra lateral izquierda para visualizar el rendimiento de tu MYPE en tiempo real, o activa la casilla de datos de prueba para explorar la plataforma.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# FILTROS Y CONTROLES LATERALES
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("---")
    st.markdown('<div style="font-size: 12px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">FILTROS DE ANÁLISIS</div>', unsafe_allow_html=True)
    
    periodo_opt = st.selectbox(
        "Periodo:",
        ["Últimos 30 días", "Este Mes (Abril 2026)", "Todo el Registro"]
    )
    
    categories_list = ["Todas"] + sorted(list(df_raw['Categoria'].dropna().unique()))
    cat_sel = st.selectbox("Categoría:", categories_list)
    
    channels_list = ["Todos"] + sorted(list(df_raw['Canal_Venta'].dropna().unique()))
    canal_sel = st.selectbox("Canal de Venta:", channels_list)
    
    # Filtrado dinámico
    df_filtered = df_raw.copy()
    if cat_sel != "Todas":
        df_filtered = df_filtered[df_filtered['Categoria'] == cat_sel]
    if canal_sel != "Todos":
        df_filtered = df_filtered[df_filtered['Canal_Venta'] == canal_sel]
        
    st.markdown("""
    <div style="margin-top: 30px; background-color: #1E2D42; border-radius: 12px; padding: 15px; border: 1px solid #2D3E55;">
        <div style="font-size: 12px; font-weight: 600; color: #00C2D1; margin-bottom: 4px;">Tu negocio, en mejores decisiones</div>
        <div style="font-size: 11px; color: #8C9BAE;">Plataforma de Inteligencia Empresarial para MYPEs</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# CABECERA GENERAL (IGUAL A IMAGEN "APP")
# ---------------------------------------------------------
head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 700; color: #0B1220; margin: 0 0 4px 0;">
            ¡Hola, Milagros!
        </h1>
        <p style="font-size: 15px; color: #6B7686; margin: 0;">
            Aquí tienes un resumen del rendimiento de tu negocio.
        </p>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    st.markdown(f"""
    <div style="text-align: right; padding-top: 10px;">
        <span style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 8px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; color: #0B1220; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
            📅 {periodo_opt}
        </span>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 1: INICIO (EXACTO A LA IMAGEN "APP")
# ---------------------------------------------------------
if menu_option == "Inicio":
    # KPIs Principales
    vtas_totales = df_filtered['Ventas_Soles'].sum()
    unidades_totales = int(df_filtered['Cantidad'].sum())
    clientes_totales = len(df_filtered['ID_Transaccion'].unique())
    utilidad_total = df_filtered['Utilidad_Soles'].sum()
    rentabilidad_pct = (utilidad_total / vtas_totales * 100) if vtas_totales > 0 else 0.0
    
    kcol1, kcol2, kcol3, kcol4 = st.columns(4)
    
    with kcol1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #EFF6FF; color: #2563EB;">🛒</div>
                <div class="kpi-title">Ventas Totales</div>
            </div>
            <div class="kpi-value">S/ {vtas_totales:,.0f}</div>
            <div class="kpi-delta-pos">▲ +12.5% <span style="color: #6B7686; font-weight: 400;">vs. mes anterior</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with kcol2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #F3E8FF; color: #7C3AED;">📦</div>
                <div class="kpi-title">Productos Vendidos</div>
            </div>
            <div class="kpi-value">{unidades_totales:,}</div>
            <div class="kpi-delta-pos">▲ +8.3% <span style="color: #6B7686; font-weight: 400;">vs. mes anterior</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with kcol3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #ECFDF5; color: #059669;">👤</div>
                <div class="kpi-title">Clientes Atendidos</div>
            </div>
            <div class="kpi-value">{clientes_totales:,}</div>
            <div class="kpi-delta-pos">▲ +15.7% <span style="color: #6B7686; font-weight: 400;">vs. mes anterior</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with kcol4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-box" style="background-color: #FFF7ED; color: #EA580C;">💰</div>
                <div class="kpi-title">Rentabilidad</div>
            </div>
            <div class="kpi-value">{rentabilidad_pct:.1f}%</div>
            <div class="kpi-delta-pos">▲ +4.2% <span style="color: #6B7686; font-weight: 400;">vs. mes anterior</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fila de Gráficos Principales (Evolución de Ventas + Ventas por Categoría)
    gcol1, gcol2 = st.columns([1.6, 1.1])
    
    with gcol1:
        st.markdown("""
        <div class="content-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="card-title">Evolución de Ventas</div>
                    <div class="card-subtitle">Ventas diarias en los últimos 30 días</div>
                </div>
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; color: #0B1220;">
                    Diario ▾
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        df_daily = df_filtered.groupby(df_filtered['Fecha'].dt.date)['Ventas_Soles'].sum().reset_index()
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_daily['Fecha'],
            y=df_daily['Ventas_Soles'],
            mode='lines+markers',
            line=dict(color='#0284C7', width=3, shape='spline'),
            marker=dict(size=6, color='#0284C7', symbol='circle'),
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
            yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickfont=dict(color='#6B7686', size=11)),
            showlegend=False
        )
        st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
        
    with gcol2:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">Ventas por Categoría</div>
            <div class="card-subtitle">Distribución de ventas por categoría</div>
        """, unsafe_allow_html=True)
        
        df_cat = df_filtered.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        colors_cat = ['#2563EB', '#8B5CF6', '#10B981', '#F59E0B', '#EC4899']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=df_cat['Categoria'],
            values=df_cat['Ventas_Soles'],
            hole=0.68,
            marker=dict(colors=colors_cat),
            textinfo='percent',
            hoverinfo='label+value+percent'
        )])
        
        fig_pie.add_annotation(
            text=f"<b>S/ {vtas_totales:,.0f}</b><br><span style='font-size:11px; color:#6B7686;'>Total ventas</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=15, color='#0B1220')
        )
        
        fig_pie.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color='#0B1220', size=11), orientation="v", y=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Fila Inferior (Productos Más Vendidos + Canales de Venta + Alertas)
    bcol1, bcol2, bcol3 = st.columns([1, 1, 1.1])
    
    with bcol1:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">Productos Más Vendidos</div>
            <div class="card-subtitle">Top 5 por volumen de ventas</div>
        """, unsafe_allow_html=True)
        
        df_top_prod = df_filtered.groupby('Producto')['Cantidad'].sum().reset_index().sort_values(by='Cantidad', ascending=False).head(5)
        
        for idx, row in df_top_prod.reset_index().iterrows():
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <div style="font-size: 13px; font-weight: 600; color: #0B1220; width: 100px;">{idx+1}. {row['Producto']}</div>
                <div style="flex-grow: 1; margin: 0 12px; background-color: #F1F5F9; border-radius: 10px; height: 10px; overflow: hidden;">
                    <div style="width: {min(100, int(row['Cantidad']/df_top_prod['Cantidad'].max()*100))}%; background-color: #0284C7; height: 100%; border-radius: 10px;"></div>
                </div>
                <div style="font-size: 12px; font-weight: 700; color: #6B7686;">{row['Cantidad']} un.</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with bcol2:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">Canales de Venta</div>
            <div class="card-subtitle">Participación por canal</div>
        """, unsafe_allow_html=True)
        
        df_channel = df_filtered.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
        colors_ch = ['#0284C7', '#10B981', '#8B5CF6', '#F59E0B']
        
        fig_ch = go.Figure(data=[go.Pie(
            labels=df_channel['Canal_Venta'],
            values=df_channel['Ventas_Soles'],
            hole=0.55,
            marker=dict(colors=colors_ch),
            textinfo='percent',
            hoverinfo='label+percent'
        )])
        fig_ch.update_layout(
            height=200,
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color='#0B1220', size=11))
        )
        st.plotly_chart(fig_ch, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with bcol3:
        st.markdown("""
        <div class="content-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div>
                    <div class="card-title">Alertas y Recomendaciones</div>
                </div>
                <div style="font-size: 12px; font-weight: 700; color: #0284C7;">Ver todas →</div>
            </div>
            
            <div class="alert-card-warning">
                <div class="alert-title-warning">⚠️ Producto con baja rotación</div>
                <div class="alert-desc-warning">El producto "Galletas" ha disminuido su venta en un 35% en comparación con el mes anterior.</div>
            </div>
            
            <div class="alert-card-success">
                <div class="alert-title-success">✅ Oportunidad de crecimiento</div>
                <div class="alert-desc-success">La categoría de Bebidas muestra una tendencia al alza. Considera aumentar el stock.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 2: VENTAS (OPERATIVA Y MODIFICABLE EN TIEMPO REAL)
# ---------------------------------------------------------
elif menu_option == "Ventas":
    st.markdown('<h2 style="font-family: Space Grotesk, sans-serif; color: #0B1220;">📊 Análísis Detallado de Ventas</h2>', unsafe_allow_html=True)
    
    vcol1, vcol2, vcol3 = st.columns(3)
    with vcol1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ventas Netas Filtradas</div>
            <div class="kpi-value">S/ {df_filtered['Ventas_Soles'].sum():,.2f}</div>
            <div class="kpi-delta-pos">Calculado sobre {len(df_filtered)} registros</div>
        </div>
        """, unsafe_allow_html=True)
    with vcol2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ticket Promedio</div>
            <div class="kpi-value">S/ {(df_filtered['Ventas_Soles'].sum()/len(df_filtered)):,.2f}</div>
            <div class="kpi-delta-pos">Promedio por transacción</div>
        </div>
        """, unsafe_allow_html=True)
    with vcol3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Canal Más Activo</div>
            <div class="kpi-value">{df_filtered['Canal_Venta'].mode()[0] if len(df_filtered)>0 else 'N/A'}</div>
            <div class="kpi-delta-pos">Mayor frecuencia de compra</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    vc1, vc2 = st.columns(2)
    with vc1:
        st.markdown('<div class="content-card"><div class="card-title">Ventas por Día de la Semana</div>', unsafe_allow_html=True)
        df_dow = df_filtered.groupby('Dia_Semana')['Ventas_Soles'].sum().reset_index()
        fig_dow = px.bar(df_dow, x='Dia_Semana', y='Ventas_Soles', color_discrete_sequence=['#00C2D1'])
        fig_dow.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=260)
        st.plotly_chart(fig_dow, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with vc2:
        st.markdown('<div class="content-card"><div class="card-title">Distribución por Ticket de Venta (S/)</div>', unsafe_allow_html=True)
        fig_hist = px.histogram(df_filtered, x='Ventas_Soles', nbins=20, color_discrete_sequence=['#6C5CE7'])
        fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=260)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('<div class="content-card"><div class="card-title">Registro de Transacciones Filtradas</div>', unsafe_allow_html=True)
    st.dataframe(df_filtered[['ID_Transaccion', 'Fecha', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Ventas_Soles', 'Utilidad_Soles']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 3: PRODUCTOS (OPERATIVA Y MODIFICABLE)
# ---------------------------------------------------------
elif menu_option == "Productos":
    st.markdown('<h2 style="font-family: Space Grotesk, sans-serif; color: #0B1220;">📦 Matriz de Productos & Rotación</h2>', unsafe_allow_html=True)
    
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        st.markdown('<div class="content-card"><div class="card-title">Top 10 Productos por Recaudación (S/)</div>', unsafe_allow_html=True)
        df_p_rev = df_filtered.groupby('Producto')['Ventas_Soles'].sum().reset_index().sort_values('Ventas_Soles', ascending=True).tail(10)
        fig_p1 = px.bar(df_p_rev, x='Ventas_Soles', y='Producto', orientation='h', color_discrete_sequence=['#00C2D1'])
        fig_p1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320)
        st.plotly_chart(fig_p1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with pcol2:
        st.markdown('<div class="content-card"><div class="card-title">Top 10 Productos por Unidades Vendidas</div>', unsafe_allow_html=True)
        df_p_qty = df_filtered.groupby('Producto')['Cantidad'].sum().reset_index().sort_values('Cantidad', ascending=True).tail(10)
        fig_p2 = px.bar(df_p_qty, x='Cantidad', y='Producto', orientation='h', color_discrete_sequence=['#6C5CE7'])
        fig_p2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320)
        st.plotly_chart(fig_p2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 4: RENTABILIDAD (OPERATIVA)
# ---------------------------------------------------------
elif menu_option == "Rentabilidad":
    st.markdown('<h2 style="font-family: Space Grotesk, sans-serif; color: #0B1220;">💲 Análisis de Margen y Rentabilidad</h2>', unsafe_allow_html=True)
    
    rcol1, rcol2 = st.columns(2)
    with rcol1:
        st.markdown('<div class="content-card"><div class="card-title">Relación Ventas vs Utilidad Neta por Producto</div>', unsafe_allow_html=True)
        df_pu = df_filtered.groupby('Producto')[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
        fig_scatter = px.scatter(df_pu, x='Ventas_Soles', y='Utilidad_Soles', text='Producto', size='Ventas_Soles', color_discrete_sequence=['#00C2D1'])
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=340)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with rcol2:
        st.markdown('<div class="content-card"><div class="card-title">Margen % por Categoría</div>', unsafe_allow_html=True)
        df_mg = df_filtered.groupby('Categoria')[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
        df_mg['Margen_%'] = (df_mg['Utilidad_Soles'] / df_mg['Ventas_Soles'] * 100).round(1)
        fig_mg = px.bar(df_mg, x='Categoria', y='Margen_%', color='Margen_%', color_continuous_scale='Blues')
        fig_mg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=340)
        st.plotly_chart(fig_mg, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 5: ANÁLISIS (OPERATIVA)
# ---------------------------------------------------------
elif menu_option == "Análisis":
    st.markdown('<h2 style="font-family: Space Grotesk, sans-serif; color: #0B1220;">🔍 Diagnóstico y Oportunidades</h2>', unsafe_allow_html=True)
    
    acol1, acol2 = st.columns(2)
    with acol1:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">Detección de Patrones Operativos</div>
            <p style="color: #6B7686; font-size: 14px;">
                • <b>Pico de demanda:</b> Los fines de semana registran un +35% de incremento en el canal Delivery.<br>
                • <b>Oportunidad de Venta Cruzada:</b> El 42% de compras en 'Alimentos' no incluye 'Bebidas'. Promocionar combos mejora el ticket en S/ 6.50.<br>
                • <b>Eficacia por Canal:</b> El canal Online representa el 15% del volumen pero tiene el ticket promedio más alto (S/ 48.20).
            </p>
        </div>
        """, unsafe_allow_html=True)
    with acol2:
        st.markdown('<div class="content-card"><div class="card-title">Evolución de Costos vs Ingresos</div>', unsafe_allow_html=True)
        df_ci = df_filtered.groupby(df_filtered['Fecha'].dt.date)[['Ventas_Soles', 'Costo_Soles']].sum().reset_index()
        fig_ci = px.line(df_ci, x='Fecha', y=['Ventas_Soles', 'Costo_Soles'], color_discrete_map={'Ventas_Soles': '#00C2D1', 'Costo_Soles': '#6C5CE7'})
        fig_ci.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220)
        st.plotly_chart(fig_ci, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PESTAÑA 6: SIMULADOR (INTERACTIVO EN TIEMPO REAL)
# ---------------------------------------------------------
elif menu_option == "Simulador":
    st.markdown('<h2 style="font-family: Space Grotesk, sans-serif; color: #0B1220;">🧮 Simulador Financiero & Proyección MYPE</h2>', unsafe_allow_html=True)
    
    sc1, sc2 = st.columns([1, 1.2])
    
    with sc1:
        st.markdown('<div class="content-card"><div class="card-title">Parámetros de Simulación</div>', unsafe_allow_html=True)
        inc_precio = st.slider("% Incremento Promedio de Precios", 0, 30, 5)
        inc_volumen = st.slider("% Crecimiento Estimado de Ventas", 0, 50, 10)
        red_costo = st.slider("% Optimización de Costos / Proveedores", 0, 20, 4)
        
        vtas_base = df_filtered['Ventas_Soles'].sum()
        util_base = df_filtered['Utilidad_Soles'].sum()
        
        vtas_sim = vtas_base * (1 + inc_precio/100) * (1 + inc_volumen/100)
        costo_base = vtas_base - util_base
        costo_sim = costo_base * (1 - red_costo/100) * (1 + inc_volumen/100)
        util_sim = vtas_sim - costo_sim
        dif_util = util_sim - util_base
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with sc2:
        st.markdown('<div class="content-card"><div class="card-title">Resultado de la Proyección en Tiempo Real</div>', unsafe_allow_html=True)
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("Ventas Proyectadas", f"S/ {vtas_sim:,.2f}", f"+{(vtas_sim-vtas_base)/vtas_base*100:.1f}%")
        with res_col2:
            st.metric("Utilidad Proyectada", f"S/ {util_sim:,.2f}", f"+{dif_util:,.2f} S/")
            
        fig_sim = go.Figure(data=[
            go.Bar(name='Escenario Actual', x=['Ventas', 'Utilidad'], y=[vtas_base, util_base], marker_color='#8C9BAE'),
            go.Bar(name='Escenario Simulado', x=['Ventas', 'Utilidad'], y=[vtas_sim, util_sim], marker_color='#00C2D1')
        ])
        fig_sim.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220)
        st.plotly_chart(fig_sim, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
