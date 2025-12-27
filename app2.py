import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Auditoría Técnica - Kepler Labs",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Datos simulados de una auditoría técnica
@st.cache_data
def cargar_datos_auditoria():
    # Evaluación por categorías
    evaluacion_df = pd.DataFrame({
        'Categoría': ['Infraestructura', 'Seguridad', 'Código', 'Documentación', 
                      'Rendimiento', 'Mantenibilidad', 'Escalabilidad', 'Monitoreo'],
        'Puntuación': [65, 45, 55, 30, 70, 40, 50, 35],
        'Crítico': [2, 4, 3, 5, 1, 4, 2, 3],
        'Medio': [3, 2, 4, 3, 2, 3, 4, 4],
        'Bajo': [1, 1, 2, 1, 3, 2, 2, 2]
    })
    
    # Hallazgos críticos
    hallazgos_df = pd.DataFrame({
        'ID': ['HAL-001', 'HAL-002', 'HAL-003', 'HAL-004', 'HAL-005'],
        'Título': [
            'Credenciales hardcodeadas en repositorio',
            'Sin backup automatizado de base de datos',
            'API sin rate limiting',
            'Documentación técnica inexistente',
            'Logs sin centralizar ni monitorear'
        ],
        'Severidad': ['Crítico', 'Crítico', 'Alto', 'Medio', 'Alto'],
        'Área': ['Seguridad', 'Infraestructura', 'Seguridad', 'Documentación', 'Monitoreo'],
        'Esfuerzo': ['2-3 días', '1 semana', '3-4 días', '2 semanas', '1 semana'],
        'Impacto': ['Alto', 'Crítico', 'Alto', 'Medio', 'Alto']
    })
    
    # Deuda técnica estimada
    deuda_tecnica_df = pd.DataFrame({
        'Componente': ['Sistema Legacy', 'Integraciones', 'Testing', 'Documentación', 'Infraestructura'],
        'Horas': [240, 120, 180, 160, 100],
        'Costo_USD': [18000, 9000, 13500, 12000, 7500]
    })
    
    # Recomendaciones priorizadas
    recomendaciones_df = pd.DataFrame({
        'Prioridad': ['P0', 'P0', 'P1', 'P1', 'P2', 'P2', 'P3'],
        'Acción': [
            'Implementar gestión de secretos (Vault/AWS Secrets)',
            'Configurar backup automatizado con retención 30 días',
            'Agregar rate limiting y throttling en APIs',
            'Implementar logging centralizado (ELK/Datadog)',
            'Crear documentación arquitectónica básica',
            'Implementar CI/CD pipeline básico',
            'Configurar monitoreo de métricas clave'
        ],
        'Impacto': ['Crítico', 'Crítico', 'Alto', 'Alto', 'Medio', 'Medio', 'Medio'],
        'Esfuerzo': ['Corto', 'Medio', 'Corto', 'Medio', 'Largo', 'Medio', 'Corto']
    })
    
    # Métricas del sistema actual
    metricas_sistema = {
        'uptime': 94.2,
        'tiempo_respuesta_promedio': 850,
        'errores_mensuales': 1247,
        'cobertura_tests': 23,
        'incidentes_mes': 8,
        'tiempo_resolucion_promedio': 6.5
    }
    
    return evaluacion_df, hallazgos_df, deuda_tecnica_df, recomendaciones_df, metricas_sistema

# Cargar datos
evaluacion_df, hallazgos_df, deuda_tecnica_df, recomendaciones_df, metricas_sistema = cargar_datos_auditoria()

