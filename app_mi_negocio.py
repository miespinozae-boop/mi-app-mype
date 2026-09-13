import streamlit as st
import pandas as pd
import numpy as np

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="NEXDATA | Inteligencia de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

REQUIRED_COLUMNS = [
    "Fecha",
    "Producto",
    "Categoria",
    "Canal_Venta",
    "Ventas_Soles",
    "Utilidad_Soles",
]

# =========================================================
# ESTILOS
# =========================================================
st.markdown(
    """
    <style>
        .main-header {
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 2px;
        }
        .sub-header {
            font-size: 14px;
            opacity: 0.70;
            margin-bottom: 18px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 750;
            margin-top: 8px;
            margin-bottom: 8px;
        }
        .insight {
            border: 1px solid rgba(128,128,128,.28);
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }
        .small-muted {
            font-size: 12px;
            opacity: .65;
        }
        .hero-box {
            border: 1px solid rgba(128,128,128,.25);
            border-radius: 14px;
            padding: 18px 20px;
            margin-bottom: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# CARGA Y VALIDACIÓN DE DATOS
# =========================================================
@st.cache_data
def load_csv(path):
    df = pd.read_csv(path)
    return prepare_data(df)


def prepare_data(df):
    df = df.copy()

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            "Faltan estas columnas obligatorias: " + ", ".join(missing)
        )

    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df["Ventas_Soles"] = pd.to_numeric(df["Ventas_Soles"], errors="coerce").fillna(0)
    df["Utilidad_Soles"] = pd.to_numeric(df["Utilidad_Soles"], errors="coerce").fillna(0)

    for col in ["Producto", "Categoria", "Canal_Venta"]:
        df[col] = df[col].fillna("Sin especificar").astype(str)

    df = df.dropna(subset=["Fecha"]).sort_values("Fecha").reset_index(drop=True)
    return df


def validate_data(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return missing


# =========================================================
# DATOS INICIALES
# =========================================================
try:
    df_base = load_csv("dataset_mype_transacciones.csv")
except Exception as e:
    st.error("No se pudo cargar el archivo de datos.")
    st.code(str(e))
    st.stop()

# =========================================================
# CARGAR LOS DATOS REALES DEL NEGOCIO
# =========================================================
st.sidebar.header("📥 Datos de tu negocio")
uploaded = st.sidebar.file_uploader(
    "Cargar Excel/CSV de tu negocio",
    type=["csv", "xlsx"],
    help="Puedes reemplazar los datos de demostración por los datos reales de tu negocio.",
)

if uploaded is not None:
    try:
        if uploaded.name.lower().endswith(".xlsx"):
            uploaded_df = pd.read_excel(uploaded)
        else:
            uploaded_df = pd.read_csv(uploaded)

        missing = validate_data(uploaded_df)
        if missing:
            st.sidebar.error("Faltan columnas: " + ", ".join(missing))
            df_source = df_base.copy()
        else:
            df_source = prepare_data(uploaded_df)
            st.sidebar.success("Datos cargados correctamente.")
    except Exception as e:
        st.sidebar.error(f"No se pudo leer el archivo: {e}")
        df_source = df_base.copy()
else:
    df_source = df_base.copy()

# =========================================================
# EDICIÓN EN TIEMPO REAL
# =========================================================
with st.sidebar.expander("✏️ Editar datos en tiempo real"):
    st.write(
        "Modifica una fila y presiona Enter o cambia de celda. "
        "Los indicadores del panel se recalcularán."
    )

    editor_key = f"editor_{uploaded.name if uploaded else 'demo'}"
    edited_df = st.data_editor(
        df_source,
        key=editor_key,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha"),
            "Ventas_Soles": st.column_config.NumberColumn(
                "Ventas (S/)", format="S/ %.2f"
            ),
            "Utilidad_Soles": st.column_config.NumberColumn(
                "Utilidad (S/)", format="S/ %.2f"
            ),
        },
    )

df_raw = prepare_data(edited_df)

if df_raw.empty:
    st.warning("No hay registros válidos para analizar.")
    st.stop()

# =========================================================
# ENCABEZADO
# =========================================================
st.markdown(
    '<div class="main-header">📊 NEXDATA – Inteligencia de Datos</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Convierte los datos de tu negocio en información, '
    "hallazgos y decisiones para tu negocio.</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-box">
        <b>Datos → Información → Hallazgos → Recomendaciones → Decisiones</b><br>
        <span class="small-muted">
        Panel demostrativo de NEXDATA para convertir datos en decisiones.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# FILTROS
# =========================================================
st.sidebar.header("🔍 Filtros de negocio")

max_date = df_raw["Fecha"].max()
min_date = df_raw["Fecha"].min()

periodos = [
    "Últimos 30 días",
    "Mes actual",
    "Mes anterior",
    "Todo el registro",
]
periodo_sel = st.sidebar.selectbox("Periodo", periodos)

if periodo_sel == "Últimos 30 días":
    fecha_fin = max_date
    fecha_inicio = max_date - pd.Timedelta(days=29)
    periodo_anterior_dias = (fecha_fin - fecha_inicio).days + 1
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    fecha_inicio_prev = fecha_fin_prev - pd.Timedelta(days=periodo_anterior_dias - 1, unit="D")
elif periodo_sel == "Mes actual":
    fecha_inicio = max_date.replace(day=1)
    fecha_fin = max_date
    dias = (fecha_fin - fecha_inicio).days + 1
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    fecha_inicio_prev = fecha_fin_prev - pd.Timedelta(days=dias - 1, unit="D")
elif periodo_sel == "Mes anterior":
    primer_dia_mes_actual = max_date.replace(day=1)
    fecha_fin = primer_dia_mes_actual - pd.Timedelta(days=1)
    fecha_inicio = fecha_fin.replace(day=1)
    dias = (fecha_fin - fecha_inicio).days + 1
    fecha_fin_prev = fecha_inicio - pd.Timedelta(days=1)
    fecha_inicio_prev = fecha_fin_prev - pd.Timedelta(days=dias - 1, unit="D")
else:
    fecha_inicio = min_date
    fecha_fin = max_date
    fecha_inicio_prev = min_date
    fecha_fin_prev = max_date

categorias = ["Todas"] + sorted(df_raw["Categoria"].dropna().unique().tolist())
cat_sel = st.sidebar.selectbox("Categoría", categorias)

productos_filtrados = (
    df_raw[df_raw["Categoria"] == cat_sel]["Producto"].unique().tolist()
    if cat_sel != "Todas"
    else df_raw["Producto"].unique().tolist()
)
productos = ["Todos"] + sorted(productos_filtrados)
prod_sel = st.sidebar.selectbox("Producto", productos)

canales = ["Todos"] + sorted(df_raw["Canal_Venta"].dropna().unique().tolist())
canal_sel = st.sidebar.selectbox("Canal de venta", canales)

def filter_df(df, start, end, category="Todas", product="Todos", channel="Todos"):
    out = df[(df["Fecha"] >= start) & (df["Fecha"] <= end)].copy()
    if category != "Todas":
        out = out[out["Categoria"] == category]
    if product != "Todos":
        out = out[out["Producto"] == product]
    if channel != "Todos":
        out = out[out["Canal_Venta"] == channel]
    return out

df_curr = filter_df(
    df_raw, fecha_inicio, fecha_fin, cat_sel, prod_sel, canal_sel
)
df_prev = filter_df(
    df_raw, fecha_inicio_prev, fecha_fin_prev, cat_sel, prod_sel, canal_sel
)

if df_curr.empty:
    st.warning("No existen datos para los filtros seleccionados.")
    st.stop()

# =========================================================
# KPIs
# =========================================================
def pct_change(current, previous):
    if previous == 0:
        return np.nan if current == 0 else np.inf
    return (current - previous) / previous * 100

ventas = df_curr["Ventas_Soles"].sum()
ventas_prev = df_prev["Ventas_Soles"].sum()
utilidad = df_curr["Utilidad_Soles"].sum()
utilidad_prev = df_prev["Utilidad_Soles"].sum()
margen = utilidad / ventas * 100 if ventas else 0
margen_prev = utilidad_prev / ventas_prev * 100 if ventas_prev else 0
transacciones = len(df_curr)
transacciones_prev = len(df_prev)
ticket = ventas / transacciones if transacciones else 0
ticket_prev = ventas_prev / transacciones_prev if transacciones_prev else 0

delta_ventas = pct_change(ventas, ventas_prev)
delta_utilidad = pct_change(utilidad, utilidad_prev)
delta_transacciones = pct_change(transacciones, transacciones_prev)
delta_ticket = pct_change(ticket, ticket_prev)
delta_margen = margen - margen_prev

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("VENTAS TOTALES", f"S/ {ventas:,.2f}", f"{delta_ventas:.1f}%" if np.isfinite(delta_ventas) else "Nuevo periodo")
k2.metric("UTILIDAD NETA", f"S/ {utilidad:,.2f}", f"{delta_utilidad:.1f}%" if np.isfinite(delta_utilidad) else "Nuevo periodo")
k3.metric("MARGEN DE UTILIDAD", f"{margen:.1f}%", f"{delta_margen:.1f} pp")
k4.metric("N.º DE VENTAS", f"{transacciones:,}", f"{delta_transacciones:.1f}%" if np.isfinite(delta_transacciones) else "Nuevo periodo")
k5.metric("TICKET PROMEDIO", f"S/ {ticket:.2f}", f"{delta_ticket:.1f}%" if np.isfinite(delta_ticket) else "Nuevo periodo")

st.caption(
    f"Periodo analizado: {fecha_inicio.strftime('%d/%m/%Y')} – "
    f"{fecha_fin.strftime('%d/%m/%Y')} | Registros: {len(df_curr):,}"
)

# =========================================================
# PESTAÑAS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📈 Dashboard",
        "📦 Productos y rentabilidad",
        "💡 ¿Qué me dicen mis datos?",
        "🔮 Simulador",
        "✏️ Datos",
    ]
)

# =========================================================
# TAB 1: DASHBOARD
# =========================================================
with tab1:
    st.subheader("Evolución de ventas y utilidad")

    daily = (
        df_curr.groupby(df_curr["Fecha"].dt.date)[["Ventas_Soles", "Utilidad_Soles"]]
        .sum()
        .sort_index()
    )
    st.line_chart(daily)

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Ventas por canal")
        channel_sales = df_curr.groupby("Canal_Venta")["Ventas_Soles"].sum().sort_values(ascending=False)
        st.bar_chart(channel_sales)

    with c2:
        st.subheader("Ventas por categoría")
        category_sales = df_curr.groupby("Categoria")["Ventas_Soles"].sum().sort_values(ascending=False)
        st.bar_chart(category_sales)

# =========================================================
# TAB 2: PRODUCTOS
# =========================================================
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🏆 Productos estrella por ventas")
        prod_sales = (
            df_curr.groupby("Producto")["Ventas_Soles"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(prod_sales)

        if not prod_sales.empty:
            top_product = prod_sales.index[0]
            top_value = prod_sales.iloc[0]
            st.info(f"Producto líder: **{top_product}**, con S/ {top_value:,.2f} en ventas.")

    with c2:
        st.subheader("💰 Margen por producto")
        prod_profit = (
            df_curr.groupby("Producto")[["Ventas_Soles", "Utilidad_Soles"]]
            .sum()
        )
        prod_profit["Margen_%"] = np.where(
            prod_profit["Ventas_Soles"] > 0,
            prod_profit["Utilidad_Soles"] / prod_profit["Ventas_Soles"] * 100,
            0,
        )
        margin_chart = prod_profit["Margen_%"].sort_values(ascending=False)
        st.bar_chart(margin_chart)

    st.subheader("Tabla de rentabilidad")
    table = prod_profit.copy()
    table["Participación_Ventas_%"] = np.where(
        ventas > 0, table["Ventas_Soles"] / ventas * 100, 0
    )
    table = table.sort_values("Ventas_Soles", ascending=False)
    st.dataframe(
        table.style.format(
            {
                "Ventas_Soles": "S/ {:,.2f}",
                "Utilidad_Soles": "S/ {:,.2f}",
                "Margen_%": "{:.1f}%",
                "Participación_Ventas_%": "{:.1f}%",
            }
        ),
        use_container_width=True,
    )

# =========================================================
# TAB 3: INSIGHTS AUTOMÁTICOS
# =========================================================
with tab3:
    st.subheader("💡 ¿Qué me dicen mis datos?")

    # 1. Ventas vs utilidad
    if ventas > 0 and utilidad > 0:
        if margen < margen_prev - 1:
            st.warning(
                f"⚠️ **Alerta de rentabilidad:** el margen actual es {margen:.1f}% "
                f"frente a {margen_prev:.1f}% del periodo anterior. "
                "Las ventas pueden estar creciendo sin traducirse en una mejor rentabilidad."
            )
        elif margen > margen_prev + 1:
            st.success(
                f"🟢 **Oportunidad:** el margen mejoró a {margen:.1f}%. "
                "Revisa qué productos o canales están impulsando esta mejora."
            )
        else:
            st.info(
                f"🔵 **Estabilidad:** el margen se mantiene alrededor de {margen:.1f}%."
            )

    # 2. Producto líder
    if not prod_sales.empty:
        top_product = prod_sales.index[0]
        top_share = prod_sales.iloc[0] / ventas * 100 if ventas else 0
        st.info(
            f"🏆 **Producto líder:** {top_product} concentra aproximadamente "
            f"{top_share:.1f}% de las ventas del periodo."
        )

    # 3. Producto con mayor margen
    if not margin_chart.empty:
        best_margin_product = margin_chart.index[0]
        best_margin = margin_chart.iloc[0]
        st.success(
            f"💰 **Mayor margen:** {best_margin_product} presenta un margen aproximado "
            f"de {best_margin:.1f}%. Evalúa si puede impulsarse con promociones o combos."
        )

    # 4. Canal líder
    channel_sales = df_curr.groupby("Canal_Venta")["Ventas_Soles"].sum().sort_values(ascending=False)
    if not channel_sales.empty:
        best_channel = channel_sales.index[0]
        channel_share = channel_sales.iloc[0] / ventas * 100 if ventas else 0
        st.info(
            f"🛍️ **Canal principal:** {best_channel} representa aproximadamente "
            f"{channel_share:.1f}% de las ventas."
        )

    # 5. Ticket
    if ticket < 40:
        st.warning(
            f"🟡 **Ticket promedio:** S/ {ticket:.2f}. "
            "Una estrategia posible es ofrecer productos complementarios o combos "
            "para elevar el valor de cada compra."
        )
    else:
        st.success(
            f"🟢 **Ticket promedio saludable:** S/ {ticket:.2f}. "
            "Analiza qué productos están elevando el valor de cada compra."
        )

    # Recomendaciones
    st.markdown("---")
    st.subheader("🎯 Acciones recomendadas")

    recommendations = []

    if margen < margen_prev:
        recommendations.append(
            "Revisar costos y precios de los productos con mayor volumen de ventas."
        )
    if ticket < 40:
        recommendations.append(
            "Probar combos, ventas cruzadas o productos complementarios para elevar el ticket."
        )
    if not prod_sales.empty:
        recommendations.append(
            f"Proteger el stock y disponibilidad de **{prod_sales.index[0]}**, "
            "porque es el producto con mayor facturación."
        )
    if not margin_chart.empty:
        recommendations.append(
            f"Evaluar promociones para **{margin_chart.index[0]}**, "
            "que presenta el mayor margen dentro del periodo."
        )

    for i, recommendation in enumerate(recommendations, 1):
        st.write(f"**{i}.** {recommendation}")

    st.caption(
        "Las alertas y recomendaciones se calculan automáticamente a partir de los datos "
        "seleccionados; no son textos fijos."
    )

# =========================================================
# TAB 4: SIMULADOR
# =========================================================
with tab4:
    st.subheader("🔮 Simula una decisión")
    st.write(
        "Modifica variables para observar cómo podría cambiar el resultado del negocio."
    )

    s1, s2 = st.columns(2)

    with s1:
        precio_factor = st.slider(
            "Variación del precio (%)",
            min_value=-30,
            max_value=30,
            value=0,
            step=1,
        )
        ventas_factor = st.slider(
            "Variación de cantidad vendida (%)",
            min_value=-50,
            max_value=100,
            value=0,
            step=5,
        )

    with s2:
        costo_factor = st.slider(
            "Variación de costos (%)",
            min_value=-30,
            max_value=30,
            value=0,
            step=1,
        )
        otros_factor = st.slider(
            "Ajuste adicional de demanda (%)",
            min_value=-20,
            max_value=20,
            value=0,
            step=1,
        )

    demanda_total = (1 + ventas_factor / 100) * (1 + otros_factor / 100)
    ventas_sim = ventas * (1 + precio_factor / 100) * demanda_total
    utilidad_sim = (
        utilidad
        + ventas * (demanda_total - 1) * (margen / 100)
        + ventas * (precio_factor / 100) * demanda_total
        - (ventas * demanda_total * (costo_factor / 100))
    )
    margen_sim = utilidad_sim / ventas_sim * 100 if ventas_sim else 0

    delta_ventas_sim = ventas_sim - ventas
    delta_util_sim = utilidad_sim - utilidad

    r1, r2, r3 = st.columns(3)
    r1.metric("Ventas proyectadas", f"S/ {ventas_sim:,.2f}", f"{delta_ventas_sim:,.2f}")
    r2.metric("Utilidad proyectada", f"S/ {utilidad_sim:,.2f}", f"{delta_util_sim:,.2f}")
    r3.metric("Margen proyectado", f"{margen_sim:.1f}%", f"{margen_sim - margen:.1f} pp")

    if utilidad_sim > utilidad:
        st.success("🟢 El escenario simulado mejora la utilidad respecto al escenario actual.")
    elif utilidad_sim < utilidad:
        st.warning("🟡 El escenario simulado reduce la utilidad. Revisa las variables antes de tomar una decisión.")
    else:
        st.info("🔵 El escenario simulado mantiene la utilidad.")

    comparison = pd.DataFrame(
        {
            "Escenario": ["Actual", "Simulado"],
            "Ventas": [ventas, ventas_sim],
            "Utilidad": [utilidad, utilidad_sim],
            "Margen": [margen, margen_sim],
        }
    ).set_index("Escenario")

    st.subheader("Comparación")
    st.dataframe(
        comparison.style.format(
            {
                "Ventas": "S/ {:,.2f}",
                "Utilidad": "S/ {:,.2f}",
                "Margen": "{:.1f}%",
            }
        ),
        use_container_width=True,
    )

# =========================================================
# TAB 5: DATOS
# =========================================================
with tab5:
    st.subheader("✏️ Datos del negocio")
    st.write(
        "Edita los registros directamente. Al realizar un cambio, vuelve a "
        "seleccionar la pestaña Dashboard para observar el impacto en los indicadores."
    )

    edited_df_main = st.data_editor(
        df_raw,
        key="editor_principal",
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha"),
            "Ventas_Soles": st.column_config.NumberColumn(
                "Ventas (S/)", format="S/ %.2f"
            ),
            "Utilidad_Soles": st.column_config.NumberColumn(
                "Utilidad (S/)", format="S/ %.2f"
            ),
        },
    )

    st.download_button(
        "⬇️ Descargar datos actuales en CSV",
        data=edited_df_main.to_csv(index=False).encode("utf-8"),
        file_name="datos_mype_actualizados.csv",
        mime="text/csv",
    )

# =========================================================
# PIE
# =========================================================
st.markdown("---")
st.caption(
    "NEXDATA | Inteligencia de Datos | "
    "Gestión por Resultados 2026"
)
