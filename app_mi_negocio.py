import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y FAVICON NEXDATA
# ---------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<rect width="100" height="100" rx="22" fill="#0E1B2E"/>
<path d="M 20 75 L 45 45 L 65 60 L 82 25" stroke="#00C2D1" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<circle cx="20" cy="75" r="6" fill="#00C2D1"/>
<circle cx="45" cy="45" r="6" fill="#00C2D1"/>
<circle cx="65" cy="60" r="6" fill="#00C2D1"/>
<path d="M 82 25 L 82 40 M 82 25 L 67 25" stroke="#6C5CE7" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

st.set_page_config(
    page_title="NexData – Inteligencia Comercial MYPE",
    page_icon="data:image/svg+xml;utf8," + FAVICON_SVG.replace("#", "%23").replace("\n", ""),
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. ESTILOS CSS - REGLA ESTRICTA CERO TEXTO BLANCO
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8FAFC !important;
        color: #0B1220 !important;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }

    [data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #8C9BAE !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] strong {
        color: #00C2D1 !important;
    }

    /* TARJETAS KPI */
    .metric-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        text-align: left;
        box-shadow: 0 4px 20px rgba(14, 27, 46, 0.04);
        margin-bottom: 15px;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 700;
        color: #6B7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #0B1220 !important;
        margin: 4px 0;
    }
    .metric-delta-pos {
        font-size: 12px;
        font-weight: 700;
        color: #059669 !important;
    }
    .metric-delta-neg {
        font-size: 12px;
        font-weight: 700;
        color: #DC2626 !important;
    }

    /* PESTAÑAS STYLED */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #F1F5F9;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        color: #6B7280 !important;
        background-color: transparent;
        padding: 0 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #0B1220 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. LOGO SVG NEXDATA EN LA BARRA LATERAL
