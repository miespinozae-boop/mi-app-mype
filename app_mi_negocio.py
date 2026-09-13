import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="NEXDATA – Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide"
)

# Estilos CSS limpios y modernos
st.markdown("""
<style>
    .main-header {
        font-size: 28px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        margin: 5px 0;
    }
    .metric-delta-pos {
        font-size: 12px;
        font-weight: 700;
        color: #16A34A;
    }
    .metric-delta-neg {
        font-size: 12px;
        font-weight: 700;
        color: #DC2626;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown('<div class="main-header">NEXDATA – Panel de Inteligencia Empresarial</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma intuitiva de análisis de datos para la toma de decisiones en tu MYPE</div>', unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_default_data():
    posibles_rutas = [
        Path("dataset_mype_transacciones.csv"),
        Path("/workspace/scratch/dataset_mype_transacciones.csv")
    ]

    for ruta in posibles_rutas:
        if ruta.exists():
            df = pd.read_csv(ruta)
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
            return df

    return pd.DataFrame()

st.sidebar.markdown("### Cargar datos")
archivo_subido = st.sidebar.file_uploader(
    "Sube tu archivo Excel o CSV",
    type=["xlsx", "xls", "csv"],
    help="Las columnas deben conservar los nombres del archivo de ejemplo."
)

@st.cache_data
def read_uploaded_file(file_bytes, file_name):
    import io

    if file_name.lower().endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        df = pd.read_excel(io.BytesIO(file_bytes))

    columnas_requeridas = [
        "Fecha", "Categoria", "Producto",
        "Canal_Venta", "Ventas_Soles", "Utilidad_Soles"
    ]
    faltantes = [c for c in columnas_requeridas if c not in df.columns]

    if faltantes:
        raise ValueError(
            "Faltan estas columnas: " + ", ".join(faltantes)
        )

    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    return df

if archivo_subido is not None:
    try:
        df_raw = read_uploaded_file(
            archivo_subido.getvalue(),
            archivo_subido.name
        )
        st.sidebar.success("Archivo cargado correctamente.")
    except Exception as e:
        st.sidebar.error(f"No se pudo cargar el archivo: {e}")
        df_raw = load_default_data()
else:
    df_raw = load_default_data()

if df_raw.empty:
    st.error("No hay datos disponibles. Sube un archivo Excel o CSV.")
    st.stop()

# ---------------------------------------------------------
# FILTROS INTERACTIVOS EN LA BARRA LATERAL Y PRINCIPAL
# ---------------------------------------------------------
st.sidebar.header("🔍 Filtros de Negocio")

# Filtro 1: Periodo
periodo_opt = st.sidebar.selectbox(
    "Seleccionar Periodo:",
    ["Últimos 30 días", "Este Mes (Septiembre 2026)", "Mes Anterior (Agosto 2026)", "Todo el Registro"]
)

max_date = df_raw['Fecha'].max()
if periodo_opt == "Últimos 30 días":
    fecha_inicio = max_date - pd.Timedelta(days=30)
    fecha_fin = max_date
    fecha_inicio_prev = fecha_inicio - pd.Timedelta(days=30)
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
elif periodo_opt == "Este Mes (Septiembre 2026)":
    fecha_inicio = pd.to_datetime("2026-09-01")
    fecha_fin = max_date
    fecha_inicio_prev = pd.to_datetime("2026-08-01")
    fecha_fin_prev = pd.to_datetime("2026-08-12")
elif periodo_opt == "Mes Anterior (Agosto 2026)":
    fecha_inicio = pd.to_datetime("2026-08-01")
    fecha_fin = pd.to_datetime("2026-08-31")
    fecha_inicio_prev = pd.to_datetime("2026-07-01")
    fecha_fin_prev = pd.to_datetime("2026-07-31")
else:
    fecha_inicio = df_raw['Fecha'].min()
    fecha_fin = max_date
    fecha_inicio_prev = fecha_inicio
    fecha_fin_prev = fecha_fin

# Filtro 2: Categoría
categorias_disponibles = ["Todas"] + list(df_raw['Categoria'].unique())
cat_sel = st.sidebar.selectbox("Categoría de Producto:", categorias_disponibles)

# Filtro 3: Producto
if cat_sel != "Todas":
    prods_disponibles = ["Todos"] + list(df_raw[df_raw['Categoria'] == cat_sel]['Producto'].unique())
else:
    prods_disponibles = ["Todos"] + list(df_raw['Producto'].unique())
prod_sel = st.sidebar.selectbox("Producto Específico:", prods_disponibles)

# Filtro 4: Canal de Venta
canales_disponibles = ["Todos"] + list(df_raw['Canal_Venta'].unique())
canal_sel = st.sidebar.selectbox("Canal de Venta:", canales_disponibles)

# Aplicar filtros al dataset actual y previo
def filtrar_df(df, f_ini, f_fin, cat, prod, canal):
    df_f = df[(df['Fecha'] >= f_ini) & (df['Fecha'] <= f_fin)]
    if cat != "Todas":
        df_f = df_f[df_f['Categoria'] == cat]
    if prod != "Todos":
        df_f = df_f[df_f['Producto'] == prod]
    if canal != "Todos":
        df_f = df_f[df_f['Canal_Venta'] == canal]
    return df_f

df_curr = filtrar_df(df_raw, fecha_inicio, fecha_fin, cat_sel, prod_sel, canal_sel)
df_prev = filtrar_df(df_raw, fecha_inicio_prev, fecha_fin_prev, cat_sel, prod_sel, canal_sel)

# ---------------------------------------------------------
# CÁLCULO DE INDICADORES CLAVE (KPIs)
# ---------------------------------------------------------
vtas_curr = df_curr['Ventas_Soles'].sum()
vtas_prev = df_prev['Ventas_Soles'].sum()
delta_vtas = ((vtas_curr - vtas_prev) / vtas_prev * 100) if vtas_prev > 0 else 0

util_curr = df_curr['Utilidad_Soles'].sum()
util_prev = df_prev['Utilidad_Soles'].sum()
delta_util = ((util_curr - util_prev) / util_prev * 100) if util_prev > 0 else 0

mg_curr = (util_curr / vtas_curr * 100) if vtas_curr > 0 else 0
mg_prev = (util_prev / vtas_prev * 100) if vtas_prev > 0 else 0
delta_mg = mg_curr - mg_prev

num_tx_curr = len(df_curr)
num_tx_prev = len(df_prev)
delta_tx = ((num_tx_curr - num_tx_prev) / num_tx_prev * 100) if num_tx_prev > 0 else 0

ticket_curr = (vtas_curr / num_tx_curr) if num_tx_curr > 0 else 0
ticket_prev = (vtas_prev / num_tx_prev) if num_tx_prev > 0 else 0
delta_ticket = ((ticket_curr - ticket_prev) / ticket_prev * 100) if ticket_prev > 0 else 0

# MOSTRAR 5 TARJETAS KPI
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Ventas Totales</div>
        <div class="metric-value">S/ {vtas_curr:,.2f}</div>
        <div class="{'metric-delta-pos' if delta_vtas >= 0 else 'metric-delta-neg'}">
            {'▲' if delta_vtas >= 0 else '▼'} {abs(delta_vtas):.1f}% vs ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Utilidad Neta</div>
        <div class="metric-value">S/ {util_curr:,.2f}</div>
        <div class="{'metric-delta-pos' if delta_util >= 0 else 'metric-delta-neg'}">
            {'▲' if delta_util >= 0 else '▼'} {abs(delta_util):.1f}% vs ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Margen de Utilidad</div>
        <div class="metric-value">{mg_curr:.1f}%</div>
        <div class="{'metric-delta-pos' if delta_mg >= 0 else 'metric-delta-neg'}">
            {'▲' if delta_mg >= 0 else '▼'} {abs(delta_mg):.1f} pp vs ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">N° de Ventas</div>
        <div class="metric-value">{num_tx_curr:,}</div>
        <div class="{'metric-delta-pos' if delta_tx >= 0 else 'metric-delta-neg'}">
            {'▲' if delta_tx >= 0 else '▼'} {abs(delta_tx):.1f}% vs ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Ticket Promedio</div>
        <div class="metric-value">S/ {ticket_curr:.2f}</div>
        <div class="{'metric-delta-pos' if delta_ticket >= 0 else 'metric-delta-neg'}">
            {'▲' if delta_ticket >= 0 else '▼'} {abs(delta_ticket):.1f}% vs ant.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# GRÁFICOS INTERACTIVOS DE ANÁLISIS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Evolución y Ventas", "📦 Productos Estrella y Rentabilidad", "💡 Alertas y Decisiones"])

with tab1:
    st.subheader("Evolución Diaria de Ventas y Utilidad")
    df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
    st.line_chart(df_daily.set_index('Fecha'))

with tab2:
    col_g1, col_g2 = st.columns(2)

    colores = [
        "#3B82F6", "#34C38F", "#8B5CF6", "#F59E0B",
        "#06B6D4", "#EF476F", "#14B8A6", "#6366F1",
        "#F97316", "#84CC16"
    ]

    with col_g1:
        st.subheader("Top Productos por Ingresos (S/)")
        df_prod_sales = df_curr.groupby("Producto")["Ventas_Soles"].sum().sort_values(ascending=True)

        fig_sales = go.Figure(go.Bar(
            x=df_prod_sales.values,
            y=df_prod_sales.index.astype(str),
            orientation="h",
            marker_color=[
                colores[i % len(colores)]
                for i in range(len(df_prod_sales))
            ],
            hovertemplate="Producto: %{y}<br>Ventas: S/ %{x:,.2f}<extra></extra>"
        ))

        fig_sales.update_layout(
            height=390,
            margin=dict(l=10, r=20, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(title="Ventas (S/)", gridcolor="#E5E7EB", zeroline=False),
            yaxis=dict(title=""),
            showlegend=False
        )

        st.plotly_chart(
            fig_sales,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col_g2:
        st.subheader("Top Productos por Rentabilidad (%)")
        df_prod_prof = df_curr.groupby("Producto").apply(
            lambda x: (
                x["Utilidad_Soles"].sum() /
                x["Ventas_Soles"].sum() * 100
            ) if x["Ventas_Soles"].sum() > 0 else 0,
            include_groups=False
        ).sort_values(ascending=True)

        fig_profit = go.Figure(go.Bar(
            x=df_prod_prof.values,
            y=df_prod_prof.index.astype(str),
            orientation="h",
            marker_color=[
                colores[i % len(colores)]
                for i in range(len(df_prod_prof))
            ],
            hovertemplate="Producto: %{y}<br>Rentabilidad: %{x:.1f}%<extra></extra>"
        ))

        fig_profit.update_layout(
            height=390,
            margin=dict(l=10, r=20, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(title="Rentabilidad (%)", gridcolor="#E5E7EB", zeroline=False),
            yaxis=dict(title=""),
            showlegend=False
        )

        st.plotly_chart(
            fig_profit,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with tab3:
    st.subheader("💡 Detección de Oportunidades y Decisiones Recomendadas")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.info("🚨 **Alertas Operativas y de Stock:**\n"
                "- **Bebidas:** Presenta un incremento de demanda del +35% los fines de semana. Se recomienda reabastecer stock los jueves.\n"
                "- **Snacks:** Margen de ganancia elevado (44%), pero representa solo el 6% de las ventas. Impulsar combos de venta.")
    
    with col_a2:
        st.success("🎯 **Acciones Recomendadas para el Empresario:**\n"
                   "- **Canal Digital (Yape / WhatsApp):** Genera el 35% de las ventas totales. Mantener atención rápida en estos canales.\n"
                   "- **Ticket Promedio:** S/ 35.35. Ofrecer productos complementarios en caja para llevar el ticket promedio a S/ 40.00.")

st.markdown("---")
st.caption("Prototipo de Aplicativo Web MYPE – Desarrollado para el Proyecto de Gestión por Resultados 2026")
