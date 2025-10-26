import streamlit as st
import pandas as pd
from conexion import (
    obtener_carreras, agregar_carrera,
    obtener_materias, agregar_materia,
    obtener_grupos, agregar_grupo
)

# ================================================================
# 🎓 VISTA DE CATÁLOGOS
# ================================================================
def vista_catalogos():
    st.title("📚 Administración de Catálogos")
    tabs = st.tabs(["🎓 Carreras", "📘 Materias", "👩‍🏫 Grupos"])

    # ================================================================
    # 🎓 TAB 1 - CARRERAS
    # ================================================================
    with tabs[0]:
        st.subheader("Gestión de Carreras")

        nombre_carrera = st.text_input("Nombre de la carrera:")
        if st.button("Agregar Carrera"):
            if nombre_carrera.strip() == "":
                st.warning("⚠️ Ingresa un nombre válido para la carrera.")
            else:
                agregar_carrera(nombre_carrera)
                st.success("✅ Carrera agregada correctamente.")

        st.divider()
        st.subheader("Listado de Carreras")
        carreras = obtener_carreras()
        if not carreras.empty:
            st.dataframe(carreras, use_container_width=True)
        else:
            st.info("No hay carreras registradas aún.")

    # ================================================================
    # 📘 TAB 2 - MATERIAS
    # ================================================================
    with tabs[1]:
        st.subheader("Gestión de Materias")

        nombre_materia = st.text_input("Nombre de la materia:")
        semestre = st.number_input("Semestre (1-12):", min_value=1, max_value=12, value=1)

        if st.button("Agregar Materia"):
            if nombre_materia.strip() == "":
                st.warning("⚠️ Ingresa un nombre válido para la materia.")
            else:
                agregar_materia(nombre_materia, semestre)
                st.success("✅ Materia agregada correctamente.")

        st.divider()
        st.subheader("Listado de Materias")
        materias = obtener_materias()
        if not materias.empty:
            st.dataframe(materias, use_container_width=True)
        else:
            st.info("No hay materias registradas aún.")

    # ================================================================
    # 👩‍🏫 TAB 3 - GRUPOS
    # ================================================================
    with tabs[2]:
        st.subheader("Gestión de Grupos")

        materias = obtener_materias()
        if materias.empty:
            st.warning("⚠️ Debes registrar materias primero.")
        else:
            materia_nombres = materias["nombre"].tolist()
            seleccion = st.selectbox("Selecciona la materia:", materia_nombres)

            materia_id = int(materias[materias["nombre"] == seleccion]["id"].values[0])
            periodo = st.text_input("Periodo (ej. 2025-1):", "2025-1")
            grupo = st.text_input("Clave del grupo:", "A")
            docente = st.text_input("Nombre del docente:")

            if st.button("Agregar Grupo"):
                try:
                    agregar_grupo(materia_id, periodo, grupo, docente)
                    st.success("✅ Grupo agregado con éxito.")
                except Exception as e:
                    st.error(f"⚠️ Error al agregar grupo: {e}")

        st.divider()
        st.subheader("Listado de Grupos")
        grupos = obtener_grupos()
        if not grupos.empty:
            st.dataframe(grupos, use_container_width=True)
        else:
            st.info("No hay grupos registrados aún.")
