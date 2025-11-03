import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def mostrar_dashboard_principal(analytics):
    """Mostrar el dashboard principal"""
    st.markdown('<div class="sub-header">📊 Dashboard de Análisis Académico</div>', unsafe_allow_html=True)
    
    
    metricas = analytics.calcular_metricas_principales()
    
    
    if metricas['total_estudiantes'] > 0:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Estudiantes", metricas['total_estudiantes'])
        with col2:
            st.metric("Calificaciones", metricas['total_calificaciones'])  
        with col3:
            st.metric("Aprobación", f"{metricas['tasa_aprobacion']}%")
        with col4:
            st.metric("Reprobación", f"{metricas['tasa_reprobacion']}%")
        with col5:
            st.metric("Deserción", f"{metricas['tasa_desercion']}%")
        
        
        col1, col2 = st.columns(2)
        
        with col1:
            mostrar_distribucion_calificaciones(analytics.df_calificaciones)  
        
        with col2:
            mostrar_analisis_asistencia(analytics.df_calificaciones) 
        

        col1, col2 = st.columns(2)
        
        with col1:
            mostrar_tendencia_unidades(analytics)
        
  
        st.subheader("📈 Análisis de Rendimiento")
        analisis_rendimiento = analytics.generar_analisis_rendimiento()
        if not analisis_rendimiento.empty:
            st.dataframe(analisis_rendimiento)
        else:
            st.info("No hay datos de rendimiento para analizar")
        

        st.subheader("⚠️ Factores de Riesgo")
        factores_riesgo = analytics.analizar_factores_riesgo()
        if not factores_riesgo.empty:
            st.dataframe(factores_riesgo)
        else:
            st.info("No hay factores de riesgo registrados")
            
    else:
        st.info("💡 No hay datos disponibles. Comienza agregando estudiantes y calificaciones en la pestaña 'Registro de Datos'.")

def mostrar_distribucion_calificaciones(df_calificaciones):  
    """Mostrar distribución de calificaciones con Matplotlib"""
    st.subheader("📊 Distribución de Calificaciones")
    
    if df_calificaciones.empty or 'calificacion_final' not in df_calificaciones.columns:
        st.info("No hay datos de calificaciones para mostrar")
        return
    
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
  
        ax.hist(df_calificaciones['calificacion_final'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        
        ax.axvline(x=70, color='red', linestyle='--', linewidth=2, label='Límite Aprobación (70)')
        
        ax.set_xlabel('Calificación Final')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Distribución de Calificaciones Finales')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error creando gráfica: {e}")

def mostrar_analisis_asistencia(df_calificaciones):  
    """Mostrar análisis de asistencia con Matplotlib"""
    st.subheader("🎯 Análisis de Asistencia")
    
    if df_calificaciones.empty or 'asistencia' not in df_calificaciones.columns:
        st.info("No hay datos de asistencia para mostrar")
        return
    
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        

        ax.boxplot(df_calificaciones['asistencia'])
        ax.set_ylabel('Porcentaje de Asistencia')
        ax.set_title('Distribución de Asistencia')
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error creando gráfica: {e}")

def mostrar_tendencia_unidades(analytics):
    """Mostrar tendencia de unidades con Matplotlib"""
    st.subheader("📈 Tendencia por Unidades")
    
    tendencia = analytics.obtener_tendencia_calificaciones()
    
    if not tendencia.empty:
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            unidades = tendencia['Unidad'].tolist()
            promedios = tendencia['Promedio'].tolist()
            
            ax.bar(unidades, promedios, color=['#ff9999', '#66b3ff', '#99ff99'])
            ax.set_xlabel('Unidad')
            ax.set_ylabel('Calificación Promedio')
            ax.set_title('Tendencia de Calificaciones por Unidad')
            ax.grid(True, alpha=0.3)
            
            for i, v in enumerate(promedios):
                ax.text(i, v + 0.5, f'{v:.1f}', ha='center', va='bottom')
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error creando gráfica: {e}")
    else:
        st.info("No hay datos de unidades para mostrar")