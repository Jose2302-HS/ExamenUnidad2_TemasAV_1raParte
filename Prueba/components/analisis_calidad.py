import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def mostrar_analisis_calidad(analytics):
    """Mostrar análisis de calidad con herramientas visuales actualizadas"""
    st.markdown('<div class="sub-header">🔍 Herramientas de Análisis de Calidad</div>', unsafe_allow_html=True)
    

    st.subheader("Selecciona una herramienta de calidad:")
    
    herramienta = st.radio(
        "",
        ["Diagrama de Pareto", "Diagrama de Dispersión", "Histograma", "Gráfico de Control"],
        horizontal=True
    )
    
    if herramienta == "Diagrama de Pareto":
        mostrar_pareto(analytics)
    elif herramienta == "Diagrama de Dispersión":
        mostrar_diagrama_dispersion(analytics)
    elif herramienta == "Histograma":
        mostrar_histograma(analytics)
    elif herramienta == "Gráfico de Control":
        mostrar_grafico_control(analytics)

def mostrar_pareto(analytics):
    """Mostrar diagrama de Pareto para factores de riesgo"""
    st.subheader("📊 Diagrama de Pareto - Factores de Riesgo")
    
    try:

        pareto_data = analytics.generar_grafico_pareto()
        

        if pareto_data is None or pareto_data.empty:
            st.info("📭 No hay factores de riesgo registrados para generar el diagrama de Pareto.")
            st.info("💡 Ve a 'Registro de Datos' → 'Registrar Factores' para agregar factores de riesgo.")
            return
        
        if len(pareto_data) == 0:
            st.info("📭 No hay factores de riesgo registrados para generar el diagrama de Pareto.")
            return
        
 
        fig, ax1 = plt.subplots(figsize=(12, 8))
        

        bars = ax1.bar(pareto_data['categoria'], pareto_data['frecuencia'], 
                      color='skyblue', edgecolor='black', alpha=0.7, label='Frecuencia')
        ax1.set_xlabel('Categorías de Factores de Riesgo')
        ax1.set_ylabel('Frecuencia', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.tick_params(axis='x', rotation=45)
        

        ax2 = ax1.twinx()
        ax2.plot(pareto_data['categoria'], pareto_data['porcentaje_acumulado'], 
                color='red', marker='o', linewidth=2, label='% Acumulado')
        ax2.set_ylabel('Porcentaje Acumulado (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.set_ylim(0, 100)
        
 
        ax2.axhline(y=80, color='green', linestyle='--', alpha=0.7, label='80%')
        
        plt.title('Diagrama de Pareto - Factores de Riesgo')
        fig.tight_layout()
        st.pyplot(fig)
        

        st.subheader("📈 Análisis de Resultados")
        

        factores_80 = pareto_data[pareto_data['porcentaje_acumulado'] <= 80]
        if not factores_80.empty:
            st.success(f"**Factores críticos (80% del impacto):** {len(factores_80)} categorías")
            for _, factor in factores_80.iterrows():
                st.write(f"• **{factor['categoria']}**: {factor['frecuencia']} ocurrencias ({factor['porcentaje_acumulado']:.1f}% acumulado)")
        
  
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Factores", pareto_data['frecuencia'].sum())
        with col2:
            st.metric("Categorías Críticas", len(factores_80))
        with col3:
            st.metric("Categorías Total", len(pareto_data))
            
    except Exception as e:
        st.error(f"❌ Error generando diagrama de Pareto: {e}")
        st.info("💡 Esto puede ser normal cuando no hay datos. Agrega factores de riesgo en 'Registro de Datos'.")

def mostrar_diagrama_dispersion(analytics):
    """Mostrar diagrama de dispersión interactivo"""
    st.info("**Diagrama de Dispersión:** Analiza la relación entre dos variables numéricas")
    

    try:
        datos_visual = analytics.obtener_datos_para_analisis_visual()
    except AttributeError:
        st.error("❌ Error: La función de análisis visual no está disponible")
        st.info("💡 Esto puede ser temporal. Intenta actualizar la página o agregar datos primero.")
        return
    
    if datos_visual.empty:
        st.warning("📭 No hay datos disponibles para análisis. Agrega datos en la pestaña 'Registro de Datos'.")
        return
    
 
    variables_disponibles = datos_visual.columns.tolist()
    
    if len(variables_disponibles) < 2:
        st.warning("❌ Se necesitan al menos 2 variables numéricas para el diagrama de dispersión")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        variable_x = st.selectbox(
            "Variable Eje X:",
            options=variables_disponibles,
            index=0
        )
    
    with col2:
        opciones_y = [v for v in variables_disponibles if v != variable_x]
        variable_y = st.selectbox(
            "Variable Eje Y:",
            options=opciones_y,
            index=0
        )
    

    fig, ax = plt.subplots(figsize=(10, 6))
    
 
    datos_validos = datos_visual[[variable_x, variable_y]].dropna()
    
    if len(datos_validos) > 0:

        scatter = ax.scatter(
            datos_validos[variable_x], 
            datos_validos[variable_y],
            alpha=0.7, 
            s=80,
            c='#2E86AB',
            edgecolors='white',
            linewidth=0.5
        )
        

        z = np.polyfit(datos_validos[variable_x], datos_validos[variable_y], 1)
        p = np.poly1d(z)
        ax.plot(datos_validos[variable_x], p(datos_validos[variable_x]), 
                "#F24236", linestyle="--", alpha=0.8, linewidth=2, label="Línea de tendencia")
        
 
        correlacion = datos_validos[variable_x].corr(datos_validos[variable_y])
        
        ax.set_xlabel(variable_x.replace('_', ' ').title(), fontsize=12)
        ax.set_ylabel(variable_y.replace('_', ' ').title(), fontsize=12)
        ax.set_title(f'Diagrama de Dispersión: {variable_x} vs {variable_y}', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        

        st.subheader("📈 Análisis de Correlación")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Coeficiente", f"{correlacion:.3f}")
        
        with col2:
            if abs(correlacion) > 0.7:
                fuerza = "Fuerte"
            elif abs(correlacion) > 0.4:
                fuerza = "Moderada"
            else:
                fuerza = "Débil"
            st.metric("Fuerza", fuerza)
        
        with col3:
            if correlacion > 0:
                direccion = "Positiva"
            else:
                direccion = "Negativa"
            st.metric("Dirección", direccion)
        

        st.info(f"""
        **Interpretación:** 
        - **Correlación {fuerza.lower()} {direccion.lower()}** entre **{variable_x}** y **{variable_y}**
        - Coeficiente: **{correlacion:.3f}**
        """)
        
    else:
        st.warning("No hay datos válidos para crear el diagrama de dispersión")

def mostrar_histograma(analytics):
    """Mostrar histograma de distribución"""
    st.info("**Histograma:** Visualiza la distribución de una variable numérica")
    
 
    try:
        datos_visual = analytics.obtener_datos_para_analisis_visual()
    except AttributeError:
        st.error("❌ Error: La función de análisis visual no está disponible")
        st.info("💡 Esto puede ser temporal. Intenta actualizar la página o agregar datos primero.")
        return
    
    if datos_visual.empty:
        st.warning("📭 No hay datos disponibles para análisis. Agrega datos en la pestaña 'Registro de Datos'.")
        return
    
 
    variables_disponibles = datos_visual.columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        variable = st.selectbox(
            "Selecciona la variable:",
            options=variables_disponibles,
            index=len(variables_disponibles)-1
        )
    
    with col2:
        bins = st.slider(
            "Número de intervalos:",
            min_value=5,
            max_value=30,
            value=15
        )
    

    fig, ax = plt.subplots(figsize=(10, 6))
    
    datos_validos = datos_visual[variable].dropna()
    
    if len(datos_validos) > 0:

        n, bins, patches = ax.hist(
            datos_validos, 
            bins=bins, 
            alpha=0.7, 
            color='#4CB963',
            edgecolor='black', 
            linewidth=0.5
        )
        

        media = datos_validos.mean()
        mediana = datos_validos.median()
        desviacion = datos_validos.std()
        

        ax.axvline(media, color='#F24236', linestyle='--', linewidth=2, 
                  label=f'Media: {media:.2f}')
        ax.axvline(mediana, color='#2E86AB', linestyle='--', linewidth=2, 
                  label=f'Mediana: {mediana:.2f}')
        
        ax.set_xlabel(variable.replace('_', ' ').title(), fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)
        ax.set_title(f'Distribución de {variable.replace("_", " ").title()}', 
                    fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        

        st.subheader("📊 Estadísticas Descriptivas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Media", f"{media:.2f}")
        with col2:
            st.metric("Mediana", f"{mediana:.2f}")
        with col3:
            st.metric("Desviación", f"{desviacion:.2f}")
        with col4:
            st.metric("Rango", f"{datos_validos.min():.1f}-{datos_validos.max():.1f}")
        
    else:
        st.warning("No hay datos válidos para crear el histograma")

def mostrar_grafico_control(analytics):
    """Mostrar gráfico de control simple"""
    st.info("**Gráfico de Control:** Monitorea la estabilidad de un proceso")
    
 
    try:
        datos_visual = analytics.obtener_datos_para_analisis_visual()
    except AttributeError:
        st.error("❌ Error: La función de análisis visual no está disponible")
        st.info("💡 Esto puede ser temporal. Intenta actualizar la página o agregar datos primero.")
        return
    
    if datos_visual.empty:
        st.warning("📭 No hay datos disponibles para análisis. Agrega datos en la pestaña 'Registro de Datos'.")
        return
    

    variables_disponibles = datos_visual.columns.tolist()
    
    variable = st.selectbox(
        "Selecciona la variable:",
        options=variables_disponibles,
        index=len(variables_disponibles)-1
    )
    
    datos_validos = datos_visual[variable].dropna()
    
    if len(datos_validos) > 0:
  
        media = datos_validos.mean()
        desviacion = datos_validos.std()
        
        lcs = media + 3 * desviacion
        lci = media - 3 * desviacion
        

        fig, ax = plt.subplots(figsize=(12, 6))
        

        ax.plot(range(len(datos_validos)), datos_validos.values, 
               marker='o', linewidth=2, markersize=4, color='#2E86AB', label=variable)
        

        ax.axhline(media, color='#4CB963', linestyle='-', linewidth=2, label=f'Media ({media:.2f})')
        ax.axhline(lcs, color='#F24236', linestyle='--', linewidth=1.5, label=f'LCS ({lcs:.2f})')
        ax.axhline(lci, color='#F24236', linestyle='--', linewidth=1.5, label=f'LCI ({lci:.2f})')
        
        ax.set_xlabel('Observaciones', fontsize=12)
        ax.set_ylabel(variable.replace('_', ' ').title(), fontsize=12)
        ax.set_title(f'Gráfico de Control - {variable.replace("_", " ").title()}', 
                    fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        

        puntos_fuera = datos_validos[(datos_validos > lcs) | (datos_validos < lci)]
        
        st.subheader("📋 Análisis de Control")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Observaciones", len(datos_validos))
        with col2:
            st.metric("Fuera Control", len(puntos_fuera))
        with col3:
            porcentaje = (len(puntos_fuera) / len(datos_validos)) * 100
            st.metric("% Fuera", f"{porcentaje:.1f}%")
        
        if len(puntos_fuera) > 0:
            st.warning(f"**Alerta:** {len(puntos_fuera)} puntos fuera de control")
        else:
            st.success("**Proceso estable**")
            
    else:
        st.warning("No hay datos válidos para el gráfico de control")