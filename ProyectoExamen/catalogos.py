import streamlit as st
from conexion import (
    obtener_carreras, agregar_carrera,
    obtener_materias, agregar_materia,
    obtener_grupos, agregar_grupo
)

def vista_catalogos():
    st.header("Catálogos del Sistema 📚")
    tabs = st.tabs(["Carreras", "Materias", "Grupos"])

    # === CARRERAS ===
    with tabs[0]:
        st.subheader("Registrar nueva carrera")
        nombre = st.text_input("Nombre de la carrera:")
        if st.button("Agregar carrera"):
            if nombre.strip():
                agregar_carrera(nombre.strip())
                st.success("✅ Carrera agregada con éxito.")
            else:
                st.warning("⚠️ Ingresa un nombre válido.")
        st.divider()
        st.subheader("Listado de carreras")
        carreras = obtener_carreras()
        if not carreras.empty:
            st.dataframe(carreras)
        else:
            st.info("No hay carreras registradas.")

    # === MATERIAS ===
    with tabs[1]:
        st.subheader("Registrar nueva materia")
        nombre_m = st.text_input("Nombre de la materia:")
        semestre = st.number_input("Semestre:", 1, 12, 1)
        if st.button("Agregar materia"):
            if nombre_m.strip():
                agregar_materia(nombre_m.strip(), semestre)
                st.success("✅ Materia agregada con éxito.")
            else:
                st.warning("⚠️ Ingresa un nombre válido.")
        st.divider()
        st.subheader("Listado de materias")
        materias = obtener_materias()
        if not materias.empty:
            st.dataframe(materias)
        else:
            st.info("No hay materias registradas.")

    # === GRUPOS ===
    with tabs[2]:
        st.subheader("Registrar nuevo grupo")
        materias = obtener_materias()
        if not materias.empty:
            opciones_m = materias["nombre"].tolist()
            seleccion = st.selectbox("Materia:", opciones_m)
            materia_id =int(materias[materias["nombre"] == seleccion]["id"].values[0])
            periodo = st.text_input("Periodo (ej. 2025-1):", "2025-1")
            grupo = st.text_input("Clave del grupo:", "A")
            docente = st.text_input("Nombre del docente:")
            if st.button("Agregar grupo"):
                agregar_grupo(materia_id, periodo, grupo, docente)
                st.success("✅ Grupo agregado con éxito.")
        else:
            st.warning("⚠️ No hay materias registradas.")
        st.divider()
        st.subheader("Listado de grupos")
        grupos = obtener_grupos()
        if not grupos.empty:
            st.dataframe(grupos)
        else:
            st.info("No hay grupos registrados.")
