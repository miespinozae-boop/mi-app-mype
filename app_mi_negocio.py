import io
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="NEXDATA – Panel de Inteligencia Empresarial", page_icon="📊", layout="wide")

st.markdown("""
<style>
html,body,[data-testid="stAppViewContainer"]{background:#fff!important;color:#172B4D!important}
[data-testid="stHeader"]{background:#fff!important}
[data-testid="stSidebar"]{background:#F8FBFF!important;border-right:1px solid #DCE5F0}
[data-testid="stSidebar"] *{color:#334A68!important}
h1,h2,h3,h4,h5,h6,[data-testid="stMarkdownContainer"] p,label{color:#172B4D!important}
.block-container{padding-top:2.2rem!important;max-width:1500px!important;padding-bottom:2rem}
.nex-logo{font-size:30px;font-weight:800;color:#172B4D!important;margin-bottom:18px}
.nex-logo span,.welcome-title span{color:#2E8CF7!important}
.welcome-title{font-size:30px;line-height:1.25;font-weight:800;color:#172B4D!important;margin-top:8px;margin-bottom:4px}
.welcome-subtitle{color:#60738F!important;font-size:15px;margin-bottom:16px}
.metric-card{background:#fff;border:1px solid #DCE5F0;border-radius:14px;padding:18px 20px;min-height:135px;box-shadow:0 3px 12px rgba(31,55,86,.04)}
.metric-label{color:#536A87!important;font-size:14px}.metric-value{color:#14213D!important;font-size:30px;font-weight:800}
.metric-delta{color:#17A673!important;font-size:13px;margin-top:9px}
.section-title{color:#172B4D!important;font-size:17px;font-weight:750;margin-bottom:2px}
.section-subtitle{color:#71839B!important;font-size:12px;margin-bottom:8px}
.alert-card{border-radius:12px;padding:13px 15px;margin:7px 0;border:1px solid #E6ECF4;background:#fff}
.alert-warning{background:#FFF9F1;border-color:#F9D9B0}.alert-success{background:#F2FBF7;border-color:#C9EBDD}
.alert-title{color:#172B4D!important;font-weight:750;font-size:13px}.alert-text{color:#60738F!important;font-size:12px}
.sidebar-note{border:1px solid #DCE5F0;border-radius:12px;padding:14px;margin-top:18px;background:#fff;color:#60738F!important;font-size:12px}
div[data-testid="stTabs"] button{color:#526987!important;font-weight:650!important}
div[data-testid="stTabs"] button[aria-selected="true"]{color:#2563EB!important}
#MainMenu,footer{visibility:hidden}
</style>

<style>
/* Controles nativos de Streamlit: fondo blanco y texto oscuro */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div,
[data-testid="stSidebar"] [data-baseweb="popover"] {
    background-color:#FFFFFF!important;
    color:#172B4D!important;
    border-color:#D6E0EC!important;
}
[data-testid="stSidebar"] button {
    color:#172B4D!important;
}
[data-testid="stFileUploader"] section {
    background:#FFFFFF!important;
    border:1px solid #D6E0EC!important;
}
[data-testid="stFileUploader"] section * {
    color:#526987!important;
}
[data-testid="stFileUploader"] button {
    background:#F3F7FC!important;
    color:#2563EB!important;
    border:1px solid #C9D8EA!important;
}
[data-testid="stDataEditor"] {
    border:1px solid #D6E0EC!important;
}
</style>

""", unsafe_allow_html=True)

DEMO = pd.DataFrame({
"Fecha":pd.date_range("2026-04-01",periods=30,freq="D"),
"Categoria":(["Alimentos","Alimentos","Bebidas","Limpieza","Higiene","Alimentos","Bebidas","Otros","Limpieza","Alimentos"]*3),
"Producto":(["Arroz","Aceite","Leche","Detergente","Galletas","Arroz","Aceite","Leche","Detergente","Galletas"]*3),
"Canal_Venta":(["Tienda física","Delivery","Online","Tienda física","Delivery","Online","Tienda física","Delivery","Online","Otros"]*3),
"Ventas_Soles":([1250,1080,920,740,620,1320,1140,980,790,650]*3),
"Utilidad_Soles":([240,205,185,130,105,255,218,195,140,112]*3),
"Cantidad":([80,70,65,52,48,84,73,67,55,50]*3)
})