# ---------------------------------------------------------
SIDEBAR_LOGO_HTML = """
<div style="padding: 10px 0 20px 0; text-align: left;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="width: 42px; height: 42px; background-color: #0E1B2E; border-radius: 10px; border: 1px solid #1E2D42; padding: 6px; display: flex; align-items: center; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" style="width: 100%; height: 100%;">
                <path d="M 20 75 L 45 45 L 65 60 L 82 25" stroke="#00C2D1" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                <circle cx="20" cy="75" r="7" fill="#00C2D1"/>
                <circle cx="45" cy="45" r="7" fill="#00C2D1"/>
                <circle cx="65" cy="60" r="7" fill="#00C2D1"/>
                <path d="M 82 25 L 82 42 M 82 25 L 65 25" stroke="#6C5CE7" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; line-height: 1.1;">
                <span style="color: #00C2D1 !important;">Nex</span><span style="color: #8C9BAE !important;">Data</span>
            </div>
            <div style="font-size: 11px; color: #8C9BAE !important; font-weight: 500;">Datos claros para tu negocio</div>
        </div>
    </div>
</div>
"""
st.sidebar.markdown(SIDEBAR_LOGO_HTML, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. CARGADOR INTELIGENTE MULTI-FORMATO (EXCEL / CSV)
# ---------------------------------------------------------
def load_and_process_dataset(source_file):
    """
    Lee archivos Excel (.xlsx) o CSV, detecta la pestaña de transacciones,
    mapea las columnas y calcula dinámicamente Ventas y Utilidad.
    """
    try:
        if isinstance(source_file, str):
            if source_file.endswith('.xlsx') or source_file.endswith('.xls'):
                xls = pd.ExcelFile(source_file)
                sheet_target = xls.sheet_names[0]
                for sheet in xls.sheet_names:
                    if 'transacc' in sheet.lower() or 'base' in sheet.lower() or 'ventas' in sheet.lower():
                        sheet_target = sheet
                        break
                df = pd.read_excel(source_file, sheet_name=sheet_target)
            else:
                df = pd.read_csv(source_file)
        else:
            filename = source_file.name.lower()
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                xls = pd.ExcelFile(source_file)
                sheet_target = xls.sheet_names[0]
                for sheet in xls.sheet_names:
                    if 'transacc' in sheet.lower() or 'base' in sheet.lower() or 'ventas' in sheet.lower():
                        sheet_target = sheet
                        break
                df = pd.read_excel(source_file, sheet_name=sheet_target)
            else:
                df = pd.read_csv(source_file)

        # Mapeo flexible de columnas
        col_map = {}
        for col in df.columns:
            c_clean = str(col).strip().lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            if 'id' in c_clean or 'transaccion' in c_clean or 'ticket' in c_clean:
                col_map[col] = 'ID_Transaccion'
            elif 'fecha' in c_clean or 'date' in c_clean:
                col_map[col] = 'Fecha'
            elif 'dia' in c_clean or 'week' in c_clean:
                col_map[col] = 'Dia_Semana'
            elif 'producto' in c_clean or 'item' in c_clean or 'descripcion' in c_clean:
                col_map[col] = 'Producto'
            elif 'categoria' in c_clean or 'linea' in c_clean or 'rubro' in c_clean:
                col_map[col] = 'Categoria'
            elif 'canal' in c_clean or 'medio' in c_clean:
                col_map[col] = 'Canal_Venta'
            elif 'cantidad' in c_clean or 'cant' in c_clean or 'unidades' in c_clean:
                col_map[col] = 'Cantidad'
            elif 'precio' in c_clean or 'pu' in c_clean or 'p_unit' in c_clean:
                col_map[col] = 'Precio_Unitario'
            elif 'venta' in c_clean or 'monto' in c_clean or 'ingreso' in c_clean or 'total' in c_clean:
                col_map[col] = 'Ventas_Soles'
            elif 'costo' in c_clean or 'c_unit' in c_clean:
                col_map[col] = 'Costo_Soles'
            elif 'utilidad' in c_clean or 'ganancia' in c_clean or 'margen' in c_clean:
                col_map[col] = 'Utilidad_Soles'

        df = df.rename(columns=col_map)

        # Rellenar columnas faltantes
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        else:
            df['Fecha'] = pd.date_range(start='2026-08-01', periods=len(df), freq='h')

        if 'Dia_Semana' not in df.columns:
            df['Dia_Semana'] = df['Fecha'].dt.day_name()

        if 'Cantidad' in df.columns:
            df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce').fillna(1)
        else:
            df['Cantidad'] = 1

        if 'Precio_Unitario' in df.columns:
            df['Precio_Unitario'] = pd.to_numeric(df['Precio_Unitario'], errors='coerce').fillna(10.0)
        else:
            df['Precio_Unitario'] = 10.0

        if 'Ventas_Soles' in df.columns:
            df['Ventas_Soles'] = pd.to_numeric(df['Ventas_Soles'], errors='coerce')
            df['Ventas_Soles'] = df['Ventas_Soles'].fillna(df['Cantidad'] * df['Precio_Unitario'])
        else:
            df['Ventas_Soles'] = df['Cantidad'] * df['Precio_Unitario']

        if 'Costo_Soles' in df.columns:
            df['Costo_Soles'] = pd.to_numeric(df['Costo_Soles'], errors='coerce')
            df['Costo_Soles'] = df['Costo_Soles'].fillna(df['Ventas_Soles'] * 0.65)
        else:
            df['Costo_Soles'] = df['Ventas_Soles'] * 0.65

        if 'Utilidad_Soles' in df.columns:
            df['Utilidad_Soles'] = pd.to_numeric(df['Utilidad_Soles'], errors='coerce')
            df['Utilidad_Soles'] = df['Utilidad_Soles'].fillna(df['Ventas_Soles'] - df['Costo_Soles'])
        else:
            df['Utilidad_Soles'] = df['Ventas_Soles'] - df['Costo_Soles']

        if 'Categoria' not in df.columns:
            df['Categoria'] = 'General'

        if 'Producto' not in df.columns:
            df['Producto'] = 'Producto Genérico'

        if 'Canal_Venta' not in df.columns:
            df['Canal_Venta'] = 'Tienda Física'

        return df
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
        return None

# ---------------------------------------------------------
# 5. CONTROLES Y FUENTE DE DATOS EN BARRA LATERAL
# ---------------------------------------------------------
st.sidebar.markdown("<h3 style='font-size: 14px; font-weight: 700;'>📂 FUENTE DE DATOS</h3>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader(
    "Subir Base de Datos (.xlsx o .csv):",
    type=['xlsx', 'xls', 'csv'],
    help="Sube tu archivo de ventas para analizar cualquier negocio."
)

demo_option = st.sidebar.selectbox(
    "O Seleccionar Demo MYPE:",
    ["🛒 Abarrotes / Minimarket (Demo)", "💊 Botica & Farmacia (Demo)", "🍾 Licorería & Licores (Demo)"]
)

# Cargar dataset según selección
df_raw = None

if uploaded_file is not None:
    df_raw = load_and_process_dataset(uploaded_file)
    st.sidebar.success(f"✅ Archivo cargado: {uploaded_file.name}")
else:
    if demo_option == "🛒 Abarrotes / Minimarket (Demo)":
        p_mype = "/workspace/artifacts/base_de_datos_mype.xlsx"
        if os.path.exists(p_mype):
            df_raw = load_and_process_dataset(p_mype)
    elif demo_option == "💊 Botica & Farmacia (Demo)":
        p_botica = "/workspace/artifacts/base_de_datos_botica.xlsx"
        if os.path.exists(p_botica):
            df_raw = load_and_process_dataset(p_botica)
    elif demo_option == "🍾 Licorería & Licores (Demo)":
        p_licor = "/workspace/artifacts/base_de_datos_licoreria.xlsx"
        if os.path.exists(p_licor):
            df_raw = load_and_process_dataset(p_licor)

# Fallback si no se encontró archivo
if df_raw is None or len(df_raw) == 0:
    p_fallback = "/workspace/scratch/dataset_mype_transacciones.csv"
    if os.path.exists(p_fallback):
        df_raw = load_and_process_dataset(p_fallback)
    else:
        dates = pd.date_range('2026-08-01', periods=100, freq='h')
        df_raw = pd.DataFrame({
            'ID_Transaccion': [f'TX-{i}' for i in range(100)],
            'Fecha': dates,
            'Dia_Semana': dates.day_name(),
            'Producto': np.random.choice(['Producto A', 'Producto B', 'Producto C'], 100),
            'Categoria': np.random.choice(['Categoría 1', 'Categoría 2'], 100),
            'Canal_Venta': np.random.choice(['Tienda Física', 'WhatsApp', 'Yape / Plin'], 100),
            'Cantidad': np.random.randint(1, 5, 100),
            'Precio_Unitario': 15.0,
            'Ventas_Soles': 30.0,
            'Costo_Soles': 18.0,
            'Utilidad_Soles': 12.0
        })

# ---------------------------------------------------------
# 6. FILTROS INTERACTIVOS
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='font-size: 14px; font-weight: 700;'>🔍 FILTROS COMERCIALES</h3>", unsafe_allow_html=True)

periodo_opt = st.sidebar.selectbox(
    "Periodo de Análisis:",
    ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Registro"]
)

max_date = df_raw['Fecha'].max()
if pd.isnull(max_date):
    max_date = pd.to_datetime("2026-09-12")

if periodo_opt == "Últimos 30 días":
    fecha_inicio = max_date - pd.Timedelta(days=30)
    fecha_fin = max_date
elif periodo_opt == "Este Mes":
    fecha_inicio = max_date.replace(day=1)
    fecha_fin = max_date
elif periodo_opt == "Mes Anterior":
    fecha_fin = max_date.replace(day=1) - pd.Timedelta(days=1)
    fecha_inicio = fecha_fin.replace(day=1)
else:
    fecha_inicio = df_raw['Fecha'].min()
    fecha_fin = max_date

categorias_list = ["Todas"] + sorted([str(c) for c in df_raw['Categoria'].dropna().unique()])
cat_sel = st.sidebar.selectbox("Categoría:", categorias_list)

if cat_sel != "Todas":
    df_sub = df_raw[df_raw['Categoria'] == cat_sel]
else:
    df_sub = df_raw

canales_list = ["Todos"] + sorted([str(c) for c in df_sub['Canal_Venta'].dropna().unique()])
canal_sel = st.sidebar.selectbox("Canal de Venta:", canales_list)

# Aplicar filtros
df_curr = df_raw[(df_raw['Fecha'] >= fecha_inicio) & (df_raw['Fecha'] <= fecha_fin)]
if cat_sel != "Todas":
    df_curr = df_curr[df_curr['Categoria'] == cat_sel]
if canal_sel != "Todos":
    df_curr = df_curr[df_curr['Canal_Venta'] == canal_sel]

days_span = (fecha_fin - fecha_inicio).days + 1
fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
fecha_inicio_prev = fecha_fin_prev - pd.Timedelta(days=days_span)

df_prev = df_raw[(df_raw['Fecha'] >= fecha_inicio_prev) & (df_raw['Fecha'] <= fecha_fin_prev)]
if cat_sel != "Todas":
    df_prev = df_prev[df_prev['Categoria'] == cat_sel]
if canal_sel != "Todos":
    df_prev = df_prev[df_prev['Canal_Venta'] == canal_sel]

# ---------------------------------------------------------
# 7. CABECERA PRINCIPAL Y BIENVENIDA
# ---------------------------------------------------------
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<h1 style='font-family: Space Grotesk, sans-serif; font-size: 32px; font-weight: 700; color: #0B1220; margin-bottom: 2px;'>¡Hola, Milagros!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 15px; color: #6B7280; margin-bottom: 25px;'>Aquí tienes el resumen ejecutivo del rendimiento comercial de tu negocio.</p>", unsafe_allow_html=True)

with col_head2:
    st.markdown(f"<div style='text-align: right; background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 10px 16px; border-radius: 12px; font-size: 13px; font-weight: 600; color: #0B1220;'>📅 {fecha_inicio.strftime("%d %b")} – {fecha_fin.strftime("%d %b %Y")}</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 8. CÁLCULO DE KPIs
# ---------------------------------------------------------
vtas_curr = df_curr['Ventas_Soles'].sum()
vtas_prev = df_prev['Ventas_Soles'].sum()
delta_vtas = ((vtas_curr - vtas_prev) / vtas_prev * 100) if vtas_prev > 0 else 0.0

util_curr = df_curr['Utilidad_Soles'].sum()
util_prev = df_prev['Utilidad_Soles'].sum()

cant_curr = df_curr['Cantidad'].sum()
cant_prev = df_prev['Cantidad'].sum()
delta_cant = ((cant_curr - cant_prev) / cant_prev * 100) if cant_prev > 0 else 0.0

num_tx_curr = len(df_curr)
num_tx_prev = len(df_prev)
delta_tx = ((num_tx_curr - num_tx_prev) / num_tx_prev * 100) if num_tx_prev > 0 else 0.0

rent_curr = (util_curr / vtas_curr * 100) if vtas_curr > 0 else 0.0
rent_prev = (util_prev / vtas_prev * 100) if vtas_prev > 0 else 0.0
delta_rent = rent_curr - rent_prev

# 4 TARJETAS KPI
kcol1, kcol2, kcol3, kcol4 = st.columns(4)

with kcol1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🛒 Ventas Totales</div>
        <div class="metric-value">S/ {vtas_curr:,.2f}</div>
        <div class="{'metric-delta-pos' if delta_vtas>=0 else 'metric-delta-neg'}">
            {'▲' if delta_vtas>=0 else '▼'} {abs(delta_vtas):.1f}% vs. periodo ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

with kcol2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📦 Productos Vendidos</div>
        <div class="metric-value">{cant_curr:,.0f} un.</div>
        <div class="{'metric-delta-pos' if delta_cant>=0 else 'metric-delta-neg'}">
            {'▲' if delta_cant>=0 else '▼'} {abs(delta_cant):.1f}% vs. periodo ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

with kcol3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">👤 Transacciones Atendidas</div>
        <div class="metric-value">{num_tx_curr:,} tx</div>
        <div class="{'metric-delta-pos' if delta_tx>=0 else 'metric-delta-neg'}">
            {'▲' if delta_tx>=0 else '▼'} {abs(delta_tx):.1f}% vs. periodo ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

with kcol4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 Rentabilidad Neta</div>
        <div class="metric-value">{rent_curr:.1f}%</div>
        <div class="{'metric-delta-pos' if delta_rent>=0 else 'metric-delta-neg'}">
            {'▲' if delta_rent>=0 else '▼'} {abs(delta_rent):.1f} pp vs. periodo ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 9. LAS 6 PESTAÑAS NAVEGABLES
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "01. Inicio", "02. Ventas", "03. Productos", "04. Rentabilidad", "05. Análisis", "06. Simulador"
])

