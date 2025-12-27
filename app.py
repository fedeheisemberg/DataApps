import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Dashboard BI PyME",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sin CSS personalizado - usando estilos nativos de Streamlit

# Datos simulados
@st.cache_data
def cargar_datos():
    # Ventas mensuales
    ventas_df = pd.DataFrame({
        'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
        'Ventas': [45000, 52000, 48000, 61000, 58000, 67000],
        'Costos': [28000, 31000, 29000, 35000, 33000, 38000],
        'Clientes': [120, 135, 128, 156, 148, 172]
    })
    ventas_df['Margen'] = ((ventas_df['Ventas'] - ventas_df['Costos']) / ventas_df['Ventas'] * 100).round(1)
    
    # Productos top
    productos_df = pd.DataFrame({
        'Producto': ['Cemento 50kg', 'Pintura látex 20L', 'Hierro 12mm x6m', 
                     'Alambre tejido', 'Ladrillos comunes'],
        'Ventas': [8500, 6200, 5800, 4200, 3900],
        'Stock': [45, 23, 67, 12, 89],
        'Categoria': ['Materiales', 'Pinturería', 'Materiales', 'Materiales', 'Materiales']
    })
    
    # Categorías
    categorias_df = pd.DataFrame({
        'Categoria': ['Materiales', 'Herramientas', 'Pinturería', 'Otros'],
        'Porcentaje': [45, 25, 20, 10]
    })
    
    # Alertas de stock
    alertas_df = pd.DataFrame({
        'Producto': ['Alambre tejido', 'Pintura látex 20L', 'Cemento 50kg'],
        'Stock': [12, 23, 45],
        'Nivel': ['Crítico', 'Bajo', 'Medio']
    })
    
    # Últimas ventas
    ultimas_ventas_df = pd.DataFrame({
        'ID': ['V-1245', 'V-1246', 'V-1247', 'V-1248', 'V-1249'],
        'Cliente': ['Constructora Lopez', 'Juan Pérez', 'Obras Martinez', 
                    'María González', 'Roberto Sánchez'],
        'Monto': [12500, 3400, 8900, 1200, 5600],
        'Fecha': ['15/06/2024', '15/06/2024', '14/06/2024', '14/06/2024', '13/06/2024']
    })
    
    return ventas_df, productos_df, categorias_df, alertas_df, ultimas_ventas_df

# Cargar datos
ventas_df, productos_df, categorias_df, alertas_df, ultimas_ventas_df = cargar_datos()

# Header
st.title("📊 Dashboard BI - PyME")
st.markdown("Sistema de análisis centralizado de datos empresariales")
st.divider()