ALIASES={
"Fecha":["fecha","date","dia","día","fecha_venta"],
"Categoria":["categoria","categoría","category","tipo","familia","rubro"],
"Producto":["producto","product","item","articulo","artículo","sku","nombre_producto"],
"Canal_Venta":["canal_venta","canal","channel","medio_venta","medio"],
"Ventas_Soles":["ventas_soles","ventas","venta","ingresos","ingreso","sales","revenue","total_ventas","importe","monto"],
"Utilidad_Soles":["utilidad_soles","utilidad","ganancia","beneficio","profit","gross_profit","net_profit"],
"Cantidad":["cantidad","unidades","qty","quantity","units","productos_vendidos"],
"Precio":["precio","price","precio_unitario","unit_price"],
"Costo":["costo","cost","costo_unitario","unit_cost"]
}
REQ=["Fecha","Categoria","Producto","Canal_Venta","Ventas_Soles","Utilidad_Soles"]

def norm(x):
    return str(x).strip().lower().replace(" ","_").replace("-","_").replace("/","_")

def standardize(raw):
    d=raw.copy(); d.columns=[str(c).strip() for c in d.columns]
    normalized={norm(c):c for c in d.columns}
    rename={}
    for target,aliases in ALIASES.items():
        for a in aliases:
            if norm(a) in normalized:
                rename[normalized[norm(a)]]=target; break
    d=d.rename(columns=rename)
    if "Fecha" not in d.columns:
        for c in d.columns:
            p=pd.to_datetime(d[c],errors="coerce")
            if p.notna().mean()>=.7: d=d.rename(columns={c:"Fecha"}); break
    if "Categoria" not in d.columns and "Producto" in d.columns: d["Categoria"]="General"
    if "Canal_Venta" not in d.columns: d["Canal_Venta"]="No especificado"

    # Si el archivo trae cantidad y precio, calcular ventas automáticamente.
    if "Ventas_Soles" not in d.columns and "Cantidad" in d.columns and "Precio" in d.columns:
        d["Ventas_Soles"] = pd.to_numeric(d["Cantidad"], errors="coerce") * pd.to_numeric(d["Precio"], errors="coerce")

    # Si trae ventas, cantidad y costo, calcular utilidad automáticamente.
    if "Utilidad_Soles" not in d.columns and all(c in d.columns for c in ["Ventas_Soles","Cantidad","Costo"]):
        ventas_num = pd.to_numeric(d["Ventas_Soles"], errors="coerce")
        cantidad_num = pd.to_numeric(d["Cantidad"], errors="coerce")
        costo_num = pd.to_numeric(d["Costo"], errors="coerce")
        d["Utilidad_Soles"] = ventas_num - (cantidad_num * costo_num)

    missing=[c for c in REQ if c not in d.columns]
    return d,missing

def prep(d):
    d=d.copy()
    for c in ["Ventas_Soles","Utilidad_Soles","Cantidad","Precio","Costo"]:
        if c in d.columns:
            d[c]=pd.to_numeric(d[c].astype(str).str.replace("S/","",regex=False).str.replace("$","",regex=False).str.replace(",","",regex=False).str.strip(),errors="coerce")
    d["Ventas_Soles"]=d["Ventas_Soles"].fillna(0); d["Utilidad_Soles"]=d["Utilidad_Soles"].fillna(0)
    d["Fecha"]=pd.to_datetime(d["Fecha"],errors="coerce")
    for c in ["Categoria","Producto","Canal_Venta"]: d[c]=d[c].fillna("Sin dato").astype(str)
    return d

def read_file(f):
    ext=Path(f.name).suffix.lower()
    if ext==".csv":
        try:return pd.read_csv(f)
        except UnicodeDecodeError:
            f.seek(0); return pd.read_csv(f,encoding="latin-1")
    if ext in [".xlsx",".xls"]:
        book=pd.ExcelFile(f)
        for sheet in book.sheet_names:
            x=pd.read_excel(book,sheet_name=sheet)
            if not x.empty:return x
        return pd.read_excel(book,sheet_name=0)
    raise ValueError("Formato no compatible")

def money(x): return f"S/ {x:,.0f}"
def margin(s,p): return p/s*100 if s else 0