# --- TAB 1: INICIO ---
with tab1:
    gcol1, gcol2 = st.columns([1.8, 1.2])
    
    with gcol1:
        st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Evolución Diaria de Ventas (S/)</h3>", unsafe_allow_html=True)
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)['Ventas_Soles'].sum().reset_index()
        
        fig_evo = px.area(
            df_daily, x='Fecha', y='Ventas_Soles',
            labels={'Ventas_Soles': 'Ventas (S/)', 'Fecha': 'Día'},
            color_discrete_sequence=['#00C2D1']
        )
        fig_evo.update_traces(line=dict(width=3), fillcolor='rgba(0,194,209,0.12)')
        fig_evo.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickfont=dict(color='#6B7280', size=11)),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7280', size=11))
        )
        st.plotly_chart(fig_evo, use_container_width=True)

    with gcol2:
        st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Ventas por Categoría</h3>", unsafe_allow_html=True)
        df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        
        fig_pie = px.pie(
            df_cat, values='Ventas_Soles', names='Categoria', hole=0.6,
            color_discrete_sequence=['#00C2D1', '#6C5CE7', '#10B981', '#F59E0B', '#3B82F6', '#8B5CF6']
        )
        fig_pie.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
        fig_pie.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    col_b1, col_b2, col_b3 = st.columns([1.2, 1, 1])
    
    with col_b1:
        st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Top 5 Productos Estrella (S/)</h3>", unsafe_allow_html=True)
        df_top5 = df_curr.groupby('Producto')['Ventas_Soles'].sum().reset_index().sort_values('Ventas_Soles', ascending=True).tail(5)
        
        fig_top = px.bar(df_top5, x='Ventas_Soles', y='Producto', orientation='h', color_discrete_sequence=['#0E1B2E'])
        fig_top.update_traces(marker_color='#0E1B2E', marker_line=dict(color='#00C2D1', width=1.5))
        fig_top.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7280')),
            yaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11))
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col_b2:
        st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>Canales de Venta</h3>", unsafe_allow_html=True)
        df_chan = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
        fig_chan = px.bar(df_chan, x='Canal_Venta', y='Ventas_Soles', color_discrete_sequence=['#6C5CE7'])
        fig_chan.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11)),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7280'))
        )
        st.plotly_chart(fig_chan, use_container_width=True)

    with col_b3:
        st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 12px;'>💡 Alertas y Oportunidades</h3>", unsafe_allow_html=True)
        top_prod = df_top5.iloc[-1]['Producto'] if len(df_top5) > 0 else "Producto Clave"
        st.info(f"🚨 **Demanda Elevada:** El producto **{top_prod}** representa la mayor contribución de ingresos del periodo.")
        st.success("🎯 **Oportunidad Comercial:** Incrementar stock los jueves para cubrir la alta demanda proyectada del fin de semana.")

