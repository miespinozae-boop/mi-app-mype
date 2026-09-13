import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import shutil

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NEXDATA - Panel de Inteligencia Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (RÉPLICA EXACTA DE INTERFAZ NEXDATA)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }
    
    header[data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.8);
    }
    footer {visibility: hidden;}
    
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
        width: 260px !important;
    }
    
    .sidebar-logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0px 25px 0px;
    }
    .logo-icon {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-weight: 800;
        font-size: 18px;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    .logo-text {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    
    .sidebar-bottom-card {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-radius: 14px;
        padding: 16px;
        margin-top: 40px;
    }
    .sidebar-bottom-title {
        font-size: 13px;
        font-weight: 700;
        color: #0369A1;
        margin-bottom: 4px;
    }
    .sidebar-bottom-brand {
        font-size: 12px;
        font-weight: 800;
        color: #0284C7;
        margin-top: 8px;
    }
    
    .greeting-title {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
    }
    .greeting-title span {
        color: #2563EB;
    }
    .greeting-subtitle {
        font-size: 14px;
        color: #64748B;
        margin-top: 4px;
    }
    
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .kpi-icon-bg {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    .icon-blue { background-color: #EFF6FF; color: #2563EB; }
    .icon-purple { background-color: #F3E8FF; color: #9333EA; }
    .icon-green { background-color: #DCFCE7; color: #16A34A; }
    .icon-orange { background-color: #FFEDD5; color: #EA580C; }
    
    .kpi-label { font-size: 13px; font-weight: 600; color: #64748B; }
    .kpi-value { font-size: 26px; font-weight: 800; color: #0F172A; margin: 4px 0 8px 0; letter-spacing: -0.5px; }
    .kpi-trend { font-size: 12px; font-weight: 700; color: #16A34A; }
    
    .content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .card-title { font-size: 16px; font-weight: 700; color: #0F172A; }
    .card-subtitle { font-size: 12px; color: #64748B; margin-bottom: 16px; }
    
    .product-row { margin-bottom: 14px; }
    .product-info { display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; color: #334155; margin-bottom: 6px; }
    .progress-bg { background-color: #F1F5F9; border-radius: 8px; height: 8px; width: 100%; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 8px; }
    
    .alert-box { border-radius: 12px; padding: 14px; margin-bottom: 12px; display: flex; align-items: flex-start; gap: 12px; }
    .alert-warning { background-color: #FFFBEB; border: 1px solid #FDE68A; }
    .alert-success { background-color: #F0FDF4; border: 1px solid #BBF7D0; }
    .alert-title { font-size: 13px; font-weight: 700; margin-bottom: 2px; }
    .warning-text { color: #92400E; }
    .success-text { color: #166534; }
    .alert-desc { font-size: 12px; color: #475569; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MENÚ LATERAL
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo-container">
            <div class="logo-icon">N</div>
            <div class="logo-text">NEXDATA</div>
        </div>
    """, unsafe_allow_html=True)
    
    menu_selection = st.radio(
        "Navegación",
        ["Inicio", "Ventas", "Productos", "Rentabilidad", "Análisis", "Simulador"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("""
        <div class="sidebar-bottom-card">
            <div class="sidebar-bottom-title">💡 Tu negocio, en mejores decisiones</div>
            <div style="font-size: 11px; color: #0369A1; margin-top: 4px;">Analítica avanzada simplificada para tu MYPE.</div>
            <div class="sidebar-bottom-brand">NEXDATA</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CABECERA PRINCIPAL
# -----------------------------------------------------------------------------
col_header_left, col_header_right = st.columns([2, 1])

with col_header_left:
    st.markdown("""
        <div>
            <h1 class="greeting-title">¡Hola, <span>Milagros</span>!</h1>
            <p class="greeting-subtitle">Aquí tienes un resumen del rendimiento de tu negocio.</p>
        </div>
    """, unsafe_allow_html=True)

with col_header_right:
    col_user, col_period = st.columns([1, 1.2])
    with col_user:
        user_select = st.selectbox("Usuario", ["Mi Negocio"], index=0, label_visibility="collapsed")
    with col_period:
        periodo_select = st.selectbox("Periodo", ["Últimos 30 días", "Este Mes", "Último Trimestre"], index=0, label_visibility="collapsed")

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TARJETAS DE INDICADORES (KPIs)
# -----------------------------------------------------------------------------
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-bg icon-blue">🛒</div>
                <div class="kpi-label">Ventas Totales</div>
            </div>
            <div class="kpi-value">S/ 48,950</div>
            <div class="kpi-trend">↑ +12.5% <span style="color:#64748B; font-weight:500;">vs. mes anterior</span></div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-bg icon-purple">📦</div>
                <div class="kpi-label">Productos Vendidos</div>
            </div>
            <div class="kpi-value">1,240</div>
            <div class="kpi-trend">↑ +8.3% <span style="color:#64748B; font-weight:500;">vs. mes anterior</span></div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-bg icon-green">👤</div>
                <div class="kpi-label">Clientes Atendidos</div>
            </div>
            <div class="kpi-value">892</div>
            <div class="kpi-trend">↑ +15.7% <span style="color:#64748B; font-weight:500;">vs. mes anterior</span></div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon-bg icon-orange">💲</div>
                <div class="kpi-label">Rentabilidad</div>
            </div>
            <div class="kpi-value">18.4%</div>
            <div class="kpi-trend">↑ +4.2% <span style="color:#64748B; font-weight:500;">vs. mes anterior</span></div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# GRÁFICOS CENTRALES
# -----------------------------------------------------------------------------
chart_col_left, chart_col_right = st.columns([1.8, 1.2])

with chart_col_left:
    st.markdown("""
        <div class="content-card">
            <div class="card-title">📈 Evolución de Ventas</div>
            <div class="card-subtitle">Ventas diarias en los últimos 30 días</div>
        </div>
    """, unsafe_allow_html=True)
    
    days_ticks = [f"{i} Abr" for i in [1, 5, 10, 15, 20, 25, 30]]
    all_days = [f"{i} Abr" for i in range(1, 31)]
    sales_curve = [
        800, 1000, 950, 1200, 1400, 1600, 1300, 1500, 1800, 2000,
        1700, 1600, 1800, 1900, 1700, 1700, 2100, 2450, 2400, 2800,
        3000, 3200, 2900, 2500, 2500, 2550, 2400, 2500, 2800, 3250
    ]
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=all_days,
        y=sales_curve,
        mode='lines+markers',
        line=dict(color='#2563EB', width=3, shape='spline'),
        marker=dict(size=6, color='#2563EB', line=dict(color='#FFFFFF', width=2)),
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.06)',
        name='Ventas (S/)'
    ))
    
    fig_line.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='#F1F5F9',
            tickvals=[f"{i} Abr" for i in [1, 5, 10, 15, 20, 25, 30]],
            ticktext=days_ticks,
            tickfont=dict(size=11, color='#64748B')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F1F5F9',
            range=[0, 4000],
            tickvals=[0, 1000, 2000, 3000, 4000],
            tickfont=dict(size=11, color='#64748B')
        ),
        showlegend=False
    )
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col_right:
    st.markdown("""
        <div class="content-card">
            <div class="card-title">📊 Ventas por Categoría</div>
            <div class="card-subtitle">Distribución de ventas por categoría</div>
        </div>
    """, unsafe_allow_html=True)
    
    cat_labels = ['Alimentos', 'Bebidas', 'Limpieza', 'Higiene', 'Otros']
    cat_values = [32.5, 24.8, 18.2, 12.6, 11.9]
    cat_colors = ['#2563EB', '#8B5CF6', '#10B981', '#F97316', '#06B6D4']
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=cat_labels,
        values=cat_values,
        hole=0.68,
        marker=dict(colors=cat_colors),
        textinfo='none',
        hoverinfo='label+percent'
    )])
    
    fig_donut.add_annotation(
        text="<b style='font-size:18px;color:#0F172A;'>S/ 48,950</b><br><span style='font-size:12px;color:#64748B;'>Total ventas</span>",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(family='Plus Jakarta Sans')
    )
    
    fig_donut.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=0.75,
            font=dict(size=12, color='#334155')
        )
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FILA INFERIOR (3 COLUMNAS)
# -----------------------------------------------------------------------------
bot_col1, bot_col2, bot_col3 = st.columns(3)

with bot_col1:
    st.markdown("""
        <div class="content-card">
            <div class="card-title">📦 Productos Más Vendidos</div>
            <div class="card-subtitle">Top 5 por volumen de ventas</div>
            
            <div class="product-row"><div class="product-info"><span>1. Arroz</span><span>320 un.</span></div><div class="progress-bg"><div class="progress-fill" style="width: 100%; background-color: #2563EB;"></div></div></div>
            <div class="product-row"><div class="product-info"><span>2. Aceite</span><span>280 un.</span></div><div class="progress-bg"><div class="progress-fill" style="width: 87.5%; background-color: #10B981;"></div></div></div>
            <div class="product-row"><div class="product-info"><span>3. Leche</span><span>220 un.</span></div><div class="progress-bg"><div class="progress-fill" style="width: 68.7%; background-color: #8B5CF6;"></div></div></div>
            <div class="product-row"><div class="product-info"><span>4. Galletas</span><span>180 un.</span></div><div class="progress-bg"><div class="progress-fill" style="width: 56.2%; background-color: #F97316;"></div></div></div>
            <div class="product-row"><div class="product-info"><span>5. Detergente</span><span>160 un.</span></div><div class="progress-bg"><div class="progress-fill" style="width: 50%; background-color: #06B6D4;"></div></div></div>
        </div>
    """, unsafe_allow_html=True)

with bot_col2:
    st.markdown("""
        <div class="content-card">
            <div class="card-title">📢 Canales de Venta</div>
            <div class="card-subtitle">Participación por canal</div>
        </div>
    """, unsafe_allow_html=True)
    
    channel_labels = ['Tienda física', 'Delivery', 'Online', 'Otros']
    channel_values = [45, 30, 15, 10]
    channel_colors = ['#2563EB', '#10B981', '#8B5CF6', '#F97316']
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=channel_labels,
        values=channel_values,
        hole=0,
        marker=dict(colors=channel_colors),
        textinfo='percent',
        textfont=dict(size=12, color='#FFFFFF', family='Plus Jakarta Sans')
    )])
    
    fig_pie.update_layout(
        height=220,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=0.82,
            font=dict(size=11, color='#334155')
        )
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with bot_col3:
    st.markdown("""
        <div class="content-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <div class="card-title">🔔 Alertas y Recomendaciones</div>
                <a href="#" style="font-size: 12px; font-weight: 700; color: #2563EB; text-decoration: none;">Ver todas →</a>
            </div>
            <div class="card-subtitle">Acciones sugeridas por el motor analítico</div>
            
            <div class="alert-box alert-warning">
                <div style="font-size: 18px;">⚠️</div>
                <div>
                    <div class="alert-title warning-text">Producto con baja rotación</div>
                    <div class="alert-desc">El producto <b>"Galletas"</b> ha disminuido su venta en un 35% en comparación con el mes anterior.</div>
                </div>
            </div>
            
            <div class="alert-box alert-success">
                <div style="font-size: 18px;">✅</div>
                <div>
                    <div class="alert-title success-text">Oportunidad de crecimiento</div>
                    <div class="alert-desc">La categoría de <b>Bebidas</b> muestra una tendencia al alza. Considera aumentar el stock.</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
