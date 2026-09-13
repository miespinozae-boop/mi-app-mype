import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y FAVICON NEXDATA
# ---------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<rect width="100" height="100" rx="20" fill="#0E1B2E"/>
<path d="M 20 75 L 45 45 L 65 60 L 85 25" fill="none" stroke="#00C2D1" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="20" cy="75" r="6" fill="#00C2D1"/>
<circle cx="45" cy="45" r="6" fill="#00C2D1"/>
<circle cx="65" cy="60" r="6" fill="#00C2D1"/>
<polygon points="85,20 75,32 90,32" fill="#6C5CE7"/>
</svg>"""

st.set_page_config(
    page_title="NexData – Panel MYPE de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección del Favicon SVG en el navegador
favicon_encoded = FAVICON_SVG.replace('#', '%23').replace('\n', '').replace('"', "'")
st.markdown(
    f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;utf8,{favicon_encoded}">',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# 2. ESTILOS CSS - REGLA ESTRICTA: CERO TEXTO BLANCO SOBRE FONDO CLARO
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F4F7FA;
        color: #0B1220;
    }
    
    .stApp {
        background-color: #F4F7FA;
    }

    /* BARRA LATERAL OSCURA */
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
    
    /* ENCABEZADOS PRINCIPALES */
    .app-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 2px;
    }
    .app-subtitle {
        font-size: 14px;
        color: #6B7686;
        margin-bottom: 20px;
    }

    /* TARJETAS KPI PREMIUN */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 16px;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .kpi-title {
        font-size: 12px;
        font-weight: 700;
        color: #6B7686;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-icon-box {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #0B1220;
        margin-bottom: 6px;
    }
    .kpi-delta-pos {
        font-size: 12px;
        font-weight: 700;
        color: #059669;
        background-color: #ECFDF5;
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-block;
    }
    .kpi-delta-neg {
        font-size: 12px;
        font-weight: 700;
        color: #DC2626;
        background-color: #FEF2F2;
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-block;
    }

    /* RECUADROS DE ALERTAS */
    .alert-box-info {
        background-color: #EFF6FF;
        border-left: 4px solid #0284C7;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
        color: #0B1220;
    }
    .alert-box-warning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
        color: #0B1220;
    }
    .alert-title {
        font-weight: 700;
        font-size: 14px;
        color: #0B1220;
        margin-bottom: 4px;
    }
    .alert-desc {
        font-size: 13px;
        color: #334155;
    }

    /* PESTAÑAS STYLED */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #E2E8F0;
        padding: 4px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        border-radius: 8px;
        color: #475569 !important;
        font-weight: 600;
        font-size: 13px;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #0B1220 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. CARGADOR INTELIGENTE MULTI-FORMATO (EXCEL / CSV)
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_and_process_dataset(file_or_path):
    """
    Carga cualquier archivo Excel (.xlsx, .xls) o CSV,
    identifica automáticamente la hoja de transacciones y calcula campos faltantes.
    """
    try:
        if isinstance(file_or_path, str):
            if file_or_path.endswith('.csv'):
                df_raw = pd.read_csv(file_or_path)
            else:
                xl = pd.ExcelFile(file_or_path)
                best_sheet = _find_best_sheet(xl)
                df_raw = pd.read_excel(file_or_path, sheet_name=best_sheet)
        else:
            fname = file_or_path.name.lower()
            if fname.endswith('.csv'):
                df_raw = pd.read_csv(file_or_path)
            else:
                xl = pd.ExcelFile(file_or_path)
                best_sheet = _find_best_sheet(xl)
                df_raw = pd.read_excel(file_or_path, sheet_name=best_sheet)
        
        return standardize_dataset(df_raw)
    except Exception as e:
        st.error(f"Error al procesar la base de datos: {e}")
        return None

def _find_best_sheet(xl_file):
    sheets = xl_file.sheet_names
    if len(sheets) == 1:
        return sheets[0]
    
    keywords = ['transacc', 'base', 'data', 'ventas', 'detalle', 'registro', 'movimiento', 'sales']
    for s in sheets:
        if any(k in s.lower() for k in keywords):
            return s
            
    best_sheet = sheets[0]
    max_score = -1
    for s in sheets:
        try:
            df = xl_file.parse(s, nrows=15)
            score = df.shape[0] * df.shape[1]
            cols_str = " ".join([str(c).lower() for c in df.columns])
            if any(k in cols_str for k in ['fecha', 'venta', 'producto', 'monto', 'total', 'precio']):
                score += 100
            if score > max_score:
                max_score = score
                best_sheet = s
        except Exception:
            pass
    return best_sheet

def standardize_dataset(df):
    df = df.copy()
    col_mapping = {}
    
    for col in df.columns:
        c_clean = str(col).strip().lower().replace('_', ' ').replace('(s/)', '').replace('soles', '').replace('unit.', 'unitario')
        c_clean = c_clean.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        
        if any(k in c_clean for k in ['id trans', 'ticket', 'codigo', 'nro_tx', 'id_tx']):
            col_mapping[col] = 'ID_Transaccion'
        elif any(k in c_clean for k in ['fecha', 'date', 'fec', 'dia venta']):
            col_mapping[col] = 'Fecha'
        elif any(k in c_clean for k in ['dia semana', 'dia_semana', 'weekday']):
            col_mapping[col] = 'Dia_Semana'
        elif any(k in c_clean for k in ['producto', 'item', 'descripcion', 'product', 'articulo']):
            col_mapping[col] = 'Producto'
        elif any(k in c_clean for k in ['categoria', 'familia', 'linea', 'rubro', 'category']):
            col_mapping[col] = 'Categoria'
        elif any(k in c_clean for k in ['canal', 'channel', 'medio', 'forma pago']):
            col_mapping[col] = 'Canal_Venta'
        elif any(k in c_clean for k in ['cantidad', 'qty', 'unidades', 'cant']):
            col_mapping[col] = 'Cantidad'
        elif any(k in c_clean for k in ['precio unit', 'precio', 'price', 'p.unit']):
            col_mapping[col] = 'Precio_Unitario'
        elif any(k in c_clean for k in ['ventas', 'monto', 'total', 'ingreso', 'revenue', 'importe']):
            col_mapping[col] = 'Ventas_Soles'
        elif any(k in c_clean for k in ['costo', 'cost', 'egreso']):
            col_mapping[col] = 'Costo_Soles'
        elif any(k in c_clean for k in ['utilidad', 'ganancia', 'profit', 'lucro', 'margen soles']):
            col_mapping[col] = 'Utilidad_Soles'

    df.rename(columns=col_mapping, inplace=True)
    
    # Procesar Fecha
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        df = df.dropna(subset=['Fecha'])
    else:
        df['Fecha'] = pd.date_range(end=pd.Timestamp.now(), periods=len(df), freq='D')
        
    # Cantidad y Precio Unitario
    if 'Cantidad' in df.columns:
        df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce').fillna(1).astype(int)
    else:
        df['Cantidad'] = 1

    if 'Precio_Unitario' in df.columns:
        df['Precio_Unitario'] = pd.to_numeric(df['Precio_Unitario'], errors='coerce').fillna(10.0)
    else:
        df['Precio_Unitario'] = 10.0

    # Ventas_Soles: calcular si es NaN o 0
    if 'Ventas_Soles' in df.columns:
        df['Ventas_Soles'] = pd.to_numeric(df['Ventas_Soles'], errors='coerce')
        df['Ventas_Soles'] = df['Ventas_Soles'].fillna(df['Cantidad'] * df['Precio_Unitario'])
        df['Ventas_Soles'] = np.where(df['Ventas_Soles'] == 0, df['Cantidad'] * df['Precio_Unitario'], df['Ventas_Soles'])
    else:
        df['Ventas_Soles'] = df['Cantidad'] * df['Precio_Unitario']

    # Costo_Soles
    if 'Costo_Soles' in df.columns:
        df['Costo_Soles'] = pd.to_numeric(df['Costo_Soles'], errors='coerce').fillna(df['Ventas_Soles'] * 0.65)
    else:
        df['Costo_Soles'] = df['Ventas_Soles'] * 0.65

    # Utilidad_Soles: calcular si es NaN
    if 'Utilidad_Soles' in df.columns:
        df['Utilidad_Soles'] = pd.to_numeric(df['Utilidad_Soles'], errors='coerce')
        df['Utilidad_Soles'] = df['Utilidad_Soles'].fillna(df['Ventas_Soles'] - df['Costo_Soles'])
    else:
        df['Utilidad_Soles'] = df['Ventas_Soles'] - df['Costo_Soles']

    if 'Producto' not in df.columns:
        df['Producto'] = "Producto " + df.index.astype(str)

    if 'Categoria' not in df.columns:
        df['Categoria'] = "General"

    if 'Canal_Venta' not in df.columns:
        df['Canal_Venta'] = "Tienda Física"

    if 'Dia_Semana' not in df.columns or df['Dia_Semana'].isnull().any():
        dias_es = {'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 
                   'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
        df['Dia_Semana'] = df['Fecha'].dt.day_name().map(dias_es).fillna('Lunes')

    if 'ID_Transaccion' not in df.columns:
        df['ID_Transaccion'] = ["TX-" + str(1001 + i) for i in range(len(df))]

    return df

# ---------------------------------------------------------
# 4. BARRA LATERAL (LOGO, LOGICA DE CARGA Y FILTROS)
# ---------------------------------------------------------
# Logo NexData SVG
st.sidebar.markdown("""
<div style="text-align: left; padding: 10px 0 20px 0;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 36px; height: 36px; background-color: #0E1B2E; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px solid #1E2D42;">
            <svg width="24" height="24" viewBox="0 0 100 100">
                <path d="M 20 75 L 45 45 L 65 60 L 85 25" fill="none" stroke="#00C2D1" stroke-width="10" stroke-linecap="round"/>
                <circle cx="20" cy="75" r="8" fill="#00C2D1"/>
                <circle cx="45" cy="45" r="8" fill="#00C2D1"/>
                <circle cx="65" cy="60" r="8" fill="#00C2D1"/>
                <polygon points="85,18 73,32 90,32" fill="#6C5CE7"/>
            </svg>
        </div>
        <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; color: #FFFFFF; line-height: 1;">
                Nex<span style="color: #00C2D1;">Data</span>
            </div>
            <div style="font-size: 10px; color: #8C9BAE; margin-top: 2px;">Datos claros para tu negocio</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📂 Carga de Datos")