# Sidebar
with st.sidebar:
    st.markdown("# 🔍 Kepler Labs")
    st.caption("Auditoría Técnica de Sistemas")
    st.divider()
    
    st.markdown("### 📋 Secciones")
    seccion = st.radio(
        "Navegación:",
        ["📊 Resumen Ejecutivo", "⚠️ Hallazgos", "💰 Deuda Técnica", 
         "🎯 Recomendaciones", "📈 Métricas Actuales"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("### 📄 Información del Proyecto")
    st.write("**Cliente:** EmpresaTech SRL")
    st.write("**Fecha:** 27 Dic 2024")
    st.write("**Auditor:** Kepler Labs")
    st.write("**Sistemas:** 3 aplicaciones web, 2 APIs, 1 base de datos")
    
    st.divider()
    
    st.info("**Nota:** Esta es una demo de reporte de auditoría técnica con datos simulados.")
    
    st.divider()
    st.caption(f"Generado: {datetime.now().strftime('%d/%m/%Y')}")

# Header
st.title("🔍 Reporte de Auditoría Técnica")
st.markdown("**Análisis integral de sistemas, infraestructura y procesos técnicos**")
st.divider()

# Resumen Ejecutivo
if seccion == "📊 Resumen Ejecutivo":
    st.header("📊 Resumen Ejecutivo")
    
    # Estado general
    puntuacion_general = evaluacion_df['Puntuación'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        color = "🔴" if puntuacion_general < 50 else "🟡" if puntuacion_general < 70 else "🟢"
        st.metric("Estado General", f"{color} {puntuacion_general:.0f}/100")
    with col2:
        total_criticos = evaluacion_df['Crítico'].sum()
        st.metric("Hallazgos Críticos", total_criticos, delta="Requieren atención inmediata", delta_color="inverse")
    with col3:
        costo_total = deuda_tecnica_df['Costo_USD'].sum()
        st.metric("Deuda Técnica Estimada", f"${costo_total:,.0f} USD")
    
    st.divider()
    
    # Evaluación por categorías
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Evaluación por Categoría")
        
        # Crear gráfico de barras horizontales con colores según puntuación
        fig_eval = go.Figure()
        
        colors = ['#ef4444' if x < 50 else '#f59e0b' if x < 70 else '#10b981' 
                  for x in evaluacion_df['Puntuación']]
        
        fig_eval.add_trace(go.Bar(
            y=evaluacion_df['Categoría'],
            x=evaluacion_df['Puntuación'],
            orientation='h',
            marker=dict(color=colors),
            text=evaluacion_df['Puntuación'],
            textposition='outside'
        ))
        
        fig_eval.update_layout(
            height=400,
            xaxis_title="Puntuación",
            xaxis=dict(range=[0, 100]),
            showlegend=False
        )
        
        st.plotly_chart(fig_eval, use_container_width=True)
    
    with col2:
        st.subheader("📊 Distribución de Hallazgos")
        
        # Preparar datos para el gráfico de burbujas
        total_hallazgos = evaluacion_df[['Crítico', 'Medio', 'Bajo']].sum()
        
        fig_dist = go.Figure()
        
        severidades = ['Crítico', 'Medio', 'Bajo']
        colores = ['#ef4444', '#f59e0b', '#3b82f6']
        valores = [total_hallazgos['Crítico'], total_hallazgos['Medio'], total_hallazgos['Bajo']]
        
        fig_dist.add_trace(go.Bar(
            x=severidades,
            y=valores,
            marker=dict(color=colores),
            text=valores,
            textposition='outside'
        ))
        
        fig_dist.update_layout(
            height=400,
            yaxis_title="Cantidad",
            showlegend=False
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
    
    st.divider()
    
    # Resumen de áreas críticas
    st.subheader("🚨 Áreas que Requieren Atención Inmediata")
    
    areas_criticas = evaluacion_df[evaluacion_df['Puntuación'] < 50].sort_values('Puntuación')
    
    for idx, row in areas_criticas.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"### 🔴 {row['Categoría']}")
        with col2:
            st.metric("Puntuación", f"{row['Puntuación']}/100")
        with col3:
            st.metric("Críticos", row['Crítico'])
        
        st.write(f"**Problemas identificados:** {row['Crítico']} críticos, {row['Medio']} medios, {row['Bajo']} bajos")
        st.divider()

# Hallazgos
elif seccion == "⚠️ Hallazgos":
    st.header("⚠️ Hallazgos Detallados")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        filtro_severidad = st.multiselect(
            "Filtrar por severidad:",
            options=['Crítico', 'Alto', 'Medio', 'Bajo'],
            default=['Crítico', 'Alto']
        )
    with col2:
        filtro_area = st.multiselect(
            "Filtrar por área:",
            options=hallazgos_df['Área'].unique(),
            default=hallazgos_df['Área'].unique()
        )
    
    # Aplicar filtros
    hallazgos_filtrados = hallazgos_df[
        (hallazgos_df['Severidad'].isin(filtro_severidad)) &
        (hallazgos_df['Área'].isin(filtro_area))
    ]
    
    st.divider()
    
    # Mostrar hallazgos
    for idx, row in hallazgos_filtrados.iterrows():
        severidad_color = {
            'Crítico': '🔴',
            'Alto': '🟠',
            'Medio': '🟡',
            'Bajo': '🔵'
        }
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"## {severidad_color[row['Severidad']]} {row['ID']}: {row['Título']}")
        
        with col2:
            st.metric("Severidad", row['Severidad'])
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.write(f"**Área:** {row['Área']}")
        with col_b:
            st.write(f"**Impacto:** {row['Impacto']}")
        with col_c:
            st.write(f"**Esfuerzo estimado:** {row['Esfuerzo']}")
        
        # Descripción según el hallazgo
        if row['ID'] == 'HAL-001':
            st.write("""
            **Descripción:** Se encontraron credenciales de acceso (API keys, contraseñas de BD) 
            hardcodeadas directamente en el código fuente y versionadas en Git.
            
            **Riesgo:** Exposición de credenciales sensibles. Cualquier persona con acceso al repositorio 
            puede obtener acceso completo a sistemas críticos.
            
            **Recomendación:** Implementar gestión de secretos con herramientas como HashiCorp Vault, 
            AWS Secrets Manager o variables de entorno seguras. Rotar inmediatamente todas las credenciales expuestas.
            """)
        elif row['ID'] == 'HAL-002':
            st.write("""
            **Descripción:** No existe sistema de backup automatizado para la base de datos de producción. 
            Los backups se realizan manualmente de forma irregular.
            
            **Riesgo:** Pérdida total de datos en caso de falla de hardware, corrupción o error humano. 
            Sin capacidad de recuperación ante desastres.
            
            **Recomendación:** Configurar backups automáticos diarios con retención de 30 días, 
            implementar snapshots incrementales y realizar pruebas de restauración mensuales.
            """)
        else:
            st.write("**Descripción detallada y recomendaciones técnicas disponibles en el reporte completo.**")
        
        st.divider()

# Deuda Técnica
elif seccion == "💰 Deuda Técnica":
    st.header("💰 Análisis de Deuda Técnica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribución por Componente")
        
        fig_deuda = px.pie(
            deuda_tecnica_df,
            values='Horas',
            names='Componente',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_deuda.update_traces(textposition='inside', textinfo='percent+label')
        fig_deuda.update_layout(height=400)
        
        st.plotly_chart(fig_deuda, use_container_width=True)
    
    with col2:
        st.subheader("💵 Costo Estimado por Área")
        
        fig_costo = px.bar(
            deuda_tecnica_df.sort_values('Costo_USD', ascending=True),
            x='Costo_USD',
            y='Componente',
            orientation='h',
            color='Costo_USD',
            color_continuous_scale='Reds'
        )
        fig_costo.update_layout(height=400, showlegend=False, xaxis_title="USD")
        
        st.plotly_chart(fig_costo, use_container_width=True)
    
    st.divider()
    
    # Tabla detallada
    st.subheader("📋 Desglose Detallado")
    
    deuda_display = deuda_tecnica_df.copy()
    deuda_display['Horas'] = deuda_display['Horas'].apply(lambda x: f"{x}h")
    deuda_display['Costo_USD'] = deuda_display['Costo_USD'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(
        deuda_display,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Componente": "Componente del Sistema",
            "Horas": "Esfuerzo Estimado",
            "Costo_USD": "Costo (USD)"
        }
    )
    
    st.divider()
    
    # Resumen
    col1, col2 = st.columns(2)
    with col1:
        total_horas = deuda_tecnica_df['Horas'].sum()
        st.metric("Total Horas de Trabajo", f"{total_horas}h", 
                  help="Aproximadamente 5-6 meses de trabajo de 1 desarrollador")
    with col2:
        total_costo = deuda_tecnica_df['Costo_USD'].sum()
        st.metric("Inversión Total Estimada", f"${total_costo:,.0f} USD")

# Recomendaciones
elif seccion == "🎯 Recomendaciones":
    st.header("🎯 Plan de Acción Recomendado")
    
    st.markdown("""
    Las siguientes recomendaciones están priorizadas según impacto y urgencia:
    - **P0:** Acción inmediata (1-2 semanas)
    - **P1:** Corto plazo (1-2 meses)
    - **P2:** Mediano plazo (3-6 meses)
    - **P3:** Largo plazo (6+ meses)
    """)
    
    st.divider()
    
    # Agrupar por prioridad
    for prioridad in ['P0', 'P1', 'P2', 'P3']:
        recs = recomendaciones_df[recomendaciones_df['Prioridad'] == prioridad]
        
        if len(recs) > 0:
            prioridad_info = {
                'P0': ('🔴', 'Crítico - Acción Inmediata'),
                'P1': ('🟠', 'Alta - Corto Plazo'),
                'P2': ('🟡', 'Media - Mediano Plazo'),
                'P3': ('🔵', 'Baja - Largo Plazo')
            }
            
            icon, titulo = prioridad_info[prioridad]
            st.subheader(f"{icon} {prioridad}: {titulo}")
            
            for idx, row in recs.iterrows():
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    st.write(f"**{row['Acción']}**")
                with col2:
                    st.write(f"Impacto: {row['Impacto']}")
                with col3:
                    st.write(f"Esfuerzo: {row['Esfuerzo']}")
            
            st.divider()
    
    # Roadmap visual
    st.subheader("🗓️ Roadmap Sugerido")
    
    roadmap_data = pd.DataFrame({
        'Fase': ['Mes 1-2', 'Mes 3-4', 'Mes 5-6', 'Mes 7+'],
        'Acciones': [
            'P0: Seguridad crítica y backups',
            'P1: Monitoreo y logging',
            'P2: Documentación y CI/CD',
            'P3: Optimizaciones y mejoras'
        ],
        'Progreso': [0, 0, 0, 0]
    })
    
    st.dataframe(
        roadmap_data,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Fase": "Período",
            "Acciones": "Acciones Principales",
            "Progreso": st.column_config.ProgressColumn(
                "Progreso",
                min_value=0,
                max_value=100
            )
        }
    )

# Métricas Actuales
elif seccion == "📈 Métricas Actuales":
    st.header("📈 Estado Actual del Sistema")
    
    # KPIs principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        uptime_color = "🔴" if metricas_sistema['uptime'] < 95 else "🟡" if metricas_sistema['uptime'] < 99 else "🟢"
        st.metric(
            "Uptime", 
            f"{uptime_color} {metricas_sistema['uptime']}%",
            delta=f"{metricas_sistema['uptime'] - 99.9:.1f}% vs objetivo",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Tiempo de Respuesta", 
            f"{metricas_sistema['tiempo_respuesta_promedio']}ms",
            delta="+350ms vs benchmark",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Cobertura de Tests", 
            f"{metricas_sistema['cobertura_tests']}%",
            delta="-57% vs estándar (80%)",
            delta_color="inverse"
        )
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Errores Mensuales", 
            f"{metricas_sistema['errores_mensuales']:,}",
            help="Errores 5xx registrados en el último mes"
        )
    
    with col2:
        st.metric(
            "Incidentes/Mes", 
            metricas_sistema['incidentes_mes'],
            delta="+3 vs mes anterior",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Tiempo Resolución", 
            f"{metricas_sistema['tiempo_resolucion_promedio']}h",
            help="Tiempo promedio de resolución de incidentes"
        )
    
    st.divider()
    
    # Comparación con benchmarks
    st.subheader("📊 Comparación con Estándares de la Industria")
    
    benchmarks = pd.DataFrame({
        'Métrica': ['Uptime', 'Cobertura Tests', 'Tiempo Respuesta', 'MTTR'],
        'Actual': [94.2, 23, 850, 6.5],
        'Estándar Industria': [99.9, 80, 500, 2],
        'Gap': [-5.7, -57, 350, 4.5]
    })
    
    fig_bench = go.Figure()
    
    fig_bench.add_trace(go.Bar(
        name='Actual',
        x=benchmarks['Métrica'],
        y=benchmarks['Actual'],
        marker_color='#ef4444'
    ))
    
    fig_bench.add_trace(go.Bar(
        name='Estándar',
        x=benchmarks['Métrica'],
        y=benchmarks['Estándar Industria'],
        marker_color='#10b981'
    ))
    
    fig_bench.update_layout(
        barmode='group',
        height=400,
        yaxis_title="Valor"
    )
    
    st.plotly_chart(fig_bench, use_container_width=True)
    
    st.divider()
    
    # Alertas y observaciones
    st.subheader("⚠️ Observaciones Clave")
    
    st.warning("**Uptime por debajo del SLA:** El sistema tiene un uptime de 94.2%, significativamente inferior al objetivo de 99.9%. Esto representa aproximadamente 42 horas de downtime al mes.")
    
    st.error("**Cobertura de tests crítica:** Con solo 23% de cobertura, el sistema está altamente expuesto a regresiones y errores en producción.")
    
    st.info("**Tiempo de respuesta elevado:** Los 850ms promedio sugieren problemas de rendimiento o queries ineficientes que afectan la experiencia de usuario.")

# Footer
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 🔍 Auditoría Técnica")
    st.markdown("**Desarrollado por Kepler Labs**")
    st.caption("Consultoría tecnológica y soluciones de software © 2024")
    st.caption("Email: info@keplerlabs.com | WhatsApp: +54 9 264 580 2870")