# --- TAB 2: VENTAS ---
with tab2:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 18px; font-weight: 700; color: #0B1220;'>Análisis Detallado de Ventas</h3>", unsafe_allow_html=True)
    vcol1, vcol2 = st.columns(2)
    
    with vcol1:
        st.markdown("##### Ventas por Día de la Semana")
        df_dow = df_curr.groupby('Dia_Semana')['Ventas_Soles'].sum().reset_index()
        fig_dow = px.bar(df_dow, x='Dia_Semana', y='Ventas_Soles', color_discrete_sequence=['#00C2D1'])
        fig_dow.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_dow, use_container_width=True)
        
    with vcol2:
        st.markdown("##### Distribución de Monto por Ticket (Histograma)")
        fig_hist = px.histogram(df_curr, x='Ventas_Soles', nbins=15, color_discrete_sequence=['#6C5CE7'])
        fig_hist.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("##### Registro de Transacciones Filtradas")
    st.dataframe(df_curr[['ID_Transaccion', 'Fecha', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Precio_Unitario', 'Ventas_Soles', 'Utilidad_Soles']], use_container_width=True)

# --- TAB 3: PRODUCTOS ---
with tab3:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 18px; font-weight: 700; color: #0B1220;'>Rendimiento de Productos</h3>", unsafe_allow_html=True)
    pcol1, pcol2 = st.columns(2)
    
    with pcol1:
        st.markdown("##### Top 10 Productos por Facturación (S/ )")
        df_p_rev = df_curr.groupby('Producto')['Ventas_Soles'].sum().reset_index().sort_values('Ventas_Soles', ascending=True).tail(10)
        fig_p_rev = px.bar(df_p_rev, x='Ventas_Soles', y='Producto', orientation='h', color_discrete_sequence=['#00C2D1'])
        fig_p_rev.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p_rev, use_container_width=True)
        
    with pcol2:
        st.markdown("##### Top 10 Productos por Volumen (Unidades)")
        df_p_qty = df_curr.groupby('Producto')['Cantidad'].sum().reset_index().sort_values('Cantidad', ascending=True).tail(10)
        fig_p_qty = px.bar(df_p_qty, x='Cantidad', y='Producto', orientation='h', color_discrete_sequence=['#10B981'])
        fig_p_qty.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p_qty, use_container_width=True)

# --- TAB 4: RENTABILIDAD ---
with tab4:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 18px; font-weight: 700; color: #0B1220;'>Análisis de Margen y Rentabilidad</h3>", unsafe_allow_html=True)
    rcol1, rcol2 = st.columns(2)
    
    with rcol1:
        st.markdown("##### Margen de Ganancia (%) por Categoría")
        df_r_cat = df_curr.groupby('Categoria').apply(lambda x: (x['Utilidad_Soles'].sum() / x['Ventas_Soles'].sum() * 100) if x['Ventas_Soles'].sum() > 0 else 0).reset_index(name='Margen_%')
        fig_r_cat = px.bar(df_r_cat, x='Categoria', y='Margen_%', color_discrete_sequence=['#F59E0B'])
        fig_r_cat.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_r_cat, use_container_width=True)
        
    with rcol2:
        st.markdown("##### Matriz Ventas vs. Utilidad por Producto")
        df_p_scat = df_curr.groupby('Producto')[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
        fig_scat = px.scatter(df_p_scat, x='Ventas_Soles', y='Utilidad_Soles', text='Producto', color_discrete_sequence=['#6C5CE7'])
        fig_scat.update_traces(marker=dict(size=12))
        fig_scat.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scat, use_container_width=True)