def apply_chart_theme(fig, height=320, showlegend=True):
    """Tema Plotly seguro para fondo blanco; evita parámetros incompatibles."""
    fig.update_layout(
        height=height,
        margin=dict(l=55, r=25, t=25, b=50),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color="#172B4D", size=12),
        showlegend=showlegend,
    )
    fig.update_xaxes(
        color="#172B4D",
        title_font=dict(color="#172B4D", size=12),
        tickfont=dict(color="#526987", size=11),
        gridcolor="#E7EDF5",
        linecolor="#D6E0EC",
        zerolinecolor="#D6E0EC",
    )
    fig.update_yaxes(
        color="#172B4D",
        title_font=dict(color="#172B4D", size=12),
        tickfont=dict(color="#526987", size=11),
        gridcolor="#E7EDF5",
        linecolor="#D6E0EC",
        zerolinecolor="#D6E0EC",
    )
    if showlegend:
        fig.update_layout(
            legend=dict(
                font=dict(color="#172B4D", size=12),
                title_font=dict(color="#172B4D", size=12),
            )
        )
    return fig

def render_chart(fig, height=320, showlegend=True):
    """Renderizador único y compatible con versiones actuales de Plotly."""
    fig = apply_chart_theme(fig, height=height, showlegend=showlegend)
    st.plotly_chart(fig, use_container_width=True, config={
        "displayModeBar": False,
        "responsive": True,
    })

def card(label,value,delta,icon,border):
    st.markdown(f"""<div class="metric-card" style="border-color:{border}55">
    <div style="display:flex;align-items:center;gap:10px"><span style="font-size:22px">{icon}</span><span class="metric-label">{label}</span></div>
    <div class="metric-value">{value}</div><div class="metric-delta">↑ {delta}</div></div>""",unsafe_allow_html=True)

if "df" not in st.session_state: st.session_state.df=DEMO.copy()
if "source" not in st.session_state: st.session_state.source="Datos demo"
if "last_upload" not in st.session_state: st.session_state.last_upload=""

with st.sidebar:
    st.markdown('<div class="nex-logo">▮▮▮ NEX<span>DATA</span></div>',unsafe_allow_html=True)
    st.markdown("### Navegación")
    page=st.radio("Navegación",["Inicio","Ventas","Productos","Rentabilidad","Análisis","Simulador","Datos"],label_visibility="collapsed",key="navigation")
    st.markdown("---")
    st.markdown("### Cargar datos")
    up=st.file_uploader("Selecciona un archivo Excel o CSV",type=["xlsx","xls","csv"],key="upload")
    if up is not None and st.session_state.last_upload!=up.name:
        try:
            raw=read_file(up); d,missing=standardize(raw)
            if missing: st.error("Faltan columnas esenciales: "+", ".join(missing))
            else:
                st.session_state.df=prep(d); st.session_state.source=up.name; st.session_state.last_upload=up.name
                st.success("Datos cargados correctamente.")
        except Exception as e: st.error(f"Error al cargar datos: {e}")
    st.markdown('<div class="sidebar-note"><b>Tu negocio, en mejores decisiones</b><br><br><b style="color:#2563EB!important">NEX</b>DATA<br>Edita tus datos y observa cómo cambia el análisis.</div>',unsafe_allow_html=True)

df=prep(st.session_state.df.copy())

# Página de edición: cada cambio se guarda en session_state y provoca rerun.
if page=="Datos":
    st.markdown('<div class="welcome-title">Datos del <span>negocio</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Modifica cualquier celda editable y el resto del análisis se recalculará automáticamente.</div>',unsafe_allow_html=True)
    editable=["Fecha","Categoria","Producto","Canal_Venta","Ventas_Soles","Utilidad_Soles","Cantidad","Precio","Costo"]
    disabled=[c for c in df.columns if c not in editable]
    edited=st.data_editor(df,use_container_width=True,hide_index=True,num_rows="dynamic",disabled=disabled,
        column_config={
            "Fecha":st.column_config.DateColumn("Fecha",format="DD/MM/YYYY"),
            "Ventas_Soles":st.column_config.NumberColumn("Ventas (S/)",min_value=0,step=1),
            "Utilidad_Soles":st.column_config.NumberColumn("Utilidad (S/)",step=1),
            "Cantidad":st.column_config.NumberColumn("Cantidad",min_value=0,step=1),
            "Precio":st.column_config.NumberColumn("Precio",min_value=0,step=.01),
            "Costo":st.column_config.NumberColumn("Costo",min_value=0,step=.01)
        },key="editor")
    st.session_state.df=prep(edited)
    x1,x2,x3=st.columns(3)
    x1.metric("Filas",f"{len(edited):,}"); x2.metric("Ventas",money(edited.Ventas_Soles.sum())); x3.metric("Utilidad",money(edited.Utilidad_Soles.sum()))
    st.download_button("Descargar datos actualizados",edited.to_csv(index=False).encode("utf-8-sig"),"nexdata_datos_actualizados.csv","text/csv")
    st.info("Los cambios quedan en la sesión y alimentan los KPIs, gráficos y simulaciones.")
    st.stop()