uploaded_file = st.sidebar.file_uploader(
    "Subir Base de Datos Excel (.xlsx) o CSV:",
    type=["xlsx", "xls", "csv"],
    help="Sube tu propio archivo Excel o CSV para analizar los datos de tu negocio al instante."
)

df_raw = None
source_name = ""

if uploaded_file is not None:
    df_raw = load_and_process_dataset(uploaded_file)
    source_name = uploaded_file.name
else:
    # Opción de selección de Demos integradas
    demo_opt = st.sidebar.selectbox(
        "O seleccionar Negocio de Ejemplo (Demo):",
        ["🛒 Minimarket / Abarrotes", "💊 Botica / Farmacia"]
    )
    if "Minimarket" in demo_opt:
        df_raw = load_and_process_dataset('/workspace/artifacts/base_de_datos_mype.xlsx')
        source_name = "Minimarket (base_de_datos_mype.xlsx)"
    else:
        df_raw = load_and_process_dataset('/workspace/artifacts/base_de_datos_botica.xlsx')
        source_name = "Botica San Martín (base_de_datos_botica.xlsx)"

if df_raw is not None and not df_raw.empty:
    st.sidebar.markdown(f"""
    <div style="background-color: #16263B; border-left: 3px solid #00C2D1; padding: 10px 12px; border-radius: 6px; font-size: 11px; margin-bottom: 20px;">
        <div style="color: #00C2D1; font-weight: 700;">✅ DATA ACTIVA</div>
        <div style="color: #FFFFFF; font-weight: 600;">{source_name}</div>
        <div style="color: #8C9BAE;">{len(df_raw):,} registros cargados</div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # FILTROS DINÁMICOS
    # ---------------------------------------------------------
    st.sidebar.markdown("### 🔍 Filtros de Negocio")

    max_date = df_raw['Fecha'].max()
    min_date = df_raw['Fecha'].min()

    periodo_opt = st.sidebar.selectbox(
        "Seleccionar Periodo:",
        ["Últimos 30 días", "Últimos 60 días", "Todo el Registro"]
    )

    if periodo_opt == "Últimos 30 días":
        fecha_inicio = max_date - pd.Timedelta(days=30)
        fecha_fin = max_date
        fecha_inicio_prev = fecha_inicio - pd.Timedelta(days=30)
        fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    elif periodo_opt == "Últimos 60 días":
        fecha_inicio = max_date - pd.Timedelta(days=60)
        fecha_fin = max_date
        fecha_inicio_prev = fecha_inicio - pd.Timedelta(days=60)
        fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    else:
        fecha_inicio = min_date
        fecha_fin = max_date
        fecha_inicio_prev = min_date
        fecha_fin_prev = max_date

    # Filtro Categoría
    cats = ["Todas"] + sorted(list(df_raw['Categoria'].dropna().unique()))
    cat_sel = st.sidebar.selectbox("Categoría de Producto:", cats)

    # Filtro Producto
    if cat_sel != "Todas":
        prods = ["Todos"] + sorted(list(df_raw[df_raw['Categoria'] == cat_sel]['Producto'].dropna().unique()))
    else:
        prods = ["Todos"] + sorted(list(df_raw['Producto'].dropna().unique()))
    prod_sel = st.sidebar.selectbox("Producto Específico:", prods)

    # Filtro Canal
    canales = ["Todos"] + sorted(list(df_raw['Canal_Venta'].dropna().unique()))
    canal_sel = st.sidebar.selectbox("Canal de Venta:", canales)

    # Aplicar filtros
    def filtrar_data(df, f_ini, f_fin, cat, prod, canal):
        df_f = df[(df['Fecha'] >= f_ini) & (df['Fecha'] <= f_fin)]
        if cat != "Todas":
            df_f = df_f[df_f['Categoria'] == cat]
        if prod != "Todos":
            df_f = df_f[df_f['Producto'] == prod]
        if canal != "Todos":
            df_f = df_f[df_f['Canal_Venta'] == canal]
        return df_f

    df_curr = filtrar_data(df_raw, fecha_inicio, fecha_fin, cat_sel, prod_sel, canal_sel)
    df_prev = filtrar_data(df_raw, fecha_inicio_prev, fecha_fin_prev, cat_sel, prod_sel, canal_sel)

    # ---------------------------------------------------------
    # CÁLCULO DE KPIs
    # ---------------------------------------------------------
    vtas_curr = df_curr['Ventas_Soles'].sum()
    vtas_prev = df_prev['Ventas_Soles'].sum()
    delta_vtas = ((vtas_curr - vtas_prev) / vtas_prev * 100) if vtas_prev > 0 else 0.0

    util_curr = df_curr['Utilidad_Soles'].sum()
    util_prev = df_prev['Utilidad_Soles'].sum()
    delta_util = ((util_curr - util_prev) / util_prev * 100) if util_prev > 0 else 0.0

    mg_curr = (util_curr / vtas_curr * 100) if vtas_curr > 0 else 0.0
    mg_prev = (util_prev / vtas_prev * 100) if vtas_prev > 0 else 0.0
    delta_mg = mg_curr - mg_prev

    num_tx_curr = len(df_curr)
    num_tx_prev = len(df_prev)
    delta_tx = ((num_tx_curr - num_tx_prev) / num_tx_prev * 100) if num_tx_prev > 0 else 0.0

    units_curr = df_curr['Cantidad'].sum()
    units_prev = df_prev['Cantidad'].sum()
    delta_units = ((units_curr - units_prev) / units_prev * 100) if units_prev > 0 else 0.0

    # ---------------------------------------------------------
    # ENCABEZADO Y ENTORNO DE TRABAJO
    # ---------------------------------------------------------
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
        <div>
            <div class="app-title">¡Hola, Milagros!</div>
            <div class="app-subtitle">Aquí tienes un resumen del rendimiento de tu negocio basado en la data cargada.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PESTAÑAS PRINCIPALES DEL SISTEMA
    # ---------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "01. Inicio", 
        "02. Ventas", 
        "03. Productos", 
        "04. Rentabilidad", 
        "05. Análisis", 
        "06. Simulador MYPE"
    ])

    # ---------------------------------------------------------
    # TAB 1: INICIO (DASHBOARD EJECUTIVO RÉPLICA APP)
    # ---------------------------------------------------------
    with tab1:
        # Fila de 4 Tarjetas KPI
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-title">Ventas Totales</div>
                    <div class="kpi-icon-box" style="background-color: #E0F2FE; color: #0284C7;">🛒</div>
                </div>
                <div class="kpi-value">S/ {vtas_curr:,.2f}</div>
                <div>
                    <span class="{'kpi-delta-pos' if delta_vtas >= 0 else 'kpi-delta-neg'}">
                        {'▲' if delta_vtas >= 0 else '▼'} {abs(delta_vtas):.1f}% vs. ant.
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-title">Productos Vendidos</div>
                    <div class="kpi-icon-box" style="background-color: #F3E8FF; color: #7C3AED;">📦</div>
                </div>
                <div class="kpi-value">{units_curr:,} un.</div>
                <div>
                    <span class="{'kpi-delta-pos' if delta_units >= 0 else 'kpi-delta-neg'}">
                        {'▲' if delta_units >= 0 else '▼'} {abs(delta_units):.1f}% vs. ant.
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-title">Transacciones</div>
                    <div class="kpi-icon-box" style="background-color: #ECFDF5; color: #059669;">👤</div>
                </div>
                <div class="kpi-value">{num_tx_curr:,} tx.</div>
                <div>
                    <span class="{'kpi-delta-pos' if delta_tx >= 0 else 'kpi-delta-neg'}">
                        {'▲' if delta_tx >= 0 else '▼'} {abs(delta_tx):.1f}% vs. ant.
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-title">Rentabilidad Neta</div>
                    <div class="kpi-icon-box" style="background-color: #FEF3C7; color: #D97706;">💰</div>
                </div>
                <div class="kpi-value">{mg_curr:.1f}%</div>
                <div>
                    <span class="{'kpi-delta-pos' if delta_mg >= 0 else 'kpi-delta-neg'}">
                        {'▲' if delta_mg >= 0 else '▼'} {abs(delta_mg):.1f} pp vs. ant.
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Fila Central de Gráficos (Evolución Diaria + Donut Categoría)
        col_g1, col_g2 = st.columns([1.6, 1])

        with col_g1:
            st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;">Evolución de Ventas Diarias (S/)</div>', unsafe_allow_html=True)
            df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)['Ventas_Soles'].sum().reset_index()
            
            fig_evo = go.Figure()
            fig_evo.add_trace(go.Scatter(
                x=df_daily['Fecha'],
                y=df_daily['Ventas_Soles'],
                mode='lines+markers',
                line=dict(color='#0284C7', width=3, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(2, 132, 199, 0.08)',
                marker=dict(size=6, color='#0284C7'),
                name='Ventas (S/)'
            ))
            fig_evo.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=10, b=20),
                height=300,
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11)),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11), title=dict(text="Soles (S/)", font=dict(color='#0B1220', size=11)))
            )
            st.plotly_chart(fig_evo, use_container_width=True)

        with col_g2:
            st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 16px; font-weight: 700; color: #0B1220; margin-bottom: 10px;">Ventas por Categoría</div>', unsafe_allow_html=True)
            df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
            
            colors_list = ['#00C2D1', '#6C5CE7', '#0284C7', '#10B981', '#F59E0B', '#EC4899', '#8B5CF6']
            fig_donut = go.Figure(go.Pie(
                labels=df_cat['Categoria'],
                values=df_cat['Ventas_Soles'],
                hole=0.6,
                marker=dict(colors=colors_list),
                textinfo='percent',
                insidetextfont=dict(color='#FFFFFF', size=11)
            ))
            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=300,
                legend=dict(font=dict(color='#0B1220', size=11), orientation="v", y=0.5),
                annotations=[dict(text=f"S/ {vtas_curr:,.0f}", x=0.5, y=0.5, font_size=16, font_family="Space Grotesk", font_color="#0B1220", showarrow=False)]
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # Fila Inferior (Top 5 + Canales + Alertas)
        col_b1, col_b2, col_b3 = st.columns([1, 1, 1.2])

        with col_b1:
            st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 15px; font-weight: 700; color: #0B1220; margin-bottom: 8px;">Top 5 Productos Vendidos</div>', unsafe_allow_html=True)
            df_top5 = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(5).reset_index()
            
            fig_top5 = go.Figure(go.Bar(
                x=df_top5['Ventas_Soles'],
                y=df_top5['Producto'],
                orientation='h',
                marker=dict(color='#00C2D1', cornerradius=4),
                text=[f"S/ {v:,.0f}" for v in df_top5['Ventas_Soles']],
                textposition='outside',
                textfont=dict(color='#0B1220', size=11)
            ))
            fig_top5.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=40, t=10, b=10),
                height=260,
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11))
            )
            st.plotly_chart(fig_top5, use_container_width=True)

        with col_b2:
            st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 15px; font-weight: 700; color: #0B1220; margin-bottom: 8px;">Ventas por Canal</div>', unsafe_allow_html=True)
            df_chan = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
            
            fig_chan = go.Figure(go.Pie(
                labels=df_chan['Canal_Venta'],
                values=df_chan['Ventas_Soles'],
                hole=0.4,
                marker=dict(colors=['#0E1B2E', '#00C2D1', '#6C5CE7', '#10B981']),
                textinfo='percent+label',
                textposition='outside',
                textfont=dict(color='#0B1220', size=10)
            ))
            fig_chan.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=260,
                showlegend=False
            )
            st.plotly_chart(fig_chan, use_container_width=True)

        with col_b3:
            st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 15px; font-weight: 700; color: #0B1220; margin-bottom: 8px;">Detección Automática de Oportunidades</div>', unsafe_allow_html=True)
            
            if not df_curr.empty:
                top_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().idxmax()
                top_chan = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().idxmax()
                
                st.markdown(f"""
                <div class="alert-box-info">
                    <div class="alert-title">🚀 Línea Comercial Principal: {top_cat}</div>
                    <div class="alert-desc">Representa la mayor concentración de ingresos del negocio. Mantener stock garantizado.</div>
                </div>
                <div class="alert-box-warning">
                    <div class="alert-title">📱 Canal Clave: {top_chan}</div>
                    <div class="alert-desc">Concentra la preferencia de compra. Promover promociones y combos por este canal.</div>
                </div>
                """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TAB 2: VENTAS
    # ---------------------------------------------------------
    with tab2:
        st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 18px; font-weight: 700; color: #0B1220; margin-bottom: 15px;">Análisis Detallado de Ventas</div>', unsafe_allow_html=True)
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown('**Ventas por Día de la Semana**')
            order_days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            df_day = df_curr.groupby('Dia_Semana')['Ventas_Soles'].sum().reindex(order_days).fillna(0).reset_index()
            
            fig_day = go.Figure(go.Bar(
                x=df_day['Dia_Semana'],
                y=df_day['Ventas_Soles'],
                marker=dict(color='#0284C7', cornerradius=4),
                text=[f"S/ {v:,.0f}" for v in df_day['Ventas_Soles']],
                textposition='auto',
                textfont=dict(color='#FFFFFF', size=10)
            ))
            fig_day.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=300,
                xaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11)),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11))
            )
            st.plotly_chart(fig_day, use_container_width=True)

        with col_v2:
            st.markdown('**Distribución de Monto por Ticket (Histograma)**')
            fig_hist = go.Figure(go.Histogram(
                x=df_curr['Ventas_Soles'],
                nbinsx=15,
                marker=dict(color='#6C5CE7', line=dict(color='#0E1B2E', width=1))
            ))
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=300,
                xaxis=dict(title=dict(text="Monto del Ticket (S/)", font=dict(color='#0B1220', size=11)), showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11)),
                yaxis=dict(title=dict(text="Frecuencia", font=dict(color='#0B1220', size=11)), showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11))
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown('**Registro de Transacciones Filtradas**')
        st.dataframe(
            df_curr[['ID_Transaccion', 'Fecha', 'Dia_Semana', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Precio_Unitario', 'Ventas_Soles', 'Utilidad_Soles']],
            use_container_width=True,
            hide_index=True
        )

    # ---------------------------------------------------------
    # TAB 3: PRODUCTOS
    # ---------------------------------------------------------
    with tab3:
        st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 18px; font-weight: 700; color: #0B1220; margin-bottom: 15px;">Rendimiento Comercial por Producto</div>', unsafe_allow_html=True)
        
        col_p1, col_v2 = st.columns(2)
        with col_p1:
            st.markdown('**Top 10 Productos por Facturación (S/)**')
            df_p_rev = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()
            fig_p_rev = go.Figure(go.Bar(
                x=df_p_rev['Ventas_Soles'],
                y=df_p_rev['Producto'],
                orientation='h',
                marker=dict(color='#00C2D1', cornerradius=4),
                text=[f"S/ {v:,.0f}" for v in df_p_rev['Ventas_Soles']],
                textposition='outside',
                textfont=dict(color='#0B1220', size=10)
            ))
            fig_p_rev.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=40, t=10, b=10),
                height=350,
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11))
            )
            st.plotly_chart(fig_p_rev, use_container_width=True)

        with col_v2:
            st.markdown('**Top 10 Productos por Volumen (Unidades)**')
            df_p_vol = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()
            fig_p_vol = go.Figure(go.Bar(
                x=df_p_vol['Cantidad'],
                y=df_p_vol['Producto'],
                orientation='h',
                marker=dict(color='#6C5CE7', cornerradius=4),
                text=[f"{v:,} un." for v in df_p_vol['Cantidad']],
                textposition='outside',
                textfont=dict(color='#0B1220', size=10)
            ))
            fig_p_vol.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=40, t=10, b=10),
                height=350,
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11))
            )
            st.plotly_chart(fig_p_vol, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 4: RENTABILIDAD
    # ---------------------------------------------------------
    with tab4:
        st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 18px; font-weight: 700; color: #0B1220; margin-bottom: 15px;">Análisis de Rentabilidad y Margen</div>', unsafe_allow_html=True)
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown('**Margen de Utilidad (%) por Categoría**')
            df_mg_cat = df_curr.groupby('Categoria').apply(
                lambda x: (x['Utilidad_Soles'].sum() / x['Ventas_Soles'].sum() * 100) if x['Ventas_Soles'].sum() > 0 else 0
            ).reset_index(name='Margen_Pct')
            
            fig_mg = go.Figure(go.Bar(
                x=df_mg_cat['Categoria'],
                y=df_mg_cat['Margen_Pct'],
                marker=dict(color='#10B981', cornerradius=4),
                text=[f"{v:.1f}%" for v in df_mg_cat['Margen_Pct']],
                textposition='auto',
                textfont=dict(color='#FFFFFF', size=11)
            ))
            fig_mg.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=320,
                xaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11)),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11), title=dict(text="Margen (%)", font=dict(color='#0B1220', size=11)))
            )
            st.plotly_chart(fig_mg, use_container_width=True)

        with col_r2:
            st.markdown('**Matriz de Dispersión: Ventas vs. Utilidad Neta**')
            df_scat = df_curr.groupby('Producto')[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
            
            fig_scat = go.Figure(go.Scatter(
                x=df_scat['Ventas_Soles'],
                y=df_scat['Utilidad_Soles'],
                mode='markers+text',
                text=df_scat['Producto'],
                textposition='top center',
                textfont=dict(color='#0B1220', size=9),
                marker=dict(size=12, color='#6C5CE7', opacity=0.8)
            ))
            fig_scat.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=320,
                xaxis=dict(title=dict(text="Ventas Totales (S/)", font=dict(color='#0B1220', size=11)), showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11)),
                yaxis=dict(title=dict(text="Utilidad Neta (S/)", font=dict(color='#0B1220', size=11)), showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11))
            )
            st.plotly_chart(fig_scat, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 5: ANÁLISIS
    # ---------------------------------------------------------
    with tab5:
        st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 18px; font-weight: 700; color: #0B1220; margin-bottom: 15px;">Inteligencia Cruzada de Negocio</div>', unsafe_allow_html=True)
        
        st.markdown('**Mapa de Calor: Ventas (S/) por Canal vs. Categoría**')
        df_piv = df_curr.pivot_table(index='Categoria', columns='Canal_Venta', values='Ventas_Soles', aggfunc='sum', fill_value=0)
        
        fig_heat = go.Figure(go.Heatmap(
            z=df_piv.values,
            x=df_piv.columns,
            y=df_piv.index,
            colorscale='Blues',
            texttemplate="S/ %{z:,.0f}",
            textfont=dict(color='#0B1220', size=11)
        ))
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            xaxis=dict(tickfont=dict(color='#0B1220', size=11)),
            yaxis=dict(tickfont=dict(color='#0B1220', size=11))
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 6: SIMULADOR MYPE INTERACTIVO
    # ---------------------------------------------------------
    with tab6:
        st.markdown('<div style="font-family: \'Space Grotesk\', sans-serif; font-size: 18px; font-weight: 700; color: #0B1220; margin-bottom: 10px;">Calculadora y Simulador Financiero MYPE</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 13px; color: #6B7686; margin-bottom: 20px;">Ajusta las variables comerciales para proyectar el impacto en ventas y utilidad en tiempo real.</div>', unsafe_allow_html=True)
        
        col_s1, col_s2 = st.columns([1, 1.5])
        
        with col_s1:
            st.markdown('**Ajuste de Variables Comerciales**')
            var_precio = st.slider("Variación de Precios (%):", -20, 30, 0, step=1)
            var_volumen = st.slider("Variación en Volumen de Ventas (%):", -30, 50, 0, step=5)
            pct_mermas = st.slider("Reducción de Mermas/Pérdidas (%):", 0, 15, 2, step=1)
            inv_mkt = st.number_input("Inversión Adicional en Marketing (S/):", 0, 2000, 150, step=50)

            # Cálculos de Proyección
            fact_precio = 1 + (var_precio / 100.0)
            fact_volumen = 1 + (var_volumen / 100.0)
            
            vtas_proj = vtas_curr * fact_precio * fact_volumen
            costo_base_proj = df_curr['Costo_Soles'].sum() * fact_volumen
            ahorro_mermas = costo_base_proj * (pct_mermas / 100.0)
            costo_final_proj = costo_base_proj - ahorro_mermas + inv_mkt
            util_proj = vtas_proj - costo_final_proj
            
            diff_vtas = vtas_proj - vtas_curr
            diff_util = util_proj - util_curr

        with col_s2:
            st.markdown('**Resultado Proyectado vs. Actual**')
            
            cs1, cs2 = st.columns(2)
            with cs1:
                st.metric("Ventas Proyectadas", f"S/ {vtas_proj:,.2f}", delta=f"S/ {diff_vtas:+,.2f}")
            with cs2:
                st.metric("Utilidad Neta Proyectada", f"S/ {util_proj:,.2f}", delta=f"S/ {diff_util:+,.2f}")
                
            fig_sim = go.Figure(data=[
                go.Bar(name='Actual', x=['Ventas', 'Utilidad'], y=[vtas_curr, util_curr], marker_color='#0E1B2E'),
                go.Bar(name='Proyectado', x=['Ventas', 'Utilidad'], y=[vtas_proj, util_proj], marker_color='#00C2D1')
            ])
            fig_sim.update_layout(
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=260,
                xaxis=dict(tickfont=dict(color='#0B1220', size=11)),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686', size=11)),
                legend=dict(font=dict(color='#0B1220', size=11))
            )
            st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 12px; color: #6B7686;">NexData – Sistema de Analítica de Datos e Inteligencia Empresarial para MYPES | 2026</div>', unsafe_allow_html=True)
