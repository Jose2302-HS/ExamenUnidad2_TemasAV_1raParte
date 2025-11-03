import streamlit as st
import pandas as pd
import numpy as np
from config.constants import CARRERAS, CATEGORIAS_FACTORES, SEMESTRES_INGRESO
from services.analytics import AnalyticsService

def mostrar_registro_datos(database_service):
    """Mostrar interfaz para registro de datos"""
    st.markdown('<div class="sub-header">📝 Registro de Datos</div>', unsafe_allow_html=True)
    

    analytics = AnalyticsService(database_service)
    

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 Importar desde Excel", 
        "👥 Registrar Estudiante", 
        "📚 Registrar Materias",
        "📊 Registrar Calificaciones",
        "⚠️ Registrar Factores"
    ])
    
    with tab1:
        mostrar_importar_excel(analytics)
    with tab2:
        mostrar_registro_estudiante(analytics)
    with tab3:
        mostrar_registro_materias(analytics)
    with tab4:
        mostrar_registro_calificaciones(analytics)
    with tab5:
        mostrar_registro_factores(analytics)

def mostrar_importar_excel(analytics):
    """Componente para importar desde Excel"""
    st.subheader("Importar Datos desde Excel")
    
    archivo_excel = st.file_uploader(
        "Selecciona archivo Excel", 
        type=['xlsx', 'xls'],
        help="El archivo debe contener hojas llamadas 'Estudiantes', 'Calificaciones', 'Factores'"
    )
    
    if archivo_excel:
        try:
            df_estudiantes_excel = pd.read_excel(archivo_excel, sheet_name='Estudiantes')
            df_calificaciones_excel = pd.read_excel(archivo_excel, sheet_name='Calificaciones')
            df_factores_excel = pd.read_excel(archivo_excel, sheet_name='Factores')
            
            st.success("✅ Archivo Excel leído correctamente")
            
            st.subheader("Vista Previa de Datos Importados")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Estudiantes:**", len(df_estudiantes_excel))
                st.dataframe(df_estudiantes_excel.head(3))
            
            with col2:
                st.write("**Calificaciones:**", len(df_calificaciones_excel))
                st.dataframe(df_calificaciones_excel.head(3))
            
            with col3:
                st.write("**Factores:**", len(df_factores_excel))
                st.dataframe(df_factores_excel.head(3))
            
            if st.button("💾 Guardar Datos en Base de Datos"):
                guardar_datos_excel(analytics, df_estudiantes_excel, df_calificaciones_excel, df_factores_excel)
                
        except Exception as e:
            st.error(f"Error al leer el archivo Excel: {e}")