with st.sidebar:
    st.markdown("### Filtros")
    valid_dates=df.Fecha.dropna()
    lo=(valid_dates.min() if not valid_dates.empty else pd.Timestamp("2026-01-01")).date()
    hi=(valid_dates.max() if not valid_dates.empty else pd.Timestamp.today()).date()
    dr=st.date_input("Periodo",value=(lo,hi),min_value=lo,max_value=hi,key="period")
    cats=sorted(df.Categoria.unique()); chans=sorted(df.Canal_Venta.unique())
    sc=st.multiselect("Categoría",cats,default=cats,key="cats")
    sh=st.multiselect("Canal de venta",chans,default=chans,key="channels")

if isinstance(dr,tuple) and len(dr)==2: start,end=pd.Timestamp(dr[0]),pd.Timestamp(dr[1])
else:start=end=pd.Timestamp(dr)
f=df[df.Fecha.between(start,end)&df.Categoria.isin(sc)&df.Canal_Venta.isin(sh)].copy()
sales=float(f.Ventas_Soles.sum()); profit=float(f.Utilidad_Soles.sum()); mar=margin(sales,profit)
units=float(f.Cantidad.sum()) if "Cantidad" in f.columns else float(len(f))
customers=int(f.Cliente.nunique()) if "Cliente" in f.columns else int(len(f))
ticket=sales/customers if customers else 0

st.markdown('<div class="welcome-title">¡Hola, <span>Milagros!</span></div>',unsafe_allow_html=True)
st.markdown('<div class="welcome-subtitle">Aquí tienes un resumen del rendimiento de tu negocio.</div>',unsafe_allow_html=True)
st.caption(f"Fuente: {st.session_state.source} · {len(f):,} registros")

