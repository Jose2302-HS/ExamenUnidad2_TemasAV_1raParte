import streamlit as st
import pandas as pd
from conexion import (
    obtener_estudiantes,  # ya lo tienes en tu código actual
    obtener_grupos,
    agregar_inscripcion,
    obtener_inscripciones
)

def vista_inscripciones():
    st.header("Inscripciones y Calificaciones ✏️")

    # --- Registrar nueva inscripción ---
    st.subheader("Registrar nueva inscripción")
    estudiantes = obtener_estudiantes()
    grupos = obtener_grupos()

    if estudiantes.empty or grupos.empty:
        st.warning("⚠️ Asegúrate de tener estudiantes y grupos registrados.")
        return

    est_sel = st.selectbox("Estudiante:", estudiantes["nombre"].tolist())
    est_id = estudiantes.loc[estudiantes["nombre"] == est_sel, "id"].values[0]

    grp_sel = st.selectbox("Grupo:", grupos["grupo"].tolist())
    grp_id = grupos.loc[grupos["grupo"] == grp_sel, "id"].values[0]

    asistencia = st.slider("Asistencia (%)", 0, 100, 90)
    u1 = st.number_input("Unidad 1:", 0, 100, 80)
    u2 = st.number_input("Unidad 2:", 0, 100, 85)
    u3 = st.number_input("Unidad 3:", 0, 100, 90)

    if st.button("Registrar inscripción"):
        agregar_inscripcion(est_id, grp_id, asistencia, u1, u2, u3)
        st.success("✅ Inscripción registrada correctamente.")

    # --- Listado de inscripciones ---
    st.divider()
    st.subheader("Listado de inscripciones")
    insc = obtener_inscripciones()
    if not insc.empty:
        st.dataframe(insc)
    else:
        st.info("No hay inscripciones registradas.")
