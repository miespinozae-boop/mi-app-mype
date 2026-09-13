import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y FUERZA DE TEMA CLARO (ALTO CONTRASTE)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mi Negocio – Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS globales de alto contraste: Fondo blanco/claro (#F8FAFC / #FFFFFF) y letras oscuras (#0F172A)
st.markdown("""
<style>
    /* Estilo base y fondo general */
    html, body, [class*="stApp"], .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    /* Barra lateral - Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }

    /* Encabezados y títulos */
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, span, label {
        color: #0F172A !important;
    }

    /* Títulos principales */
    .main-header {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #1E3A8A !important;
        margin-bottom: 4px !important;
    }
    .sub-header {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        margin-bottom: 20px !important;
    }

    /* Tarjetas KPI de Alto Contraste */
    .metric-card {
        background-color: #FFFFFF !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        text-align: center !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 10px !important;
    }
    .metric-label {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #334155 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .metric-value {
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #0F172A !important;
        margin: 6px 0 !important;
    }
    .metric-delta-pos {
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #15803D !important; /* Verde oscuro visible */
        background-color: #DCFCE7 !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
    }
    .metric-delta-neg {
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #B91C1C !important; /* Rojo oscuro visible */
        background-color: #FEE2E2 !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
    }

    /* Contenedores de tarjetas de contenido */
    .content-box {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
    }

    /* Personalización de Pestañas (Tabs) */
    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #334155 !important;
        background-color: #F1F5F9 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 18px !important;
        border: 1px solid #CBD5E1 !important;
        margin-right: 4px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
        background-color: #2563EB !important;
        border-color: #2563EB !important;
    }

    /* Radio buttons en Sidebar */
    div[data-testid="stRadio"] label {
        background-color: #F1F5F9 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 6px !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        display: block !important;
    }

    /* Selectboxes y Entradas */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #94A3B8 !important;
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    /* Alertas */
    .stAlert {
        color: #0F172A !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CARGA Y PREPARACIÓN DE DATOS ROBUSTA
# -----------------------------------------------------------------------------
@st.cache_data
def generar_datos_sinteticos():
    np.random.seed(42)
    fechas = pd.date_range(start="2026-08-01", end="2026-09-12", freq="D")
    productos_dict = {
        "Abarrotes": [("Arroz Costeño 5kg", 24.50, 18.00), ("Aceite Primor 1L", 11.50, 8.50), ("Azúcar Rubia 1kg", 4.20, 3.10), ("Fideos Don Vittorio", 3.80, 2.70)],
        "Bebidas": [("Inca Kola 1.5L", 7.50, 5.20), ("Coca Cola 1.5L", 7.80, 5.40), ("Agua San Luis 2.5L", 4.50, 2.80), ("Cerveza Cusqueña 620ml", 8.50, 6.00)],
        "Lácteos": [("Leche Gloria Azul 400g", 4.20, 3.20), ("Yogurt Gloria 1L", 6.80, 4.90), ("Mantequilla Laive 200g", 8.20, 6.00)],
        "Snacks & Dulces": [("Galletas Casino 6pk", 4.50, 2.80), ("Papas Lays Clásicas", 5.00, 3.20), ("Chocolate Submarino", 2.50, 1.50)],
        "Limpieza": [("Detergente Bolívar 800g", 9.50, 7.00), ("Jabón Bolívar", 3.50, 2.40), ("Lavavajillas Ayudín", 5.20, 3.60)]
    }
    canales = ["Tienda Física", "Yape / WhatsApp", "Delivery Local"]

    registros = []
    tx_id = 1000
    for fecha in fechas:
        num_ventas = np.random.randint(15, 30)
        es_fin_semana = fecha.weekday() >= 5
        if es_fin_semana:
            num_ventas = int(num_ventas * 1.4)

        for _ in range(num_ventas):
            tx_id += 1
            cat = np.random.choice(list(productos_dict.keys()))
            prod_info = productos_dict[cat][np.random.randint(0, len(productos_dict[cat]))]
            prod_nombre, precio, costo = prod_info
            cant = np.random.randint(1, 6)
            canal = np.random.choice(canales, p=[0.6, 0.3, 0.1])

            vtas = round(cant * precio, 2)
            cst = round(cant * costo, 2)
            util = round(vtas - cst, 2)

            registros.append({
                "ID_Transaccion": f"TX-{tx_id}",
                "Fecha": fecha,
                "Dia_Semana": fecha.strftime("%A"),
                "Producto": prod_nombre,
                "Categoria": cat,
                "Canal_Venta": canal,
                "Cantidad": cant,
                "Precio_Unitario": precio,
                "Ventas_Soles": vtas,
                "Costo_Soles": cst,
                "Utilidad_Soles": util
            })
    return pd.DataFrame(registros)

def Cargar_Datos(file_uploaded=None):
    if file_uploaded is not None:
        try:
            if file_uploaded.name.endswith('.csv'):
                df = pd.read_csv(file_uploaded)
            else:
                df = pd.read_excel(file_uploaded)
            if 'Fecha' in df.columns:
                df['Fecha'] = pd.to_datetime(df['Fecha'])
            return df, "Archivo personalizado cargado exitosamente."
        except Exception as e:
            st.sidebar.error(f"Error al leer archivo: {e}. Cargando datos predeterminados.")
    
    # Intentar cargar dataset predeterminado local o generar
    rutas_posibles = [
        "dataset_mype_transacciones.csv",
        "/workspace/artifacts/dataset_mype_transacciones.csv",
        "/workspace/scratch/dataset_mype_transacciones.csv"
    ]
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            try:
                df = pd.read_csv(ruta)
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                return df, "Dataset predeterminado cargado."
            except:
                pass
    return generar_datos_sinteticos(), "Dataset sintético MYPE generado."

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL (SIDEBAR) INTERACTIVA Y COMPLETA
# -----------------------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#1E3A8A; margin-bottom:0;'>NEXDATA</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:12px; color:#475569; font-weight:600;'>Inteligencia Empresarial para MYPES</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Cargador de Archivos
archivo_subido = st.sidebar.file_uploader("📂 Cargar tu Excel / CSV:", type=["csv", "xlsx", "xls"])
df_raw, msg_carga = Cargar_Datos(archivo_subido)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Menú de Navegación")

# Navegación entre Pestañas / Pantallas (Totalmente Funcional)
opcion_menu = st.sidebar.radio(
    "Selecciona la pantalla:",
    ["🏠 Inicio / Dashboard", "📊 Ventas & Evolución", "📦 Productos Estrella", "💲 Rentabilidad", "💡 Alertas & Decisiones", "🧮 Simulador MYPE"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filtros de Negocio")

# Filtro Periodo
periodo_opt = st.sidebar.selectbox(
    "Periodo de Análisis:",
    ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Registro"]
)

max_date = df_raw['Fecha'].max()
min_date = df_raw['Fecha'].min()

if periodo_opt == "Últimos 30 días":
    fecha_fin = max_date
    fecha_inicio = max_date - pd.Timedelta(days=30)
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    fecha_inicio_prev = fecha_inicio - pd.Timedelta(days=30)
elif periodo_opt == "Este Mes":
    fecha_fin = max_date
    fecha_inicio = pd.to_datetime(f"{max_date.year}-{max_date.month:02d}-01")
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    fecha_inicio_prev = fecha_fin_prev - pd.Timedelta(days=30)
elif periodo_opt == "Mes Anterior":
    primer_dia_mes_actual = pd.to_datetime(f"{max_date.year}-{max_date.month:02d}-01")
    fecha_fin = primer_dia_mes_actual - pd.Timedelta(days=1)
    fecha_inicio = pd.to_datetime(f"{fecha_fin.year}-{fecha_fin.month:02d}-01")
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    fecha_inicio_prev = fecha_fin_prev - pd.Timedelta(days=30)
else:
    fecha_inicio = min_date
    fecha_fin = max_date
    fecha_inicio_prev = min_date
    fecha_fin_prev = max_date

# Filtros adicionales
cats = ["Todas"] + sorted(list(df_raw['Categoria'].dropna().unique()))
cat_sel = st.sidebar.selectbox("Categoría:", cats)

if cat_sel != "Todas":
    prods = ["Todos"] + sorted(list(df_raw[df_raw['Categoria'] == cat_sel]['Producto'].dropna().unique()))
else:
    prods = ["Todos"] + sorted(list(df_raw['Producto'].dropna().unique()))
prod_sel = st.sidebar.selectbox("Producto:", prods)

canales = ["Todos"] + sorted(list(df_raw['Canal_Venta'].dropna().unique()))
canal_sel = st.sidebar.selectbox("Canal de Venta:", canales)

# Filtrado de DataFrames
def aplicar_filtros(df, f_ini, f_fin, cat, prod, canal):
    df_f = df[(df['Fecha'] >= f_ini) & (df['Fecha'] <= f_fin)].copy()
    if cat != "Todas":
        df_f = df_f[df_f['Categoria'] == cat]
    if prod != "Todos":
        df_f = df_f[df_f['Producto'] == prod]
    if canal != "Todos":
        df_f = df_f[df_f['Canal_Venta'] == canal]
    return df_f

df_curr = aplicar_filtros(df_raw, fecha_inicio, fecha_fin, cat_sel, prod_sel, canal_sel)
df_prev = aplicar_filtros(df_raw, fecha_inicio_prev, fecha_fin_prev, cat_sel, prod_sel, canal_sel)

# CÁLCULOS KPI
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
d_tx = ((tx_c - tx_p) / tx_p * 100) if tx_p > 0 else 0

tkt_c = (vtas_c / tx_c) if tx_c > 0 else 0
tkt_p = (vtas_p / tx_p) if tx_p > 0 else 0
d_tkt = ((tkt_c - tkt_p) / tkt_p * 100) if tkt_p > 0 else 0


# -----------------------------------------------------------------------------
# 4. CONTENIDO SEGÚN LA NAVEGACIÓN DE LA BARRA LATERAL
# -----------------------------------------------------------------------------

# ENCABEZADO PRINCIPAL VISIBLE EN TODAS LAS PANTALLAS
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown('<div class="main-header">Mi Negocio – Panel de Inteligencia Empresarial</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Toma decisiones estratégicas con datos en tiempo real para tu MYPE</div>', unsafe_allow_html=True)
with col_head2:
    st.info(f"ℹ️ {msg_carga}")

# --- PANTALLA 1: INICIO / DASHBOARD ---
if opcion_menu == "🏠 Inicio / Dashboard":
    st.markdown("### 📊 Indicadores Clave de Desempeño (KPIs)")

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Ventas Totales</div>
            <div class="metric-value">S/ {vtas_c:,.2f}</div>
            <div class="{'metric-delta-pos' if d_vtas >= 0 else 'metric-delta-neg'}">
                {'▲' if d_vtas >= 0 else '▼'} {abs(d_vtas):.1f}% vs ant.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Utilidad Neta</div>
            <div class="metric-value">S/ {util_c:,.2f}</div>
            <div class="{'metric-delta-pos' if d_util >= 0 else 'metric-delta-neg'}">
                {'▲' if d_util >= 0 else '▼'} {abs(d_util):.1f}% vs ant.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Margen Utilidad</div>
            <div class="metric-value">{mg_c:.1f}%</div>
            <div class="{'metric-delta-pos' if d_mg >= 0 else 'metric-delta-neg'}">
                {'▲' if d_mg >= 0 else '▼'} {abs(d_mg):.1f} pp vs ant.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">N° de Ventas</div>
            <div class="metric-value">{tx_c:,}</div>
            <div class="{'metric-delta-pos' if d_tx >= 0 else 'metric-delta-neg'}">
                {'▲' if d_tx >= 0 else '▼'} {abs(d_tx):.1f}% vs ant.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Ticket Promedio</div>
            <div class="metric-value">S/ {tkt_c:.2f}</div>
            <div class="{'metric-delta-pos' if d_tkt >= 0 else 'metric-delta-neg'}">
                {'▲' if d_tkt >= 0 else '▼'} {abs(d_tkt):.1f}% vs ant.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns([1.8, 1.2])

    with col_g1:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>📈 Evolución Diaria de Ventas y Utilidad</h4>", unsafe_allow_html=True)
        
        df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
        
        fig_evol = go.Figure()
        fig_evol.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Ventas_Soles'],
            mode='lines+markers', name='Ventas (S/)',
            line=dict(color='#2563EB', width=3, shape='spline'),
            fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.08)'
        ))
        fig_evol.add_trace(go.Scatter(
            x=df_daily['Fecha'], y=df_daily['Utilidad_Soles'],
            mode='lines+markers', name='Utilidad (S/)',
            line=dict(color='#16A34A', width=2.5, shape='spline')
        ))
        fig_evol.update_layout(
            height=320, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0F172A', size=11)),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0F172A', size=11)),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#0F172A', size=12))
        )
        st.plotly_chart(fig_evol, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_g2:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>📊 Ventas por Categoría</h4>", unsafe_allow_html=True)
        
        df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        fig_pie = px.pie(
            df_cat, names='Categoria', values='Ventas_Soles',
            hole=0.5, color_discrete_sequence=['#2563EB', '#16A34A', '#9333EA', '#EA580C', '#0284C7']
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            height=320, margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(font=dict(color='#0F172A', size=11))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PANTALLA 2: VENTAS & EVOLUCIÓN ---
elif opcion_menu == "📊 Ventas & Evolución":
    st.markdown("### 📊 Análisis Detallado de Ventas")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>🛒 Ventas por Canal de Venta</h4>", unsafe_allow_html=True)
        df_canal = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
        fig_canal = px.bar(
            df_canal, x='Canal_Venta', y='Ventas_Soles', text_auto='.2f',
            color='Canal_Venta', color_discrete_sequence=['#2563EB', '#16A34A', '#EA580C']
        )
        fig_canal.update_layout(
            height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#0F172A', size=12), title=""),
            yaxis=dict(tickfont=dict(color='#0F172A', size=11), title="Soles (S/)"),
            showlegend=False
        )
        st.plotly_chart(fig_canal, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_v2:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>📅 Ventas por Día de la Semana</h4>", unsafe_allow_html=True)
        dias_orden = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        df_curr['Dia_Num'] = df_curr['Fecha'].dt.dayofweek
        df_dias = df_curr.groupby('Dia_Num')['Ventas_Soles'].sum().reset_index()
        df_dias['Dia_Nombre'] = df_dias['Dia_Num'].apply(lambda x: dias_es[x])
        
        fig_dias = px.bar(
            df_dias, x='Dia_Nombre', y='Ventas_Soles', text_auto='.2f',
            color_discrete_sequence=['#2563EB']
        )
        fig_dias.update_layout(
            height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#0F172A', size=12), title=""),
            yaxis=dict(tickfont=dict(color='#0F172A', size=11), title="Soles (S/)")
        )
        st.plotly_chart(fig_dias, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 📋 Registro Detallado de Transacciones")
    st.dataframe(
        df_curr[['ID_Transaccion', 'Fecha', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Ventas_Soles', 'Utilidad_Soles']].sort_values(by='Fecha', ascending=False),
        use_container_width=True
    )

# --- PANTALLA 3: PRODUCTOS ESTRELLA ---
elif opcion_menu == "📦 Productos Estrella":
    st.markdown("### 📦 Desempeño por Productos")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>🏆 Top 10 Productos por Ingresos (S/)</h4>", unsafe_allow_html=True)
        df_top_rev = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()
        
        fig_top_rev = px.bar(df_top_rev, y='Producto', x='Ventas_Soles', orientation='h', text_auto='.2f', color_discrete_sequence=['#2563EB'])
        fig_top_rev.update_layout(
            height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#0F172A'), title="Soles (S/)"),
            yaxis=dict(tickfont=dict(color='#0F172A', size=12), title="")
        )
        st.plotly_chart(fig_top_rev, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_p2:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>🔢 Top 10 Productos por Unidades Vendidas</h4>", unsafe_allow_html=True)
        df_top_qty = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()
        
        fig_top_qty = px.bar(df_top_qty, y='Producto', x='Cantidad', orientation='h', text_auto=True, color_discrete_sequence=['#16A34A'])
        fig_top_qty.update_layout(
            height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#0F172A'), title="Unidades"),
            yaxis=dict(tickfont=dict(color='#0F172A', size=12), title="")
        )
        st.plotly_chart(fig_top_qty, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PANTALLA 4: RENTABILIDAD ---
elif opcion_menu == "💲 Rentabilidad":
    st.markdown("### 💲 Análisis de Márgenes y Rentabilidad")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>💰 Margen de Ganancia (%) por Categoría</h4>", unsafe_allow_html=True)
        
        df_mg_cat = df_curr.groupby('Categoria').apply(
            lambda x: (x['Utilidad_Soles'].sum() / x['Ventas_Soles'].sum() * 100) if x['Ventas_Soles'].sum() > 0 else 0
        ).reset_index(name='Margen_%')
        
        fig_mg = px.bar(df_mg_cat, x='Categoria', y='Margen_%', text_auto='.1f', color_discrete_sequence=['#9333EA'])
        fig_mg.update_layout(
            height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#0F172A', size=12), title=""),
            yaxis=dict(tickfont=dict(color='#0F172A'), title="Margen (%)")
        )
        st.plotly_chart(fig_mg, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r2:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>⚖️ Relación Ventas vs. Utilidad por Producto</h4>", unsafe_allow_html=True)
        
        df_prod_summary = df_curr.groupby('Producto').agg({
            'Ventas_Soles': 'sum',
            'Utilidad_Soles': 'sum',
            'Cantidad': 'sum'
        }).reset_index()
        
        fig_scatter = px.scatter(
            df_prod_summary, x='Ventas_Soles', y='Utilidad_Soles', size='Cantidad', text='Producto',
            color='Utilidad_Soles', color_continuous_scale='Greens'
        )
        fig_scatter.update_traces(textposition='top center')
        fig_scatter.update_layout(
            height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#0F172A'), title="Ventas Totales (S/)"),
            yaxis=dict(tickfont=dict(color='#0F172A'), title="Utilidad Neta (S/)")
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- PANTALLA 5: ALERTAS & DECISIONES ---
elif opcion_menu == "💡 Alertas & Decisiones":
    st.markdown("### 💡 Inteligencia de Negocio y Decisiones Recomendadas")

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>🚨 Alertas Operativas Detectadas</h4>", unsafe_allow_html=True)
        st.warning("⚠️ **Demanda Alta en Fines de Semana:** Las ventas de Bebidas incrementan un +42% los días Sábado y Domingo. **Acción:** Reabastecer stock los jueves.")
        st.error("🔴 **Alerta de Rotación de Stock:** El producto 'Galletas Casino' ha reducido su velocidad de venta en 28%. **Acción:** Impulsar ventas cruzadas en caja.")
        st.success("🟢 **Consolidación Digital:** El canal 'Yape / WhatsApp' representa el 30% de los ingresos totales con cero comisión. **Acción:** Colocar QR visible en mostrador.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_a2:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>🎯 Plan de Acción Recomendado para la MYPE</h4>", unsafe_allow_html=True)
        st.info("1️⃣ **Aumentar Ticket Promedio:** Ofrecer promociones de 'Lleva 2 por S/ X' en golosinas y snacks al momento del cobro.")
        st.info("2️⃣ **Optimización de Compras:** Reducir compras de productos de baja rotación y concentrar liquidez en Abarrotes de primera necesidad.")
        st.info("3️⃣ **Medición GpR Continuada:** Revisar semanalmente la evolución del Margen de Utilidad para asegurar que se mantenga por encima del 25%.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PANTALLA 6: SIMULADOR MYPE ---
elif opcion_menu == "🧮 Simulador MYPE":
    st.markdown("### 🧮 Simulador Interactivo de Rentabilidad y ROI")
    st.markdown("<p style='color:#475569;'>Ajusta los parámetros para simular el impacto financiero del uso de la plataforma SaaS en tu MYPE.</p>", unsafe_allow_html=True)

    col_s1, col_s2 = st.columns([1, 1])

    with col_s1:
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>⚙️ Parámetros de Simulación</h4>", unsafe_allow_html=True)
        
        vta_base = st.number_input("Ventas Mensuales Actuales (S/):", value=11900.0, step=500.0)
        p_merma = st.slider("% Mermas/Pérdidas sin Analítica:", min_value=1.0, max_value=10.0, value=5.0, step=0.5) / 100.0
        
        inc_ventas = st.slider("% Crecimiento Estimado en Ventas (Evitación de Quiebres):", min_value=0.0, max_value=30.0, value=16.3, step=0.5) / 100.0
        red_merma = st.slider("% Reducción de Mermas con Analítica:", min_value=10.0, max_value=90.0, value=70.0, step=5.0) / 100.0
        
        costo_plan = st.selectbox("Plan de Suscripción Seleccionado:", ["Plan Premium (S/ 150/mes)", "Plan Básico (S/ 50/mes)"])
        tarifa_plan = 150.0 if "Premium" in costo_plan else 50.0
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s2:
        # CÁLCULOS SIMULADOR
        merma_trad = vta_base * p_merma
        vta_analitica = vta_base * (1 + inc_ventas)
        merma_analitica = merma_trad * (1 - red_merma)
        
        ganancia_extra_vtas = vta_base * inc_ventas * 0.25 # Asumiendo 25% margen
        ahorro_mermas = merma_trad - merma_analitica
        beneficio_bruto = ganancia_extra_vtas + ahorro_mermas
        beneficio_neto = beneficio_bruto - tarifa_plan
        roi_cliente = (beneficio_neto / tarifa_plan * 100) if tarifa_plan > 0 else 0

        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#1E3A8A; margin-top:0;'>📈 Resultados de la Simulación</h4>", unsafe_allow_html=True)
        
        st.metric("Ventas Totales Proyectadas:", f"S/ {vta_analitica:,.2f}", f"+S/ {vta_base*inc_ventas:,.2f}")
        st.metric("Ahorro Mensual en Mermas:", f"S/ {ahorro_mermas:,.2f}", f"-{red_merma*100:.0f}% Mermas")
        st.metric("Beneficio Neto Adicional para la MYPE:", f"S/ {beneficio_neto:,.2f} / mes")
        
        st.success(f"🎉 **ROI del Cliente:** **{roi_cliente:.1f}%** — Por cada S/ 1.00 invertido en la plataforma, la MYPE recupera **S/ {(beneficio_neto/tarifa_plan)+1:.2f}** en ganancia directa.")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("NEXDATA – Plataforma de Analítica Avanzada de Datos para MYPES | Proyecto GpR 2026")