# Sidebar
with st.sidebar:
    st.markdown("# 🏗️ Ferretería El Constructor")
    st.caption("Sistema de análisis BI")
    st.divider()
    st.markdown("### 🎯 Navegación")
    
    vista = st.radio(
        "Selecciona una vista:",
        ["🏠 General", "💰 Ventas", "📦 Productos", "👥 Clientes"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("### 📅 Período")
    periodo = st.selectbox(
        "Seleccionar período",
        ["Últimos 6 meses", "Último trimestre", "Último mes", "Año completo"]
    )
    
    st.divider()
    st.info("**Demo Portfolio**\n\nDashboard BI para centralizar datos de PyMEs")
    
    st.divider()
    st.caption(f"**Última actualización:**\n{datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Vista General
if vista == "🏠 General":
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ventas = ventas_df['Ventas'].sum()
        st.metric(
            label="💵 Ventas Totales",
            value=f"${total_ventas:,.0f}",
            delta="Últimos 6 meses"
        )
    
    with col2:
        margen_promedio = ventas_df['Margen'].mean()
        st.metric(
            label="📈 Margen Promedio",
            value=f"{margen_promedio:.1f}%",
            delta="Rentabilidad"
        )
    
    with col3:
        clientes_actuales = ventas_df['Clientes'].iloc[-1]
        st.metric(
            label="👥 Clientes Activos",
            value=f"{clientes_actuales}",
            delta="+24 vs mes anterior"
        )
    
    with col4:
        productos_criticos = len(alertas_df)
        st.metric(
            label="⚠️ Productos Críticos",
            value=f"{productos_criticos}",
            delta="Requieren atención",
            delta_color="inverse"
        )
    
    st.divider()
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Evolución de Ventas")
        fig_ventas = go.Figure()
        fig_ventas.add_trace(go.Scatter(
            x=ventas_df['Mes'], 
            y=ventas_df['Ventas'],
            mode='lines+markers',
            name='Ventas',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        fig_ventas.add_trace(go.Scatter(
            x=ventas_df['Mes'], 
            y=ventas_df['Costos'],
            mode='lines+markers',
            name='Costos',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8)
        ))
        fig_ventas.update_layout(
            height=350,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_ventas, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Distribución por Categoría")
        fig_categorias = px.pie(
            categorias_df,
            values='Porcentaje',
            names='Categoria',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_categorias.update_traces(textposition='inside', textinfo='percent+label')
        fig_categorias.update_layout(height=350)
        st.plotly_chart(fig_categorias, use_container_width=True)
    
    st.divider()
    
    # Alertas y últimas ventas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚠️ Alertas de Stock")
        for idx, row in alertas_df.iterrows():
            icon_map = {"Crítico": "🔴", "Bajo": "🟡", "Medio": "🔵"}
            
            st.markdown(f"### {icon_map[row['Nivel']]} {row['Producto']}")
            st.write(f"**Stock:** {row['Stock']} unidades | **Nivel:** {row['Nivel']}")
            if idx < len(alertas_df) - 1:
                st.divider()
    
    with col2:
        st.subheader("📄 Últimas Ventas")
        for idx, row in ultimas_ventas_df.head(3).iterrows():
            st.markdown(f"### {row['ID']} - {row['Cliente']}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Monto", f"${row['Monto']:,.0f}")
            with col_b:
                st.write(f"**Fecha:** {row['Fecha']}")
            if idx < 2:
                st.divider()

# Vista Ventas
elif vista == "💰 Ventas":
    st.header("💰 Análisis de Ventas")
    
    # Métricas de ventas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        venta_promedio = ventas_df['Ventas'].mean()
        st.metric("Venta Promedio Mensual", f"${venta_promedio:,.0f}")
    
    with col2:
        mejor_mes = ventas_df.loc[ventas_df['Ventas'].idxmax(), 'Mes']
        mejor_venta = ventas_df['Ventas'].max()
        st.metric(f"Mejor Mes: {mejor_mes}", f"${mejor_venta:,.0f}")
    
    with col3:
        crecimiento = ((ventas_df['Ventas'].iloc[-1] / ventas_df['Ventas'].iloc[0]) - 1) * 100
        st.metric("Crecimiento", f"{crecimiento:.1f}%", delta=f"{crecimiento:.1f}%")
    
    st.divider()
    
    # Gráfico de barras comparativo
    st.subheader("📊 Ventas vs Costos Mensual")
    fig_barras = go.Figure()
    fig_barras.add_trace(go.Bar(
        x=ventas_df['Mes'],
        y=ventas_df['Ventas'],
        name='Ventas',
        marker_color='#1f77b4'
    ))
    fig_barras.add_trace(go.Bar(
        x=ventas_df['Mes'],
        y=ventas_df['Costos'],
        name='Costos',
        marker_color='#ff7f0e'
    ))
    fig_barras.update_layout(barmode='group', height=400)
    st.plotly_chart(fig_barras, use_container_width=True)
    
    st.divider()
    
    # Evolución de clientes y margen
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Evolución de Clientes")
        fig_clientes = px.line(
            ventas_df,
            x='Mes',
            y='Clientes',
            markers=True,
            line_shape='spline'
        )
        fig_clientes.update_traces(line_color='#2ca02c', line_width=3, marker_size=10)
        fig_clientes.update_layout(height=350)
        st.plotly_chart(fig_clientes, use_container_width=True)
    
    with col2:
        st.subheader("📈 Margen de Ganancia (%)")
        fig_margen = px.bar(
            ventas_df,
            x='Mes',
            y='Margen',
            color='Margen',
            color_continuous_scale='RdYlGn'
        )
        fig_margen.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_margen, use_container_width=True)

# Vista Productos
elif vista == "📦 Productos":
    st.header("📦 Análisis de Productos")
    
    # Métricas de productos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_productos = len(productos_df)
        st.metric("Total Productos", total_productos)
    
    with col2:
        producto_top = productos_df.loc[productos_df['Ventas'].idxmax(), 'Producto']
        st.metric("Producto Top", producto_top)
    
    with col3:
        stock_total = productos_df['Stock'].sum()
        st.metric("Stock Total", f"{stock_total} unidades")
    
    st.divider()
    
    # Top productos
    st.subheader("🏆 Top 5 Productos por Ventas")
    fig_top = px.bar(
        productos_df.sort_values('Ventas', ascending=True),
        x='Ventas',
        y='Producto',
        orientation='h',
        color='Ventas',
        color_continuous_scale='Blues'
    )
    fig_top.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_top, use_container_width=True)
    
    st.divider()
    
    # Tabla de inventario
    st.subheader("📋 Inventario Actual")
    
    # Agregar columna de estado
    def estado_stock(stock):
        if stock < 30:
            return '🔴 Bajo'
        elif stock < 50:
            return '🟡 Medio'
        else:
            return '🟢 Bueno'
    
    productos_display = productos_df.copy()
    productos_display['Estado'] = productos_display['Stock'].apply(estado_stock)
    productos_display['Ventas'] = productos_display['Ventas'].apply(lambda x: f"${x:,.0f}")
    productos_display['Stock'] = productos_display['Stock'].apply(lambda x: f"{x} unidades")
    
    st.dataframe(
        productos_display,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Producto": st.column_config.TextColumn("Producto", width="large"),
            "Ventas": st.column_config.TextColumn("Ventas"),
            "Stock": st.column_config.TextColumn("Stock"),
            "Categoria": st.column_config.TextColumn("Categoría"),
            "Estado": st.column_config.TextColumn("Estado")
        }
    )

# Vista Clientes
elif vista == "👥 Clientes":
    st.header("👥 Análisis de Clientes")
    
    # Métricas de clientes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Clientes", "452", delta="Registrados")
    
    with col2:
        st.metric("Nuevos este Mes", "28", delta="+12%")
    
    with col3:
        ticket_promedio = ultimas_ventas_df['Monto'].mean()
        st.metric("Ticket Promedio", f"${ticket_promedio:,.0f}")
    
    st.divider()
    
    # Últimas ventas detalladas
    st.subheader("🛒 Ventas Recientes por Cliente")
    
    for idx, row in ultimas_ventas_df.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{row['Cliente']}**")
            st.caption(f"ID: {row['ID']}")
        
        with col2:
            st.metric("", f"${row['Monto']:,.0f}")
        
        with col3:
            st.markdown(f"📅 {row['Fecha']}")
        
        st.divider()
    
    # Gráfico de distribución de montos
    st.subheader("💵 Distribución de Montos de Venta")
    fig_montos = px.histogram(
        ultimas_ventas_df,
        x='Monto',
        nbins=10,
        color_discrete_sequence=['#1f77b4']
    )
    fig_montos.update_layout(
        height=300,
        showlegend=False,
        xaxis_title="Monto de Venta",
        yaxis_title="Frecuencia"
    )
    st.plotly_chart(fig_montos, use_container_width=True)

# Footer
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 📊 Dashboard BI para PyMEs")
    st.markdown("**Desarrollado por Kepler Labs**")
    st.caption("Sistema de análisis empresarial centralizado © 2024")