# --- TAB 5: ANÁLISIS ---
with tab5:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 18px; font-weight: 700; color: #0B1220;'>Inteligencia de Negocio Avanzada</h3>", unsafe_allow_html=True)
    
    st.markdown("##### Mapa de Calor: Ventas por Canal vs. Categoría")
    df_pv = df_curr.pivot_table(index='Categoria', columns='Canal_Venta', values='Ventas_Soles', aggfunc='sum', fill_value=0)
    fig_heat = px.imshow(df_pv, color_continuous_scale='Blues')
    fig_heat.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heat, use_container_width=True)

# --- TAB 6: SIMULADOR ---
with tab6:
    st.markdown("<h3 style='font-family: Space Grotesk, sans-serif; font-size: 18px; font-weight: 700; color: #0B1220;'>Calculadora y Simulador Financiero MYPE</h3>", unsafe_allow_html=True)
    st.markdown("Ajusta las variables comerciales para simular el impacto en la Utilidad Neta mensual de tu negocio.")
    
    scol1, scol2 = st.columns([1, 1.5])
    
    with scol1:
        var_precio = st.slider("Aumento / Descuento de Precios (%):", -20, 30, 5)
        var_volumen = st.slider("Variación Estimada de Volumen (%):", -30, 50, 10)
        var_costo = st.slider("Variación en Costos de Proveedor (%):", -15, 20, 2)
        inv_mkt = st.slider("Inversión en Publicidad / Delivery (S/):", 0, 1000, 150)

    with scol2:
        vtas_base = vtas_curr
        costos_base = df_curr['Costo_Soles'].sum()
        util_base = util_curr
        
        vtas_sim = vtas_base * (1 + var_precio/100) * (1 + var_volumen/100)
        costos_sim = costos_base * (1 + var_costo/100) * (1 + var_volumen/100) + inv_mkt
        util_sim = vtas_sim - costos_sim
        diff_util = util_sim - util_base
        
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
            <h4 style="margin-0; color: #6B7280; font-size: 13px; font-weight: 700;">PROYECCIÓN DE UTILIDAD NETA SIMULADA</h4>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 700; color: #0B1220; margin: 8px 0;">
                S/ {util_sim:,.2f}
            </div>
            <div style="font-size: 14px; font-weight: 700; color: {'#059669' if diff_util>=0 else '#DC2626'};">
                {'▲ +' if diff_util>=0 else '▼ '} S/ {abs(diff_util):,.2f} vs. estado actual
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        df_sim_comp = pd.DataFrame({
            'Escenario': ['Actual', 'Simulado'],
            'Ventas': [vtas_base, vtas_sim],
            'Utilidad': [util_base, util_sim]
        })
        fig_sim = px.bar(df_sim_comp, x='Escenario', y=['Ventas', 'Utilidad'], barmode='group', color_discrete_sequence=['#00C2D1', '#10B981'])
        fig_sim.update_layout(height=240, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sim, use_container_width=True)

st.markdown("---")
st.caption("NexData MYPE v2.5 – Plataforma de Inteligencia Comercial y Gestión por Resultados 2026")