def mostrar_registro_estudiante(analytics):
    """Componente para registro manual de estudiantes"""
    st.subheader("Registrar Nuevo Estudiante")
    
    with st.form("form_estudiante"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre completo*", placeholder="Juan García López")
            carrera_id = st.selectbox(
                "Carrera*", 
                options=list(CARRERAS.keys()),
                format_func=lambda x: f"{CARRERAS[x]} (ID: {x})"
            )
            ingreso_semestre = st.selectbox("Semestre de ingreso*", SEMESTRES_INGRESO)
        
        with col2:
            horas_estudio = st.number_input("Horas de estudio semanales*", min_value=0, max_value=80, value=20)
            desercion = st.checkbox("Estudiante en riesgo de deserción")
        
        submitted = st.form_submit_button("💾 Registrar Estudiante")
        
        if submitted:
            if not nombre:
                st.error("❌ El nombre es obligatorio")
            else:
                data = {
                    'nombre': nombre,
                    'carrera_id': int(carrera_id), 
                    'ingreso_semestre': ingreso_semestre,
                    'horas_estudio': int(horas_estudio),  
                    'desercion': bool(desercion)  
                }
                
                resultado = analytics.db.insertar_estudiante(data)
                if resultado:
                    st.success(f"✅ Estudiante '{nombre}' registrado correctamente con ID: {resultado['id']}")
                    st.info(f"📚 Carrera asignada: {CARRERAS[carrera_id]}")
                    analytics.cargar_datos()
                    st.rerun()
                else:
                    st.error("❌ Error al registrar el estudiante")

def mostrar_registro_materias(analytics):
    """Componente para registro de materias"""
    st.subheader("📚 Registrar Nueva Materia")
    
    with st.form("form_materia"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_materia = st.text_input("Nombre de la materia*", placeholder="Programación Orientada a Objetos")
            semestre = st.number_input("Semestre*", min_value=1, max_value=12, value=1)
        
        with col2:
            carrera_id = st.selectbox(
                "Carrera*", 
                options=list(CARRERAS.keys()),
                format_func=lambda x: f"{CARRERAS[x]}",
                key="carrera_materia"
            )
            docente = st.text_input("Docente*", placeholder="Dr. Juan Pérez")
        
        submitted = st.form_submit_button("📚 Registrar Materia")
        
        if submitted:
            if not nombre_materia or not docente:
                st.error("❌ Nombre de la materia y docente son obligatorios")
            else:
                data = {
                    'nombre': nombre_materia,
                    'semestre': int(semestre),  
                    'carrera_id': int(carrera_id),  
                    'docente': docente
                }
                
                resultado = analytics.db.insertar_materia(data)
                if resultado:
                    st.success(f"✅ Materia '{nombre_materia}' registrada correctamente con ID: {resultado['id']}")
                    st.info(f"📖 Semestre: {semestre}, Carrera: {CARRERAS[carrera_id]}, Docente: {docente}")
                    analytics.cargar_datos()
                    st.rerun()
                else:
                    st.error("❌ Error al registrar la materia")

def mostrar_registro_calificaciones(analytics):
    """Componente para registro de calificaciones"""
    st.subheader("📊 Registrar Calificaciones por Materia")
    

    if analytics.df_estudiantes.empty:
        st.warning("⚠️ No hay estudiantes registrados. Primero registra al menos un estudiante.")
        return
    

    if analytics.df_materias.empty:
        st.warning("⚠️ No hay materias registradas. Primero registra al menos una materia.")
        return
    
 
    st.markdown("### 🔍 Filtrar Estudiantes")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        carrera_filtro = st.selectbox(
            "Filtrar por carrera:",
            options=["Todas"] + [CARRERAS[cid] for cid in CARRERAS.keys()],
            index=0
        )
    with col_f2:
        semestre_filtro = st.selectbox(
            "Filtrar por semestre:",
            options=["Todos"] + sorted(analytics.df_estudiantes["ingreso_semestre"].dropna().unique().tolist()),
            index=0
        )
    

    df_filtrado = analytics.df_estudiantes.copy()
    if carrera_filtro != "Todas":
        carrera_id = [k for k, v in CARRERAS.items() if v == carrera_filtro][0]
        df_filtrado = df_filtrado[df_filtrado["carrera_id"] == carrera_id]
    if semestre_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["ingreso_semestre"] == semestre_filtro]
    
    if df_filtrado.empty:
        st.warning("⚠️ No se encontraron estudiantes con esos filtros.")
        return
    
    with st.form("form_calificaciones"):
        col1, col2 = st.columns(2)
        
        with col1:

            estudiantes_options = {}
            for est in df_filtrado.to_dict('records'):
                carrera_nombre = CARRERAS.get(est.get('carrera_id', 1), 'Carrera no especificada')
                estudiantes_options[est['id']] = f"{est['nombre']} - {carrera_nombre} (Sem: {est.get('ingreso_semestre', '-')})"
            
            estudiante_id = st.selectbox(
                "Estudiante*",
                options=list(estudiantes_options.keys()),
                format_func=lambda x: f"ID {x}: {estudiantes_options[x]}"
            )
            
            periodo = st.selectbox("Periodo*", ["2025-1", "2024-2", "2024-1", "2023-2", "2023-1"])
        
        with col2:

            materias_options = {}
            for mat in analytics.df_materias.to_dict('records'):
                carrera_nombre = CARRERAS.get(mat.get('carrera_id', 1), 'Carrera no especificada')
                materias_options[mat['id']] = f"{mat['nombre']} - {carrera_nombre}"
            
            materia_id = st.selectbox(
                "Materia*",
                options=list(materias_options.keys()),
                format_func=lambda x: f"ID {x}: {materias_options[x]}"
            )
            
            grupo = st.text_input("Grupo*", placeholder="A", max_chars=5)
        
        st.subheader("Calificaciones por Unidad")
        col3, col4, col5, col6 = st.columns(4)
        
        with col3:
            u1 = st.number_input("Unidad 1", min_value=0.0, max_value=100.0, value=80.0, step=0.1)
        with col4:
            u2 = st.number_input("Unidad 2", min_value=0.0, max_value=100.0, value=80.0, step=0.1)
        with col5:
            u3 = st.number_input("Unidad 3", min_value=0.0, max_value=100.0, value=80.0, step=0.1)
        with col6:
            asistencia = st.number_input("Asistencia (%)", min_value=0.0, max_value=100.0, value=90.0, step=0.1)
        
        submitted = st.form_submit_button("📊 Registrar Calificaciones")
        
        if submitted:
            try:
                if not grupo:
                    st.error("❌ El grupo es obligatorio")
                    return
                
                if not materia_id:
                    st.error("❌ Debes seleccionar una materia")
                    return
                
                calificacion_final = (u1 + u2 + u3) / 3
                
                calificacion_data = {
                    'estudiante_id': int(estudiante_id),
                    'materia_id': int(materia_id),
                    'periodo': periodo,
                    'calificacion_final': float(round(calificacion_final, 2)),
                    'asistencia': float(asistencia),
                    'u1': float(u1),
                    'u2': float(u2),
                    'u3': float(u3),
                    'grupo': grupo.upper()
                }
                
                resultado = analytics.db.insertar_calificacion(calificacion_data)
                if resultado:
                    st.success(f"✅ Calificaciones registradas correctamente con ID: {resultado['id']}")
                    st.info(f"📊 Calificación final: {calificacion_final:.1f} - {'Aprobado' if calificacion_final >= 70 else 'Reprobado'}")
                    analytics.cargar_datos()
                    st.rerun()
                else:
                    st.error("❌ Error al registrar las calificaciones")
                    
            except Exception as e:
                st.error(f"❌ Error al procesar las calificaciones: {str(e)}")

def mostrar_registro_factores(analytics):
    """Componente para registro de factores de riesgo - VERSIÓN CORREGIDA"""
    st.subheader("Registrar Factores de Riesgo")
    

    if analytics.df_estudiantes.empty:
        st.warning("⚠️ No hay estudiantes registrados. Primero registra al menos un estudiante.")
        return
    

    estudiantes_options = {}
    for est in analytics.df_estudiantes.to_dict('records'):
        carrera_nombre = CARRERAS.get(est.get('carrera_id', 1), 'Carrera no especificada')
        estudiantes_options[est['id']] = f"{est['nombre']} - {carrera_nombre}"
    
    with st.form("form_factor"):
        col1, col2 = st.columns(2)
        
        with col1:
            categoria = st.selectbox("Categoría del factor*", CATEGORIAS_FACTORES)
            estudiante_id = st.selectbox(
                "Estudiante*",
                options=list(estudiantes_options.keys()),
                format_func=lambda x: f"ID {x}: {estudiantes_options[x]}"
            )
        
        with col2:
            nombre_factor = st.text_input("Descripción del factor*", placeholder="Problemas económicos familiares")
            gravedad = st.slider("Nivel de gravedad*", 1, 5, 3)
            descripcion_gravedad = {
                1: "Muy bajo", 2: "Bajo", 3: "Medio", 4: "Alto", 5: "Muy alto"
            }[gravedad]
            st.write(f"**Nivel:** {descripcion_gravedad}")
        
        submitted = st.form_submit_button("⚠️ Registrar Factor de Riesgo")
        
        if submitted:
            if not nombre_factor:
                st.error("❌ La descripción del factor es obligatoria")
            else:
                try:
                    
                    calificaciones_estudiante = analytics.df_calificaciones[
                        analytics.df_calificaciones['estudiante_id'] == estudiante_id
                    ]
                    
                    calificacion_id = None
                    if not calificaciones_estudiante.empty:
                       
                        calificacion_id = int(calificaciones_estudiante.iloc[0]['id'])
                    
                    
                    data = {
                        'categoria': str(categoria),
                        'nombre': str(nombre_factor),
                        'inscripcion_id': calificacion_id,  
                        'gravedad': int(gravedad)  
                    }
                    
                    resultado = analytics.db.insertar_factor(data)
                    if resultado:
                        st.success("✅ Factor de riesgo registrado correctamente")
                        analytics.cargar_datos()
                        st.rerun()
                    else:
                        st.error("❌ Error al registrar el factor de riesgo")
                        
                except Exception as e:
                    st.error(f"❌ Error al procesar el factor de riesgo: {str(e)}")
                    st.info("💡 Si el problema persiste, intenta registrar primero una calificación para el estudiante.")

def guardar_datos_excel(analytics, df_estudiantes, df_calificaciones, df_factores):
    """Guardar datos de Excel en la base de datos"""
    try:
        # Insertar estudiantes
        for _, estudiante in df_estudiantes.iterrows():
            data = {
                'nombre': estudiante.get('nombre', ''),
                'carrera_id': int(estudiante.get('carrera_id', 1)),
                'ingreso_semestre': estudiante.get('ingreso_semestre', ''),
                'horas_estudio': int(estudiante.get('horas_estudio', 0)),
                'desercion': bool(estudiante.get('desercion', False))
            }
            analytics.db.insertar_estudiante(data)
        
        st.success("✅ Datos guardados correctamente en la base de datos")
        analytics.cargar_datos()
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error al guardar en la base de datos: {e}")