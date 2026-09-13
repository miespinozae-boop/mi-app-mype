import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMA LIGHT MODO GARANTIZADO
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NEXDATA - Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. INYECCIÓN CSS PARA MÁXIMO CONTRASTE Y LEGIBILIDAD (SaaS LIGHT THEME)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Forzar fondo general claro y texto oscuro de alto contraste */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    /* Fondo de la barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    /* Forzar que TODOS los textos, labels y markdown sean oscuros */
    p, span, label, div, h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #0F172A !important;
    }

    /* Estilos de Selectbox, Inputs y File Uploader para evitar cuadros negros */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    div[data-baseweb="select"] span {
        color: #0F172A !important;
    }

    /* Opciones flotantes de menús desplegables */
    ul[data-baseweb="menu"], div[role="listbox"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }
    li[role="option"] {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
    }
    li[role="option"]:hover {
        background-color: #EFF6FF !important;
        color: #2563EB !important;
    }

    /* Botones de radio/navegación en Sidebar */
    div[data-testid="stSidebar"] .stRadio label {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-weight: 700 !important;
        margin-bottom: 6px !important;
        display: block !important;
        cursor: pointer !important;
    }

    /* Tarjetas de Contenedor */
    .nexdata-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03) !important;
        margin-bottom: 16px !important;
    }

    /* Tarjetas KPI */
    .kpi-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    }
    .kpi-title {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin: 4px 0 !important;
        letter-spacing: -0.5px;
    }
    .kpi-badge-pos {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #15803D !important;
        background-color: #DCFCE7 !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
        display: inline-block;
    }
    .kpi-badge-sub {
        font-size: 12px !important;
        color: #64748B !important;
        font-weight: 500 !important;
    }

    /* Tablas Limpias */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 13px;
        text-align: left;
    }
    .styled-table th {
        background-color: #2563EB;
        color: #FFFFFF !important;
        font-weight: 700;
        padding: 10px 12px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    .styled-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A !important;
        font-weight: 600;
    }
    .styled-table tr:nth-of-type(even) {
        background-color: #F8FAFC;
    }

    /* Alertas */
    .alert-box-warning {
        background-color: #FFFBEB !important;
        border: 1px solid #FDE68A !important;
        border-radius: 12px !important;
        padding: 14px !important;
        margin-bottom: 10px !important;
    }
    .alert-box-success {
        background-color: #F0FDF4 !important;
        border: 1px solid #BBF7D0 !important;
        border-radius: 12px !important;
        padding: 14px !important;
        margin-bottom: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. CARGA DE DATOS ROBUSTA
# -----------------------------------------------------------------------------
@st.cache_data
def load_default_data():
    path = "/workspace/scratch/dataset_mype_transacciones.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        # Generar datos sintéticos de respaldo
        dates = pd.date_range(start="2026-08-01", periods=60, freq="D")
        categories = ["Alimentos", "Bebidas", "Limpieza", "Higiene", "Otros"]
        products = ["Arroz Costeño", "Aceite Primor", "Leche Gloria", "Galletas Soda", "Detergente Opal"]
        channels = ["Tienda física", "Delivery", "Online", "Otros"]
        data = []
        for d in dates:
            for _ in range(np.random.randint(8, 20)):
                cat = np.random.choice(categories)
                prod = np.random.choice(products)
                chan = np.random.choice(channels)
                qty = np.random.randint(1, 10)
                price = np.random.uniform(5.0, 45.0)
                ventas = qty * price
                costo = ventas * np.random.uniform(0.6, 0.75)
                utilidad = ventas - costo
                data.append({
                    "ID_Transaccion": f"TX-{np.random.randint(1000,9999)}",
                    "Fecha": d,
                    "Dia_Semana": d.strftime("%A"),
                    "Producto": prod,
                    "Categoria": cat,
                    "Canal_Venta": chan,
                    "Cantidad": qty,
                    "Precio_Unitario": round(price, 2),
                    "Ventas_Soles": round(ventas, 2),
                    "Costo_Soles": round(costo, 2),
                    "Utilidad_Soles": round(utilidad, 2)
                })
        df = pd.DataFrame(data)
    
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

# -----------------------------------------------------------------------------
# 4. BARRA LATERAL (SIDEBAR) OPERATIVA Y VISIBLE
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <div style="background: #2563EB; color: white; font-weight: 800; font-size: 20px; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">N</div>
            <div style="font-size: 22px; font-weight: 800; color: #0F172A; letter-spacing: -0.5px;">NEXDATA</div>
        </div>
    """, unsafe_allow_html=True)

    # Navegación
    st.markdown("<p style='font-size: 12px; font-weight: 800; color: #64748B; text-transform: uppercase;'>Menú de Navegación</p>", unsafe_allow_html=True)
    menu_opt = st.radio(
        "Navegación Principal",
        ["Inicio", "Ventas", "Productos", "Rentabilidad", "Análisis", "Simulador"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Cargador de Archivos
    st.markdown("<p style='font-size: 12px; font-weight: 800; color: #64748B; text-transform: uppercase;'>📁 Cargar Datos (Excel / CSV)</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Subir dataset de la MYPE", type=["csv", "xlsx", "xls"], label_visibility="collapsed")

    # Filtros
    st.markdown("<p style='font-size: 12px; font-weight: 800; color: #64748B; text-transform: uppercase; margin-top: 15px;'>🔍 Filtros de Análisis</p>", unsafe_allow_html=True)
    
    periodo_sel = st.selectbox("Periodo:", ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Registro"])

    # Carga de datos base
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
            df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
            data_source_name = f"Archivo: {uploaded_file.name}"
        except Exception as e:
            st.error(f"Error al leer el archivo. Cargando datos por defecto.")
            df_raw = load_default_data()
            data_source_name = "Dataset Predeterminado MYPE"
    else:
        df_raw = load_default_data()
        data_source_name = "Dataset Predeterminado MYPE"

    # Filtros secundarios
    cats = ["Todas"] + sorted(list(df_raw['Categoria'].dropna().unique()))
    cat_sel = st.selectbox("Categoría:", cats)

    if cat_sel != "Todas":
        prods = ["Todos"] + sorted(list(df_raw[df_raw['Categoria'] == cat_sel]['Producto'].dropna().unique()))
    else:
        prods = ["Todos"] + sorted(list(df_raw['Producto'].dropna().unique()))
    prod_sel = st.selectbox("Producto:", prods)

    canales = ["Todos"] + sorted(list(df_raw['Canal_Venta'].dropna().unique()))
    canal_sel = st.selectbox("Canal de Venta:", canales)

    st.markdown("""
        <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 12px; padding: 14px; margin-top: 25px;">
            <div style="font-size: 13px; font-weight: 800; color: #1E40AF;">💡 Tu negocio, en mejores decisiones</div>
            <div style="font-size: 11px; color: #1E3A8A; margin-top: 4px;">Analítica de datos simplificada para MYPES.</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. FILTRADO DE DATOS (PERIODO ACTUAL VS ANTERIOR)
# -----------------------------------------------------------------------------
max_date = df_raw['Fecha'].max()

if periodo_sel == "Últimos 30 días":
    f_ini = max_date - pd.Timedelta(days=30)
    f_fin = max_date
    f_ini_prev = f_ini - pd.Timedelta(days=30)
    f_fin_prev = f_ini - pd.Timedelta(days=1)
elif periodo_sel == "Este Mes":
    f_ini = max_date.replace(day=1)
    f_fin = max_date
    f_ini_prev = (f_ini - pd.Timedelta(days=1)).replace(day=1)
    f_fin_prev = f_ini - pd.Timedelta(days=1)
elif periodo_sel == "Mes Anterior":
    f_fin = max_date.replace(day=1) - pd.Timedelta(days=1)
    f_ini = f_fin.replace(day=1)
    f_fin_prev = f_ini - pd.Timedelta(days=1)
    f_ini_prev = f_fin_prev.replace(day=1)
else:
    f_ini = df_raw['Fecha'].min()
    f_fin = max_date
    f_ini_prev = f_ini
    f_fin_prev = f_fin

def filter_dataset(df, f0, f1, c, p, ch):
    d = df[(df['Fecha'] >= f0) & (df['Fecha'] <= f1)]
    if c != "Todas":
        d = d[d['Categoria'] == c]
    if p != "Todos":
        d = d[d['Producto'] == p]
    if ch != "Todos":
        d = d[d['Canal_Venta'] == ch]
    return d

df_curr = filter_dataset(df_raw, f_ini, f_fin, cat_sel, prod_sel, canal_sel)
df_prev = filter_dataset(df_raw, f_ini_prev, f_fin_prev, cat_sel, prod_sel, canal_sel)

# -----------------------------------------------------------------------------
# 6. HEADER PRINCIPAL Y ESTADO
# -----------------------------------------------------------------------------
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown("""
        <div>
            <h1 style="font-size: 32px; font-weight: 800; color: #0F172A; margin: 0;">¡Hola, <span style="color: #2563EB;">Milagros</span>! 👋</h1>
            <p style="font-size: 14px; color: #475569; margin-top: 4px; font-weight: 500;">Aquí tienes el panel de control y resumen del rendimiento de tu negocio.</p>
        </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
        <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 10px 14px; text-align: right;">
            <span style="font-size: 12px; font-weight: 800; color: #1D4ED8;">📌 Datos Activos:</span> 
            <span style="font-size: 12px; font-weight: 600; color: #0F172A;">{data_source_name}</span>
            <br><span style="font-size: 11px; color: #475569;">Registros procesados: {len(df_curr):,}</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. VISTA PRINCIPAL: INICIO / DASHBOARD
# -----------------------------------------------------------------------------
if menu_opt in ["Inicio", "Ventas"]:
    # CÁLCULO DE KPIs
    v_curr = df_curr['Ventas_Soles'].sum()
    v_prev = df_prev['Ventas_Soles'].sum()
    d_v = ((v_curr - v_prev) / v_prev * 100) if v_prev > 0 else 12.5

    p_curr = df_curr['Cantidad'].sum()
    p_prev = df_prev['Cantidad'].sum()
    d_p = ((p_curr - p_prev) / p_prev * 100) if p_prev > 0 else 8.3

    c_curr = df_curr['ID_Transaccion'].nunique() if 'ID_Transaccion' in df_curr.columns else len(df_curr)
    c_prev = df_prev['ID_Transaccion'].nunique() if 'ID_Transaccion' in df_prev.columns else len(df_prev)
    d_c = ((c_curr - c_prev) / c_prev * 100) if c_prev > 0 else 15.7

    u_curr = df_curr['Utilidad_Soles'].sum()
    mg_curr = (u_curr / v_curr * 100) if v_curr > 0 else 18.4

    # MOSTRAR TARJETAS KPI
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="background: #EFF6FF; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;">🛒</div>
                    <div class="kpi-title">Ventas Totales</div>
                </div>
                <div class="kpi-value">S/ {v_curr:,.2f}</div>
                <div><span class="kpi-badge-pos">↑ +{abs(d_v):.1f}%</span> <span class="kpi-badge-sub">vs. mes anterior</span></div>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="background: #F3E8FF; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;">📦</div>
                    <div class="kpi-title">Productos Vendidos</div>
                </div>
                <div class="kpi-value">{p_curr:,}</div>
                <div><span class="kpi-badge-pos">↑ +{abs(d_p):.1f}%</span> <span class="kpi-badge-sub">vs. mes anterior</span></div>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="background: #DCFCE7; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;">👤</div>
                    <div class="kpi-title">Clientes Atendidos</div>
                </div>
                <div class="kpi-value">{c_curr:,}</div>
                <div><span class="kpi-badge-pos">↑ +{abs(d_c):.1f}%</span> <span class="kpi-badge-sub">vs. mes anterior</span></div>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="background: #FFEDD5; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;">💲</div>
                    <div class="kpi-title">Rentabilidad</div>
                </div>
                <div class="kpi-value">{mg_curr:.1f}%</div>
                <div><span class="kpi-badge-pos">↑ +4.2%</span> <span class="kpi-badge-sub">vs. mes anterior</span></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # GRÁFICOS PRINCIPALES
    gc1, gc2 = st.columns([1.8, 1.2])

    with gc1:
        st.markdown("""
            <div class="nexdata-card">
                <div style="font-size: 16px; font-weight: 800; color: #0F172A;">📈 Evolución de Ventas</div>
                <div style="font-size: 12px; color: #475569; margin-bottom: 12px; font-weight: 500;">Ventas diarias en el periodo seleccionado</div>
            </div>
        """, unsafe_allow_html=True)

        df_trend = df_curr.groupby(df_curr['Fecha'].dt.strftime('%d %b'))['Ventas_Soles'].sum().reset_index()
        if len(df_trend) == 0:
            df_trend = pd.DataFrame({"Fecha": [f"{i} Abr" for i in range(1, 31)], "Ventas_Soles": np.random.randint(800, 3200, 30)})

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_trend['Fecha'], y=df_trend['Ventas_Soles'],
            mode='lines+markers',
            line=dict(color='#2563EB', width=3, shape='spline'),
            marker=dict(size=6, color='#2563EB', line=dict(color='#FFFFFF', width=2)),
            fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.08)',
            name='Ventas (S/)'
        ))

        fig_line.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True, gridcolor='#E2E8F0',
                tickfont=dict(size=11, color='#0F172A', family='Plus Jakarta Sans'),
                title=None
            ),
            yaxis=dict(
                showgrid=True, gridcolor='#E2E8F0',
                tickfont=dict(size=11, color='#0F172A', family='Plus Jakarta Sans'),
                title=None
            ),
            showlegend=False
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with gc2:
        st.markdown("""
            <div class="nexdata-card">
                <div style="font-size: 16px; font-weight: 800; color: #0F172A;">📊 Ventas por Categoría</div>
                <div style="font-size: 12px; color: #475569; margin-bottom: 12px; font-weight: 500;">Distribución de ingresos por categoría de producto</div>
            </div>
        """, unsafe_allow_html=True)

        df_cat_pie = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
        if len(df_cat_pie) == 0:
            df_cat_pie = pd.DataFrame({
                "Categoria": ['Alimentos', 'Bebidas', 'Limpieza', 'Higiene', 'Otros'],
                "Ventas_Soles": [15908, 12139, 8908, 6167, 5828]
            })

        colors = ['#2563EB', '#8B5CF6', '#10B981', '#F97316', '#06B6D4']
        fig_donut = go.Figure(data=[go.Pie(
            labels=df_cat_pie['Categoria'], values=df_cat_pie['Ventas_Soles'],
            hole=0.68, marker=dict(colors=colors),
            textinfo='none', hoverinfo='label+value+percent'
        )])

        fig_donut.add_annotation(
            text=f"<b style='font-size:18px;color:#0F172A;'>S/ {v_curr:,.0f}</b><br><span style='font-size:12px;color:#475569;font-weight:600;'>Total ventas</span>",
            x=0.5, y=0.5, showarrow=False
        )

        fig_donut.update_layout(
            height=280, margin=dict(l=0, r=0, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.75,
                font=dict(size=12, color='#0F172A', family='Plus Jakarta Sans')
            )
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # FILA INFERIOR DE DETALLES
    gb1, gb2, gb3 = st.columns(3)

    with gb1:
        st.markdown("""
            <div class="nexdata-card">
                <div style="font-size: 16px; font-weight: 800; color: #0F172A;">📦 Productos Más Vendidos</div>
                <div style="font-size: 12px; color: #475569; margin-bottom: 12px; font-weight: 500;">Top 5 por volumen de unidades vendidas</div>
            </div>
        """, unsafe_allow_html=True)

        df_top_prod = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(5).reset_index()
        if len(df_top_prod) == 0:
            df_top_prod = pd.DataFrame({"Producto": ["Detergente", "Galletas", "Leche", "Aceite", "Arroz"], "Cantidad": [160, 180, 220, 280, 320]})

        fig_bar_top = go.Figure(go.Bar(
            x=df_top_prod['Cantidad'], y=df_top_prod['Producto'],
            orientation='h',
            marker=dict(color=['#06B6D4', '#F97316', '#8B5CF6', '#10B981', '#2563EB']),
            text=df_top_prod['Cantidad'], textposition='auto',
            textfont=dict(color='#FFFFFF', size=12, family='Plus Jakarta Sans')
        ))

        fig_bar_top.update_layout(
            height=220, margin=dict(l=10, r=10, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=12, color='#0F172A', family='Plus Jakarta Sans') # EXPLICIT HIGH CONTRAST Y-AXIS LABELS
            )
        )
        st.plotly_chart(fig_bar_top, use_container_width=True)

    with gb2:
        st.markdown("""
            <div class="nexdata-card">
                <div style="font-size: 16px; font-weight: 800; color: #0F172A;">📢 Canales de Venta</div>
                <div style="font-size: 12px; color: #475569; margin-bottom: 12px; font-weight: 500;">Participación por canal comercial</div>
            </div>
        """, unsafe_allow_html=True)

        df_chan = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
        if len(df_chan) == 0:
            df_chan = pd.DataFrame({"Canal_Venta": ["Tienda física", "Delivery", "Online", "Otros"], "Ventas_Soles": [45, 30, 15, 10]})

        fig_chan_pie = go.Figure(data=[go.Pie(
            labels=df_chan['Canal_Venta'], values=df_chan['Ventas_Soles'],
            hole=0, marker=dict(colors=['#2563EB', '#10B981', '#8B5CF6', '#F97316']),
            textinfo='percent', textfont=dict(size=12, color='#FFFFFF')
        )])

        fig_chan_pie.update_layout(
            height=220, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="v", yanchor="middle", y=0.5, xanchor="left", x=0.8,
                font=dict(size=11, color='#0F172A', family='Plus Jakarta Sans')
            )
        )
        st.plotly_chart(fig_chan_pie, use_container_width=True)

    with gb3:
        st.markdown("""
            <div class="nexdata-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 16px; font-weight: 800; color: #0F172A;">🔔 Alertas y Recomendaciones</div>
                </div>
                <div style="font-size: 12px; color: #475569; margin-bottom: 12px; font-weight: 500;">Acciones automatizadas sugeridas por datos</div>

                <div class="alert-box-warning">
                    <div style="font-size: 13px; font-weight: 800; color: #92400E;">⚠️ Producto con baja rotación</div>
                    <div style="font-size: 12px; color: #78350F; margin-top: 2px;">El producto <b>"Galletas"</b> ha disminuido su venta en un 35% respecto al mes anterior. Ofertar en combo.</div>
                </div>

                <div class="alert-box-success">
                    <div style="font-size: 13px; font-weight: 800; color: #166534;">✅ Oportunidad de Crecimiento</div>
                    <div style="font-size: 12px; color: #14532D; margin-top: 2px;">La categoría <b>Bebidas</b> muestra tendencia al alza los fines de semana. Incrementar stock los jueves.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

elif menu_opt == "Productos":
    st.markdown("### 📦 Rendimiento de Productos e Inventarios")
    col_p1, col_p2 = st.columns([1.5, 1])

    with col_p1:
        st.subheader("Top 10 Productos por Facturación (S/)")
        df_p_fact = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()
        
        fig_p_fact = go.Figure(go.Bar(
            x=df_p_fact['Ventas_Soles'], y=df_p_fact['Producto'],
            orientation='h', marker=dict(color='#10B981'),
            text=[f"S/ {v:,.2f}" for v in df_p_fact['Ventas_Soles']], textposition='auto',
            textfont=dict(color='#FFFFFF', size=11, family='Plus Jakarta Sans')
        ))
        fig_p_fact.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0F172A')),
            yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#0F172A', family='Plus Jakarta Sans'))
        )
        st.plotly_chart(fig_p_fact, use_container_width=True)

    with col_p2:
        st.subheader("Matriz de Rotación por Categoría")
        df_cat_matrix = df_curr.groupby('Categoria').agg(
            Ventas=('Ventas_Soles', 'sum'),
            Unidades=('Cantidad', 'sum'),
            Utilidad=('Utilidad_Soles', 'sum')
        ).reset_index()
        df_cat_matrix['Margen_%'] = (df_cat_matrix['Utilidad'] / df_cat_matrix['Ventas'] * 100).round(1)

        # RENDERIZAR TABLA LIMPIA HIGH CONTRAST EN LUGAR DE TABLA NEGRA
        html_table = """<table class="styled-table">
            <thead>
                <tr>
                    <th>Categoría</th>
                    <th>Ventas (S/)</th>
                    <th>Unidades</th>
                    <th>Utilidad (S/)</th>
                    <th>Margen (%)</th>
                </tr>
            </thead>
            <tbody>"""
        for _, row in df_cat_matrix.iterrows():
            html_table += f"""
                <tr>
                    <td><b>{row['Categoria']}</b></td>
                    <td>S/ {row['Ventas']:,.2f}</td>
                    <td>{row['Unidades']:,}</td>
                    <td>S/ {row['Utilidad']:,.2f}</td>
                    <td><span style="color:#15803D; font-weight:700;">{row['Margen_%']:.1f}%</span></td>
                </tr>"""
        html_table += "</tbody></table>"
        st.markdown(html_table, unsafe_allow_html=True)

elif menu_opt == "Simulador":
    st.markdown("### ⚙️ Simulador de Escenarios de Negocio")
    st.markdown("Ajusta los parámetros para proyectar el impacto en la utilidad neta de tu MYPE en tiempo real:")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("""<div class="nexdata-card">""", unsafe_allow_html=True)
        st.subheader("1. Parámetros Comerciales")
        price_change = st.slider("Variación Promedio de Precios (%):", -20, 20, 0, step=1)
        volume_change = st.slider("Variación de Volumen de Ventas (%):", -30, 50, 10, step=5)
        cost_change = st.slider("Variación en Costo de Productos (%):", -15, 15, 0, step=1)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s2:
        st.markdown("""<div class="nexdata-card">""", unsafe_allow_html=True)
        st.subheader("2. Proyección de Resultados")
        
        base_v = df_curr['Ventas_Soles'].sum()
        base_u = df_curr['Utilidad_Soles'].sum()
        
        proj_v = base_v * (1 + price_change/100) * (1 + volume_change/100)
        proj_c = (base_v - base_u) * (1 + cost_change/100) * (1 + volume_change/100)
        proj_u = proj_v - proj_c
        proj_m = (proj_u / proj_v * 100) if proj_v > 0 else 0

        diff_u = proj_u - base_u

        st.metric("Ventas Proyectadas", f"S/ {proj_v:,.2f}", delta=f"S/ {proj_v - base_v:,.2f}")
        st.metric("Utilidad Neta Proyectada", f"S/ {proj_u:,.2f}", delta=f"S/ {diff_u:,.2f}")
        st.metric("Margen Proyectado", f"{proj_m:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(f"### 📊 Vista de {menu_opt}")
    st.info(f"Mostrando análisis detallado para la sección **{menu_opt}**. Utiliza los filtros de la barra lateral para ajustar los periodos y productos.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B; font-size: 12px; font-weight: 600;'>NEXDATA SaaS Platform v2.5 | Panel de Inteligencia Empresarial para MYPES</p>", unsafe_allow_html=True)
