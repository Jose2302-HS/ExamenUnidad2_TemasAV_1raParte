import streamlit as st
import pandas as pd
from datetime import date
# Importamos los módulos
from conexion import obtener_estudiantes, agregar_estudiante
from graficos import grafico_pareto, grafico_dispersion
from asistencia import registrar_asistencia, obtener_asistencias

# Configuración del dashboard
st.set_page_config(page_title="Sistema de Gestión Académica", layout="wide")

st.title("🎓 Sistema de Gestión Académica - TecNM Tijuana")

# --- Barra de navegación (pestañas superiores) ---
tabs = st.tabs(["📋 Registro de Estudiantes", "🗓️ Asistencia", "⚠️ Factores de Reprobación", "📈 Gráficas", "📄 Reportes"])

# =====================================================================
# 📋 TAB 1 - REGISTRO DE ESTUDIANTES
# =====================================================================
with tabs[0]:
    st.subheader("Registro de Estudiantes")

    col1, col2, col3 = st.columns(3)
    with col1:
        nombre = st.text_input("Nombre")
        carrera = st.selectbox("Carrera", ["Informática", "Industrial", "Electrónica"])
    with col2:
        semestre = st.number_input("Semestre", 1, 12)
        cal1 = st.number_input("Calificación Unidad 1", 0, 100)
    with col3:
        cal2 = st.number_input("Calificación Unidad 2", 0, 100)
        cal3 = st.number_input("Calificación Unidad 3", 0, 100)

    if st.button("Guardar Estudiante"):
        agregar_estudiante(nombre, carrera, semestre, cal1, cal2, cal3)
        st.success("✅ Estudiante guardado correctamente en Supabase.")

    st.divider()
    st.subheader("📋 Estudiantes Registrados")
    df = obtener_estudiantes()
    st.dataframe(df, use_container_width=True)

# =====================================================================
# 🗓️ TAB 2 - ASISTENCIA
# =====================================================================
with tabs[1]:
    st.subheader("Registro de Asistencia")

    id_estudiante = st.number_input("ID del estudiante", min_value=1, key="asistencia_id")
    fecha_asistencia = st.date_input("Fecha", value=date.today())
    asistio = st.radio("¿Asistió?", ["Sí", "No"], horizontal=True)

    if st.button("Registrar Asistencia"):
        asistio_bool = True if asistio == "Sí" else False
        registrar_asistencia(id_estudiante, fecha_asistencia, asistio_bool)
        st.success("✅ Asistencia registrada correctamente en Supabase.")

    st.divider()
    st.subheader("📋 Asistencias registradas")
    df_asistencias = obtener_asistencias()
    if not df_asistencias.empty:
        st.dataframe(df_asistencias, use_container_width=True)

        total = len(df_asistencias)
        presentes = df_asistencias[df_asistencias["asistio"] == True]
        porcentaje = (len(presentes) / total) * 100 if total > 0 else 0
        st.info(f"📊 Porcentaje general de asistencia: {porcentaje:.2f}%")
    else:
        st.warning("No hay registros de asistencia aún.")

# =====================================================================
# ⚠️ TAB 3 - FACTORES DE REPROBACIÓN
# =====================================================================
from factores import registrar_factor, obtener_factores

with tabs[2]:
    st.subheader("Registro de Factores de Reprobación")

    id_estudiante_factor = st.number_input("ID del estudiante", min_value=1, key="factor_id")
    tipo_factor = st.text_input("Tipo de factor (ejemplo: Falta de estudio, Problemas personales, etc.)")
    impacto = st.selectbox("Impacto del factor", ["Bajo", "Medio", "Alto"])

    if st.button("Registrar Factor"):
        if tipo_factor.strip() == "":
            st.error("⚠️ Debes ingresar un tipo de factor.")
        else:
            registrar_factor(id_estudiante_factor, tipo_factor, impacto)
            st.success("✅ Factor de reprobación registrado correctamente en Supabase.")

    st.divider()
    st.subheader("📋 Factores registrados")
    df_factores = obtener_factores()

    if not df_factores.empty:
        st.dataframe(df_factores, use_container_width=True)
        conteo = df_factores["impacto"].value_counts()
        st.info(f"📊 Resumen de impacto:\n{conteo.to_string()}")
    else:
        st.warning("No hay factores registrados aún.")

# =====================================================================
# 📈 TAB 4 - GRÁFICAS
# =====================================================================
from factores import obtener_factores
from graficos import (
    grafico_pareto,
    grafico_dispersion,
    grafico_histograma,
    grafico_control,
    grafico_ishikawa
)

with tabs[3]:
    st.subheader("📊 Panel de Análisis Académico y de Calidad")

    df = obtener_estudiantes()
    df_factores = obtener_factores()

    if df.empty:
        st.warning("No hay estudiantes registrados aún.")
    else:
        # ----- Fila 1 -----
        col1, col2 = st.columns(2)
        with col1:
            grafico_pareto(df)
        with col2:
            grafico_dispersion(df)

        st.divider()

        # ----- Fila 2 -----
        col3, col4 = st.columns(2)
        with col3:
            grafico_histograma(df)
        with col4:
            grafico_control(df)

        st.divider()


# =====================================================================
# 📄 TAB 5 - REPORTES
# =====================================================================
from asistencia import obtener_asistencias
from factores import obtener_factores
from exportar import exportar_excel, exportar_pdf

with tabs[4]:
    st.subheader("📄 Generación y Exportación de Reportes")

    df_estudiantes = obtener_estudiantes()
    df_asistencias = obtener_asistencias()
    df_factores = obtener_factores()

    if df_estudiantes.empty:
        st.warning("No hay datos suficientes para generar reportes.")
    else:
        formato = st.radio("Selecciona formato de exportación:", ["Excel (.xlsx)", "PDF (.pdf)"], horizontal=True)

        if st.button("📤 Exportar Reporte"):
            if formato == "Excel (.xlsx)":
                ruta = exportar_excel(df_estudiantes, df_asistencias, df_factores)
                with open(ruta, "rb") as file:
                    st.download_button(
                        label="⬇️ Descargar archivo Excel",
                        data=file,
                        file_name="reporte_calidad.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
            else:
                ruta = exportar_pdf(df_estudiantes, df_asistencias, df_factores)
                with open(ruta, "rb") as file:
                    st.download_button(
                        label="⬇️ Descargar archivo PDF",
                        data=file,
                        file_name="reporte_calidad.pdf",
                        mime="application/pdf",
                    )