if page=="Inicio":
    a,b,c,d=st.columns(4)
    with a:card("Ventas Totales",money(sales),"datos actuales","🛒","#4B9AF5")
    with b:card("Productos Vendidos",f"{units:,.0f}","datos actuales","▣","#8B6FE8")
    with c:card("Clientes Atendidos",f"{customers:,.0f}","datos actuales","♙","#20B486")
    with d:card("Rentabilidad",f"{mar:.1f}%","tiempo real","$","#F6A23A")
    st.write("")
    l,r=st.columns([1.45,1])
    with l:
        st.markdown('<div class="section-title">Evolución de Ventas</div><div class="section-subtitle">Ventas diarias del periodo seleccionado</div>',unsafe_allow_html=True)
        daily=f.groupby("Fecha",as_index=False).Ventas_Soles.sum()
        if not daily.empty:
            fig=px.line(daily,x="Fecha",y="Ventas_Soles",markers=True)
            fig.update_traces(line_color="#4B9AF5",line_width=3,marker_size=6)
            render_chart(fig, height=300, showlegend=False)
        else:st.info("No hay datos para el periodo.")
    with r:
        st.markdown('<div class="section-title">Ventas por Categoría</div><div class="section-subtitle">Distribución por categoría</div>',unsafe_allow_html=True)
        cat=f.groupby("Categoria",as_index=False).Ventas_Soles.sum()
        if not cat.empty and cat.Ventas_Soles.sum()>0:
            fig=px.pie(cat,names="Categoria",values="Ventas_Soles",hole=.58)
            render_chart(fig, height=300, showlegend=True)
        else:st.info("No hay ventas por categoría.")
    st.write("")
    p1,p2,p3=st.columns([1,1,1.15])
    with p1:
        st.markdown('<div class="section-title">Productos Más Vendidos</div><div class="section-subtitle">Top 5 por volumen</div>',unsafe_allow_html=True)
        qtycol="Cantidad" if "Cantidad" in f.columns else "Ventas_Soles"
        prod=f.groupby("Producto",as_index=False)[qtycol].sum().sort_values(qtycol).tail(5)
        if not prod.empty:
            fig=px.bar(prod,x=qtycol,y="Producto",orientation="h",text_auto=".0f")
            fig.update_traces(marker_color=["#27B8C7","#F6A23A","#8B6FE8","#20B486","#4B9AF5"][-len(prod):])
            render_chart(fig, height=270, showlegend=False)
    with p2:
        st.markdown('<div class="section-title">Canales de Venta</div><div class="section-subtitle">Participación por canal</div>',unsafe_allow_html=True)
        ch=f.groupby("Canal_Venta",as_index=False).Ventas_Soles.sum()
        if not ch.empty:
            fig=px.pie(ch,names="Canal_Venta",values="Ventas_Soles")
            fig.update_layout(height=270,margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor="white",font=dict(color="#172B4D"))
            st.plotly_chart(fig,use_container_width=True)
    with p3:
        st.markdown('<div class="section-title">Alertas y Recomendaciones</div>',unsafe_allow_html=True)
        if not f.empty:
            ps=f.groupby("Producto").Ventas_Soles.sum().sort_values()
            cs=f.groupby("Categoria").Ventas_Soles.sum().sort_values(ascending=False)
            if len(ps):
                st.markdown(f'<div class="alert-card alert-warning"><div class="alert-title">Producto de menor rotación</div><div class="alert-text">{ps.index[0]} registra las ventas más bajas del periodo. Revisa precio, promoción y disponibilidad.</div></div>',unsafe_allow_html=True)
            if len(cs):
                st.markdown(f'<div class="alert-card alert-success"><div class="alert-title">Oportunidad de crecimiento</div><div class="alert-text">La categoría {cs.index[0]} lidera las ventas. Evalúa aumentar stock o promoción.</div></div>',unsafe_allow_html=True)

