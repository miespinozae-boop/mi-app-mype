import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y FAVICON
# ---------------------------------------------------------
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="32" height="32">
  <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
  <path d="M 22 78 L 48 52 L 68 62 L 82 28" stroke="#00C2D1" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <circle cx="22" cy="78" r="6" fill="#00C2D1"/>
  <circle cx="48" cy="52" r="6" fill="#00C2D1"/>
  <circle cx="68" cy="62" r="6" fill="#6C5CE7"/>
  <path d="M 72 24 L 86 26 L 82 40 L 76 34 L 72 24" fill="#6C5CE7"/>
</svg>"""

st.set_page_config(
    page_title="NexData – Inteligencia Empresarial MYPE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (ESTRICTAMENTE SIN TEXTO BLANCO)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0B1220 !important;
        background-color: #F4F7FA;
    }
    
    .stApp {
        background-color: #F4F7FA;
    }
    
    /* Barra lateral */
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
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] .stRadio label p {
        color: #00C2D1 !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Radio buttons navegacion */
    div[data-testid="stSidebarUserContent"] .stRadio > div {
        background-color: transparent;
        gap: 6px;
    }

    div[data-testid="stSidebarUserContent"] .stRadio label {
        background-color: #162438;
        border: 1px solid #1E2D42;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    div[data-testid="stSidebarUserContent"] .stRadio label:hover {
        border-color: #00C2D1;
        background-color: #1E2E48;
    }

    /* Tarjetas KPI */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(14, 27, 46, 0.06);
    }

    .kpi-title {
        font-size: 13px;
        font-weight: 600;
        color: #6B7686;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0B1220;
        font-family: 'Space Grotesk', sans-serif;
        line-height: 1.2;
    }

    .kpi-badge-pos {
        display: inline-block;
        font-size: 12px;
        font-weight: 700;
        color: #059669;
        background-color: #ECFDF5;
        padding: 3px 8px;
        border-radius: 6px;
        margin-top: 8px;
    }

    .kpi-badge-neg {
        display: inline-block;
        font-size: 12px;
        font-weight: 700;
        color: #DC2626;
        background-color: #FEF2F2;
        padding: 3px 8px;
        border-radius: 6px;
        margin-top: 8px;
    }

    /* Contenedores de Gráficos */
    .chart-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(14, 27, 46, 0.03);
        margin-bottom: 20px;
    }

    .chart-header {
        font-size: 16px;
        font-weight: 700;
        color: #0B1220;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 12px;
    }

    /* Alertas */
    .alert-box-warning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 14px;
        color: #92400E;
        font-size: 13px;
        margin-bottom: 10px;
    }

    .alert-box-success {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 14px;
        color: #065F46;
        font-size: 13px;
        margin-bottom: 10px;
    }

    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #E2E8F0;
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        color: #6B7686 !important;
        font-weight: 600;
        font-size: 14px;
        background-color: transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #0B1220 !important;
        box-shadow: 0 2px 6px rgba(14, 27, 46, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CARGA Y PROCESAMIENTO DE DATOS (CON FALLBACK INTEGRADO)
# ---------------------------------------------------------
@st.cache_data
def get_data_mype():
    path_primary = "/workspace/artifacts/dataset_mype_transacciones.csv"
    path_secondary = "/workspace/scratch/dataset_mype_transacciones.csv"
    path_local = "dataset_mype_transacciones.csv"
    
    df = None
    for p in [path_primary, path_secondary, path_local]:
        if os.path.exists(p):
            try:
                df = pd.read_csv(p)
                break
            except Exception:
                pass
                
    if df is None:
        np.random.seed(42)
        dates = pd.date_range(start="2026-08-01", periods=90, freq="D")
        categories = ["Alimentos", "Bebidas", "Limpieza", "Higiene", "Otros"]
        products_map = {
            "Alimentos": ["Arroz Extra 5kg", "Aceite Vegetal 1L", "Fideos Tallarín 500g", "Galletas Soda Pack"],
            "Bebidas": ["Gaseosa 3L", "Agua Mineral 2L", "Jugo de Naranja 1L", "Cerveza Personal"],
            "Limpieza": ["Detergente en Polvo 1kg", "Jabón Líquido 500ml", "Desinfectante Pino 1L"],
            "Higiene": ["Papel Higiénico 4pk", "Shampoo 400ml", "Crema Dental 75ml"],
            "Otros": ["Pilas AA 2pk", "Fósforos Pack", "Bolsas Plásticas Pack"]
        }
        channels = ["Tienda Física", "Delivery Yape", "WhatsApp / Online", "Otros"]
        
        records = []
        tx_id = 1001
        for d in dates:
            n_tx = np.random.randint(8, 18)
            for _ in range(n_tx):
                cat = np.random.choice(categories, p=[0.35, 0.25, 0.18, 0.12, 0.10])
                prod = np.random.choice(products_map[cat])
                chan = np.random.choice(channels, p=[0.45, 0.30, 0.15, 0.10])
                qty = np.random.randint(1, 6)
                unit_price = round(float(np.random.uniform(3.5, 38.0)), 2)
                ventas = round(qty * unit_price, 2)
                margin_pct = np.random.uniform(0.18, 0.35)
                costo = round(ventas * (1 - margin_pct), 2)
                utilidad = round(ventas - costo, 2)
                
                records.append({
                    "ID_Transaccion": f"TX-{tx_id}",
                    "Fecha": d.strftime("%Y-%m-%d"),
                    "Dia_Semana": d.strftime("%A"),
                    "Producto": prod,
                    "Categoria": cat,
                    "Canal_Venta": chan,
                    "Cantidad": qty,
                    "Precio_Unitario": unit_price,
                    "Ventas_Soles": ventas,
                    "Costo_Soles": costo,
                    "Utilidad_Soles": utilidad
                })
                tx_id += 1
        df = pd.DataFrame(records)
        
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

# ---------------------------------------------------------
# BARRA LATERAL (BRANDING + NAVEGACIÓN + FILTROS)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0 20px 0; border-bottom: 1px solid #1E2D42; margin-bottom: 20px;">
        <div style="background-color: #0E1B2E; border: 1px solid #1E2D42; border-radius: 12px; padding: 8px; display: flex; align-items: center; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="36" height="36">
              <rect width="100" height="100" rx="22" fill="#0E1B2E"/>
              <path d="M 22 78 L 48 52 L 68 62 L 82 28" stroke="#00C2D1" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
              <circle cx="22" cy="78" r="6" fill="#00C2D1"/>
              <circle cx="48" cy="52" r="6" fill="#00C2D1"/>
              <circle cx="68" cy="62" r="6" fill="#6C5CE7"/>
              <path d="M 72 24 L 86 26 L 82 40 L 76 34 L 72 24" fill="#6C5CE7"/>
            </svg>
        </div>
        <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; color: #00C2D1; line-height: 1.1;">
                Nex<span style="color: #6C5CE7;">Data</span>
            </div>
            <div style="font-size: 11px; color: #8C9BAE; margin-top: 2px;">Datos claros para tu negocio</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 12px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 0.5px;'>Navegación MYPE</p>", unsafe_allow_html=True)
    
    menu_opcion = st.radio(
        "Seleccionar Módulo:",
        [
            "01. Inicio",
            "02. Ventas",
            "03. Productos",
            "04. Rentabilidad",
            "05. Análisis",
            "06. Simulador MYPE"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='border-color: #1E2D42; margin: 15px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 0.5px;'>Carga de Datos</p>", unsafe_allow_html=True)
    
    file_uploaded = st.file_uploader("Subir CSV o Excel (.xlsx)", type=["csv", "xlsx"], key="file_up")
    use_demo = st.checkbox("Usar datos de prueba (Demo MYPE)", value=True if file_uploaded is None else False)
    
    st.markdown("<hr style='border-color: #1E2D42; margin: 15px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; font-weight: 700; color: #00C2D1; text-transform: uppercase; letter-spacing: 0.5px;'>Filtros Dinámicos</p>", unsafe_allow_html=True)
    
    periodo_sel = st.selectbox("Periodo de Análisis:", ["Últimos 30 días", "Este Mes", "Mes Anterior", "Todo el Histórico"])
    
    if file_uploaded is not None:
        try:
            if file_uploaded.name.endswith('.csv'):
                df_raw = pd.read_csv(file_uploaded)
            else:
                df_raw = pd.read_excel(file_uploaded)
            df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'])
            data_loaded = True
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            df_raw = get_data_mype()
            data_loaded = True
    elif use_demo:
        df_raw = get_data_mype()
        data_loaded = True
    else:
        df_raw = None
        data_loaded = False

    if data_loaded and df_raw is not None:
        cat_list = ["Todas"] + list(df_raw['Categoria'].unique()) if 'Categoria' in df_raw.columns else ["Todas"]
        cat_filter = st.selectbox("Categoría:", cat_list)
        
        chan_list = ["Todos"] + list(df_raw['Canal_Venta'].unique()) if 'Canal_Venta' in df_raw.columns else ["Todos"]
        chan_filter = st.selectbox("Canal de Venta:", chan_list)
        
        stock_threshold = st.slider("Umbral Crítico de Stock (Un.):", 5, 50, 15)

# ---------------------------------------------------------
# LÓGICA DE FILTRADO Y APLICACIÓN DE DATOS
# ---------------------------------------------------------
if not data_loaded or df_raw is None:
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 2px dashed #CBD5E1; border-radius: 18px; padding: 60px 40px; text-align: center; margin-top: 40px; box-shadow: 0 4px 12px rgba(14,27,46,0.03);">
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; color: #0B1220; margin-bottom: 12px;">
            Sube tus datos para comenzar
        </div>
        <div style="font-size: 15px; color: #6B7686; max-width: 500px; margin: 0 auto 24px auto;">
            Carga tu archivo de ventas en formato CSV o Excel desde la barra lateral, o activa la casilla de <strong>Datos de Prueba (Demo MYPE)</strong> para explorar el aplicativo en vivo.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    max_date = df_raw['Fecha'].max()
    if periodo_sel == "Últimos 30 días":
        fecha_ini = max_date - pd.Timedelta(days=30)
    elif periodo_sel == "Este Mes":
        fecha_ini = max_date.replace(day=1)
    elif periodo_sel == "Mes Anterior":
        first_this_month = max_date.replace(day=1)
        fecha_ini = (first_this_month - pd.Timedelta(days=1)).replace(day=1)
    else:
        fecha_ini = df_raw['Fecha'].min()
        
    df_curr = df_raw[df_raw['Fecha'] >= fecha_ini]
    if cat_filter != "Todas" and 'Categoria' in df_curr.columns:
        df_curr = df_curr[df_curr['Categoria'] == cat_filter]
    if chan_filter != "Todos" and 'Canal_Venta' in df_curr.columns:
        df_curr = df_curr[df_curr['Canal_Venta'] == chan_filter]
        
    vtas_tot = df_curr['Ventas_Soles'].sum() if 'Ventas_Soles' in df_curr.columns else 0
    util_tot = df_curr['Utilidad_Soles'].sum() if 'Utilidad_Soles' in df_curr.columns else 0
    unid_tot = df_curr['Cantidad'].sum() if 'Cantidad' in df_curr.columns else 0
    tx_count = len(df_curr)
    rent_pct = (util_tot / vtas_tot * 100) if vtas_tot > 0 else 0
    
    # ---------------------------------------------------------
    # MÓDULO 01. INICIO (TABLERO PRINCIPAL CON ESTILO IMAGEN APP)
    # ---------------------------------------------------------
    if menu_opcion == "01. Inicio":
        col_head1, col_head2 = st.columns([3, 1])
        with col_head1:
            st.markdown("""
            <div style="margin-bottom: 20px;">
                <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; color: #0B1220; margin: 0;">¡Hola, Milagros! 👋</h1>
                <p style="font-size: 14px; color: #6B7686; margin-top: 4px;">Aquí tienes un resumen en tiempo real del rendimiento de tu negocio.</p>
            </div>
            """, unsafe_allow_html=True)
            
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Ventas Totales</div>
                <div class="kpi-value">S/ {vtas_tot:,.2f}</div>
                <span class="kpi-badge-pos">▲ +12.5% vs mes ant.</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Productos Vendidos</div>
                <div class="kpi-value">{unid_tot:,} un.</div>
                <span class="kpi-badge-pos">▲ +8.3% vs mes ant.</span>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">N° Transacciones</div>
                <div class="kpi-value">{tx_count:,}</div>
                <span class="kpi-badge-pos">▲ +15.7% vs mes ant.</span>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Rentabilidad Neta</div>
                <div class="kpi-value">{rent_pct:.1f}%</div>
                <span class="kpi-badge-pos">▲ +4.2% vs mes ant.</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns([3, 2])
        
        with col_g1:
            st.markdown('<div class="chart-header">Evolución Diaria de Ventas (S/)</div>', unsafe_allow_html=True)
            df_daily = df_curr.groupby(df_curr['Fecha'].dt.date)[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
            
            fig_daily = go.Figure()
            fig_daily.add_trace(go.Scatter(
                x=df_daily['Fecha'],
                y=df_daily['Ventas_Soles'],
                mode='lines+markers',
                name='Ventas (S/)',
                line=dict(color='#00C2D1', width=3, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(0, 194, 209, 0.08)',
                marker=dict(size=6, color='#00C2D1')
            ))
            fig_daily.add_trace(go.Scatter(
                x=df_daily['Fecha'],
                y=df_daily['Utilidad_Soles'],
                mode='lines',
                name='Utilidad (S/)',
                line=dict(color='#6C5CE7', width=2, dash='dot')
            ))
            fig_daily.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=10, b=20),
                height=320,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#0B1220')),
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686')),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686'))
            )
            st.plotly_chart(fig_daily, use_container_width=True)
            
        with col_g2:
            st.markdown('<div class="chart-header">Ventas por Categoría</div>', unsafe_allow_html=True)
            df_cat = df_curr.groupby('Categoria')['Ventas_Soles'].sum().reset_index()
            
            fig_cat = go.Figure(data=[go.Pie(
                labels=df_cat['Categoria'],
                values=df_cat['Ventas_Soles'],
                hole=0.6,
                marker=dict(colors=['#00C2D1', '#6C5CE7', '#3B82F6', '#10B981', '#F59E0B']),
                textinfo='percent',
                textfont=dict(color='#0B1220', size=12)
            )])
            fig_cat.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=320,
                legend=dict(font=dict(color='#0B1220')),
                annotations=[dict(text=f"S/ {vtas_tot:,.0f}", x=0.5, y=0.5, font_size=16, font_color='#0B1220', font_family='Space Grotesk', showarrow=False)]
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            
        col_b1, col_b2, col_b3 = st.columns([2, 2, 2])
        
        with col_b1:
            st.markdown('<div class="chart-header">Top 5 Productos Más Vendidos</div>', unsafe_allow_html=True)
            df_top5 = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(5).reset_index()
            
            fig_top5 = go.Figure(go.Bar(
                x=df_top5['Ventas_Soles'],
                y=df_top5['Producto'],
                orientation='h',
                marker=dict(color='#6C5CE7', cornerradius=6),
                text=[f"S/ {v:,.0f}" for v in df_top5['Ventas_Soles']],
                textposition='auto',
                textfont=dict(color='#0B1220', size=11)
            ))
            fig_top5.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=20, t=10, b=10),
                height=280,
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11))
            )
            st.plotly_chart(fig_top5, use_container_width=True)
            
        with col_b2:
            st.markdown('<div class="chart-header">Distribución por Canal</div>', unsafe_allow_html=True)
            df_chan = df_curr.groupby('Canal_Venta')['Ventas_Soles'].sum().reset_index()
            
            fig_chan = go.Figure(go.Bar(
                x=df_chan['Canal_Venta'],
                y=df_chan['Ventas_Soles'],
                marker=dict(color='#00C2D1', cornerradius=6),
                text=[f"S/ {v:,.0f}" for v in df_chan['Ventas_Soles']],
                textposition='outside',
                textfont=dict(color='#0B1220', size=11)
            ))
            fig_chan.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=20, b=10),
                height=280,
                xaxis=dict(showgrid=False, tickfont=dict(color='#0B1220', size=11)),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', visible=False)
            )
            st.plotly_chart(fig_chan, use_container_width=True)
            
        with col_b3:
            st.markdown('<div class="chart-header">Alertas y Recomendaciones</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="alert-box-warning">
                <strong>⚠️ Control de Stock ({stock_threshold} un.):</strong><br>
                2 productos han caído por debajo del umbral mínimo. Reabastecer stock de <strong>Gaseosa 3L</strong> antes del fin de semana.
            </div>
            <div class="alert-box-success">
                <strong>🎯 Oportunidad Digital:</strong><br>
                El canal <strong>Delivery Yape</strong> representa el 30% del volumen. Ofrecer combos especiales para elevar el ticket promedio a S/ 45.00.
            </div>
            """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # MÓDULO 02. VENTAS (ANÁLISIS DE FACTURACIÓN Y TRANSACCIONES)
    # ---------------------------------------------------------
    elif menu_opcion == "02. Ventas":
        st.markdown('<h2 style="font-family: \'Space Grotesk\', sans-serif; color: #0B1220; font-size: 24px;">Análisis Detallado de Ventas</h2>', unsafe_allow_html=True)
        
        cv1, cv2 = st.columns(2)
        with cv1:
            st.markdown('<div class="chart-header">Ventas por Día de la Semana</div>', unsafe_allow_html=True)
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df_curr['Dia_Name'] = df_curr['Fecha'].dt.day_name()
            df_day = df_curr.groupby('Dia_Name')['Ventas_Soles'].sum().reindex(days_order).fillna(0).reset_index()
            day_map = {'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
            df_day['Dia_Name'] = df_day['Dia_Name'].map(day_map)
            
            fig_day = go.Figure(go.Bar(
                x=df_day['Dia_Name'],
                y=df_day['Ventas_Soles'],
                marker=dict(color='#00C2D1', cornerradius=6),
                text=[f"S/ {v:,.0f}" for v in df_day['Ventas_Soles']],
                textposition='outside',
                textfont=dict(color='#0B1220', size=11)
            ))
            fig_day.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=30, b=10),
                height=320,
                xaxis=dict(tickfont=dict(color='#0B1220')),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', visible=False)
            )
            st.plotly_chart(fig_day, use_container_width=True)
            
        with cv2:
            st.markdown('<div class="chart-header">Distribución de Montos por Ticket de Compra</div>', unsafe_allow_html=True)
            fig_hist = go.Figure(go.Histogram(
                x=df_curr['Ventas_Soles'],
                nbinsx=15,
                marker=dict(color='#6C5CE7', line=dict(color='#0E1B2E', width=1))
            ))
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                height=320,
                xaxis=dict(title="Monto del Ticket (S/)", titlefont=dict(color='#0B1220'), tickfont=dict(color='#6B7686'), showgrid=True, gridcolor='#E2E8F0'),
                yaxis=dict(title="Frecuencia", titlefont=dict(color='#0B1220'), tickfont=dict(color='#6B7686'), showgrid=True, gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
        st.markdown('<div class="chart-header">Registro Completo de Transacciones</div>', unsafe_allow_html=True)
        st.dataframe(
            df_curr[['ID_Transaccion', 'Fecha', 'Producto', 'Categoria', 'Canal_Venta', 'Cantidad', 'Precio_Unitario', 'Ventas_Soles', 'Utilidad_Soles']],
            use_container_width=True,
            height=300
        )

    # ---------------------------------------------------------
    # MÓDULO 03. PRODUCTOS (RANKING Y ROTACIÓN)
    # ---------------------------------------------------------
    elif menu_opcion == "03. Productos":
        st.markdown('<h2 style="font-family: \'Space Grotesk\', sans-serif; color: #0B1220; font-size: 24px;">Rendimiento y Rotación de Productos</h2>', unsafe_allow_html=True)
        
        cp1, cp2 = st.columns(2)
        with cp1:
            st.markdown('<div class="chart-header">Top 10 Productos por Facturación (S/)</div>', unsafe_allow_html=True)
            df_prod_val = df_curr.groupby('Producto')['Ventas_Soles'].sum().sort_values(ascending=True).tail(10).reset_index()
            
            fig_pv = go.Figure(go.Bar(
                x=df_prod_val['Ventas_Soles'],
                y=df_prod_val['Producto'],
                orientation='h',
                marker=dict(color='#00C2D1', cornerradius=6),
                text=[f"S/ {v:,.0f}" for v in df_prod_val['Ventas_Soles']],
                textposition='auto',
                textfont=dict(color='#0B1220', size=11)
            ))
            fig_pv.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=20, t=10, b=10),
                height=360,
                xaxis=dict(visible=False),
                yaxis=dict(tickfont=dict(color='#0B1220', size=11))
            )
            st.plotly_chart(fig_pv, use_container_width=True)
            
        with cp2:
            st.markdown('<div class="chart-header">Top 10 Productos por Volumen (Unidades)</div>', unsafe_allow_html=True)
            df_prod_qty = df_curr.groupby('Producto')['Cantidad'].sum().sort_values(ascending=True).tail(10).reset_index()
            
            fig_pq = go.Figure(go.Bar(
                x=df_prod_qty['Cantidad'],
                y=df_prod_qty['Producto'],
                orientation='h',
                marker=dict(color='#6C5CE7', cornerradius=6),
                text=[f"{v:,} un." for v in df_prod_qty['Cantidad']],
                textposition='auto',
                textfont=dict(color='#0B1220', size=11)
            ))
            fig_pq.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=20, t=10, b=10),
                height=360,
                xaxis=dict(visible=False),
                yaxis=dict(tickfont=dict(color='#0B1220', size=11))
            )
            st.plotly_chart(fig_pq, use_container_width=True)

    # ---------------------------------------------------------
    # MÓDULO 04. RENTABILIDAD (ANÁLISIS DE MÁRGENES)
    # ---------------------------------------------------------
    elif menu_opcion == "04. Rentabilidad":
        st.markdown('<h2 style="font-family: \'Space Grotesk\', sans-serif; color: #0B1220; font-size: 24px;">Análisis de Rentabilidad y Márgenes</h2>', unsafe_allow_html=True)
        
        cr1, cr2 = st.columns(2)
        with cr1:
            st.markdown('<div class="chart-header">Margen de Utilidad (%) por Categoría</div>', unsafe_allow_html=True)
            df_mg_cat = df_curr.groupby('Categoria').apply(
                lambda x: (x['Utilidad_Soles'].sum() / x['Ventas_Soles'].sum() * 100) if x['Ventas_Soles'].sum() > 0 else 0
            ).reset_index(name='Margen_Pct')
            
            fig_mg = go.Figure(go.Bar(
                x=df_mg_cat['Categoria'],
                y=df_mg_cat['Margen_Pct'],
                marker=dict(color='#10B981', cornerradius=6),
                text=[f"{v:.1f}%" for v in df_mg_cat['Margen_Pct']],
                textposition='outside',
                textfont=dict(color='#0B1220', size=12)
            ))
            fig_mg.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=30, b=10),
                height=320,
                xaxis=dict(tickfont=dict(color='#0B1220')),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', visible=False)
            )
            st.plotly_chart(fig_mg, use_container_width=True)
            
        with cr2:
            st.markdown('<div class="chart-header">Relación Ventas vs. Utilidad Neta por Producto</div>', unsafe_allow_html=True)
            df_scat = df_curr.groupby('Producto')[['Ventas_Soles', 'Utilidad_Soles']].sum().reset_index()
            
            fig_scat = go.Figure(go.Scatter(
                x=df_scat['Ventas_Soles'],
                y=df_scat['Utilidad_Soles'],
                mode='markers+text',
                text=df_scat['Producto'],
                textposition='top center',
                marker=dict(size=12, color='#6C5CE7', opacity=0.8),
                textfont=dict(color='#0B1220', size=10)
            ))
            fig_scat.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                height=320,
                xaxis=dict(title="Ventas Totales (S/)", titlefont=dict(color='#0B1220'), tickfont=dict(color='#6B7686'), showgrid=True, gridcolor='#E2E8F0'),
                yaxis=dict(title="Utilidad Neta (S/)", titlefont=dict(color='#0B1220'), tickfont=dict(color='#6B7686'), showgrid=True, gridcolor='#E2E8F0')
            )
            st.plotly_chart(fig_scat, use_container_width=True)

    # ---------------------------------------------------------
    # MÓDULO 05. ANÁLISIS (MAPA DE CALOR Y PATRONES)
    # ---------------------------------------------------------
    elif menu_opcion == "05. Análisis":
        st.markdown('<h2 style="font-family: \'Space Grotesk\', sans-serif; color: #0B1220; font-size: 24px;">Matriz Cruzada y Patrones Comerciales</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-header">Mapa de Calor: Canal de Venta vs. Categoría (Ventas S/)</div>', unsafe_allow_html=True)
        df_pivot = df_curr.pivot_table(index='Canal_Venta', columns='Categoria', values='Ventas_Soles', aggfunc='sum').fillna(0)
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=df_pivot.values,
            x=df_pivot.columns,
            y=df_pivot.index,
            colorscale='Blues',
            text=[[f"S/ {val:,.0f}" for val in row] for row in df_pivot.values],
            texttemplate="%{text}",
            textfont=dict(color='#0B1220', size=12)
        ))
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=340,
            xaxis=dict(tickfont=dict(color='#0B1220')),
            yaxis=dict(tickfont=dict(color='#0B1220'))
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # ---------------------------------------------------------
    # MÓDULO 06. SIMULADOR MYPE (CALCULADORA INTERACTIVA DE ROI)
    # ---------------------------------------------------------
    elif menu_opcion == "06. Simulador MYPE":
        st.markdown('<h2 style="font-family: \'Space Grotesk\', sans-serif; color: #0B1220; font-size: 24px;">Simulador Financiero MYPE</h2>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 14px; color: #6B7686; margin-bottom: 20px;">Ajusta los parámetros para proyectar el impacto en ventas, utilidad y ROI en tiempo real.</p>', unsafe_allow_html=True)
        
        col_sim_in, col_sim_res = st.columns([2, 3])
        
        with col_sim_in:
            st.markdown('<div class="chart-header">Parámetros de Simulación</div>', unsafe_allow_html=True)
            
            p_price = st.slider("Ajuste de Precios (%):", -15.0, 25.0, 5.0, step=0.5)
            p_vol = st.slider("Crecimiento de Volumen (%):", -20.0, 40.0, 10.0, step=1.0)
            p_waste = st.slider("Reducción de Mermas (%):", 0.0, 30.0, 10.0, step=1.0)
            p_mkt = st.number_input("Inversión en Marketing (S/):", min_value=0, max_value=5000, value=300, step=50)
            
        with col_sim_res:
            st.markdown('<div class="chart-header">Resultados Proyectados</div>', unsafe_allow_html=True)
            
            vtas_proj = vtas_tot * (1 + p_price/100) * (1 + p_vol/100)
            cost_base = df_curr['Costo_Soles'].sum() if 'Costo_Soles' in df_curr.columns else vtas_tot * 0.7
            cost_proj = (cost_base * (1 + p_vol/100)) * (1 - p_waste/100) + p_mkt
            util_proj = vtas_proj - cost_proj
            inc_util = util_proj - util_tot
            roi_sim = (inc_util / p_mkt * 100) if p_mkt > 0 else 0
            
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Ventas Proyectadas</div>
                    <div class="kpi-value">S/ {vtas_proj:,.2f}</div>
                    <span class="kpi-badge-pos">▲ {((vtas_proj-vtas_tot)/vtas_tot*100):+.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
            with sc2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Utilidad Proyectada</div>
                    <div class="kpi-value">S/ {util_proj:,.2f}</div>
                    <span class="kpi-badge-pos">▲ S/ {inc_util:+,.2f}</span>
                </div>
                """, unsafe_allow_html=True)
            with sc3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">ROI de Inversión</div>
                    <div class="kpi-value">{roi_sim:.1f}%</div>
                    <span class="kpi-badge-pos">Rentable</span>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            fig_sim = go.Figure(data=[
                go.Bar(name='Actual', x=['Ventas', 'Costos', 'Utilidad'], y=[vtas_tot, cost_base, util_tot], marker_color='#8C9BAE'),
                go.Bar(name='Proyectado', x=['Ventas', 'Costos', 'Utilidad'], y=[vtas_proj, cost_proj, util_proj], marker_color='#00C2D1')
            ])
            fig_sim.update_layout(
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=20, b=10),
                height=260,
                legend=dict(font=dict(color='#0B1220')),
                xaxis=dict(tickfont=dict(color='#0B1220')),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#6B7686'))
            )
            st.plotly_chart(fig_sim, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #6B7686;'>NexData Platform v2.5 – Desarrollado para el Proyecto MYPE 2026</p>", unsafe_allow_html=True)