elif page=="Ventas":
    st.header("Ventas"); st.caption("Analiza la evolución y composición de tus ventas.")
    m1,m2,m3=st.columns(3); m1.metric("Ventas",money(sales)); m2.metric("Unidades",f"{units:,.0f}"); m3.metric("Ticket promedio",money(ticket))
    daily=f.groupby("Fecha",as_index=False).Ventas_Soles.sum()
    fig=px.line(daily,x="Fecha",y="Ventas_Soles",markers=True); fig.update_traces(line_color="#4B9AF5",line_width=3); apply_chart_theme(fig, height=420, showlegend=False)
    st.plotly_chart(fig,use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.dataframe(f.groupby("Canal_Venta",as_index=False).Ventas_Soles.sum().sort_values("Ventas_Soles",ascending=False),use_container_width=True,hide_index=True)

elif page=="Productos":
    st.header("Productos"); st.caption("Identifica productos líderes y productos que requieren atención.")
    prod=f.groupby("Producto",as_index=False).agg(Ventas=("Ventas_Soles","sum"),Utilidad=("Utilidad_Soles","sum"),Cantidad=("Cantidad","sum") if "Cantidad" in f.columns else ("Ventas_Soles","size"))
    prod["Margen_%"]=np.where(prod.Ventas!=0,prod.Utilidad/prod.Ventas*100,0)
    x,y=st.columns(2)
    with x:
        st.subheader("Top productos por ventas"); z=prod.nlargest(10,"Ventas").sort_values("Ventas")
        fig=px.bar(z,x="Ventas",y="Producto",orientation="h",text_auto=".0f"); fig.update_traces(marker_color=["#4B9AF5","#20B486","#8B6FE8","#F6A23A","#27B8C7"]*3); apply_chart_theme(fig, height=430, showlegend=False); st.plotly_chart(fig,use_container_width=True)
    with y:
        st.subheader("Top productos por rentabilidad"); z=prod.nlargest(10,"Margen_%").sort_values("Margen_%")
        fig=px.bar(z,x="Margen_%",y="Producto",orientation="h",text_auto=".1f"); fig.update_traces(marker_color=["#8B6FE8","#20B486","#4B9AF5","#F6A23A","#27B8C7"]*3); apply_chart_theme(fig, height=430, showlegend=False); st.plotly_chart(fig,use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.dataframe(prod,use_container_width=True,hide_index=True)

elif page=="Rentabilidad":
    st.header("Rentabilidad"); st.caption("Evalúa utilidad y margen.")
    cat=f.groupby("Categoria",as_index=False).agg(Ventas=("Ventas_Soles","sum"),Utilidad=("Utilidad_Soles","sum")); cat["Margen_%"]=np.where(cat.Ventas!=0,cat.Utilidad/cat.Ventas*100,0)
    x,y=st.columns(2)
    with x:
        st.subheader("Utilidad por categoría"); fig=px.bar(cat.sort_values("Utilidad"),x="Utilidad",y="Categoria",orientation="h",text_auto=".0f"); fig.update_traces(marker_color=["#20B486","#8B6FE8","#4B9AF5","#F6A23A","#27B8C7"]); apply_chart_theme(fig, height=380, showlegend=False); st.plotly_chart(fig,use_container_width=True)
    with y:
        st.subheader("Margen por categoría"); fig=px.bar(cat.sort_values("Margen_%"),x="Margen_%",y="Categoria",orientation="h",text_auto=".1f"); fig.update_traces(marker_color=["#4B9AF5","#20B486","#8B6FE8","#F6A23A","#27B8C7"]); apply_chart_theme(fig, height=380, showlegend=False); st.plotly_chart(fig,use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.dataframe(cat,use_container_width=True,hide_index=True)

elif page=="Análisis":
    st.header("Análisis"); st.caption("Explora los datos actuales.")
    st.dataframe(f.describe(include="all").transpose().reset_index().rename(columns={"index":"Campo"}),use_container_width=True)
    st.subheader("Ventas por categoría y canal")
    st.dataframe(pd.pivot_table(f,index="Categoria",columns="Canal_Venta",values="Ventas_Soles",aggfunc="sum",fill_value=0),use_container_width=True)

elif page=="Simulador":
    st.header("Simulador"); st.caption("Mueve los controles y observa el impacto inmediatamente.")
    if f.empty: st.warning("No hay datos para simular.")
    else:
        product=st.selectbox("Producto",sorted(f.Producto.unique()))
        base=f[f.Producto==product]
        base_sales=float(base.Ventas_Soles.sum()); base_profit=float(base.Utilidad_Soles.sum())
        base_units=float(base.Cantidad.sum()) if "Cantidad" in base else max(1,len(base))
        base_price=base_sales/base_units if base_units else 0
        base_cost=max(0,(base_sales-base_profit)/base_units) if base_units else 0
        a,b,c,d=st.columns(4)
        pc=a.slider("Cambio de precio",-50,50,0,1,format="%d%%")
        qc=b.slider("Cambio de cantidad",-50,100,0,1,format="%d%%")
        cc=c.slider("Cambio de costo",-50,50,0,1,format="%d%%")
        dc=d.slider("Cambio de demanda",-50,100,0,1,format="%d%%")
        sp=base_price*(1+pc/100); su=base_units*(1+qc/100)*(1+dc/100); sco=base_cost*(1+cc/100)
        ss=sp*su; sprofit=(sp-sco)*su; sm=margin(ss,sprofit)
        r1,r2,r3=st.columns(3); r1.metric("Ventas simuladas",money(ss),f"{ss-base_sales:+,.0f}"); r2.metric("Utilidad simulada",money(sprofit),f"{sprofit-base_profit:+,.0f}"); r3.metric("Margen simulado",f"{sm:.1f}%",f"{sm-margin(base_sales,base_profit):+.1f} pp")
        fig=go.Figure([go.Bar(name="Actual",x=["Ventas","Utilidad"],y=[base_sales,base_profit],marker_color="#AFC8E8"),go.Bar(name="Simulado",x=["Ventas","Utilidad"],y=[ss,sprofit],marker_color="#4B9AF5")])
        apply_chart_theme(fig, height=330, showlegend=True); fig.update_layout(barmode="group"); st.plotly_chart(fig,use_container_width=True)
        if sprofit>base_profit: st.success("El escenario mejora la utilidad estimada.")
        elif sprofit<base_profit: st.warning("El escenario reduce la utilidad estimada.")
        else: st.info("El escenario mantiene una utilidad similar.")
