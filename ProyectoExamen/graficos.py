import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ======================================
# GRÁFICO DE PARETO
# ======================================
def grafico_pareto(df_estudiantes):
    st.subheader("📊 Gráfico de Pareto - Calificaciones Promedio")
    df_estudiantes["promedio"] = df_estudiantes[["unidad1", "unidad2", "unidad3"]].mean(axis=1)
    df_ordenado = df_estudiantes.sort_values(by="promedio", ascending=False)

    fig, ax = plt.subplots(figsize=(5,3))
    ax.bar(df_ordenado["nombre"], df_ordenado["promedio"], color="skyblue")
    ax.set_title("Gráfico de Pareto", fontsize=10)
    ax.set_xlabel("Estudiantes", fontsize=8)
    ax.set_ylabel("Promedio", fontsize=8)
    plt.xticks(rotation=30, fontsize=7)
    plt.yticks(fontsize=7)
    st.pyplot(fig, use_container_width=False)

# ======================================
# GRÁFICO DE DISPERSIÓN
# ======================================
def grafico_dispersion(df_estudiantes):
    st.subheader("📈 Diagrama de Dispersión - Unidad 1 vs Unidad 2")
    fig, ax = plt.subplots(figsize=(5,3))
    ax.scatter(df_estudiantes["unidad1"], df_estudiantes["unidad2"], color="lightcoral")
    ax.set_title("Dispersión U1 vs U2", fontsize=10)
    ax.set_xlabel("Unidad 1", fontsize=8)
    ax.set_ylabel("Unidad 2", fontsize=8)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    st.pyplot(fig, use_container_width=False)

# ======================================
# HISTOGRAMA DE CALIFICACIONES
# ======================================
def grafico_histograma(df_estudiantes):
    st.subheader("📊 Histograma - Distribución de Calificaciones")
    df_estudiantes["promedio"] = df_estudiantes[["unidad1", "unidad2", "unidad3"]].mean(axis=1)

    fig, ax = plt.subplots(figsize=(5,3))
    ax.hist(df_estudiantes["promedio"], bins=5, color="mediumseagreen", edgecolor="black")
    ax.set_title("Distribución de Promedios", fontsize=10)
    ax.set_xlabel("Promedio", fontsize=8)
    ax.set_ylabel("Frecuencia", fontsize=8)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    st.pyplot(fig, use_container_width=False)

# ======================================
# DIAGRAMA DE CONTROL
# ======================================
def grafico_control(df_estudiantes):
    st.subheader("📉 Diagrama de Control - Calificaciones Promedio")
    df_estudiantes["promedio"] = df_estudiantes[["unidad1", "unidad2", "unidad3"]].mean(axis=1)

    promedio_general = df_estudiantes["promedio"].mean()
    limite_superior = promedio_general + 10
    limite_inferior = promedio_general - 10

    fig, ax = plt.subplots(figsize=(5,3))
    ax.plot(df_estudiantes["id"], df_estudiantes["promedio"], marker="o", linestyle="-", color="royalblue")
    ax.axhline(promedio_general, color="green", linestyle="--", label="Promedio")
    ax.axhline(limite_superior, color="red", linestyle="--", label="Límite Sup.")
    ax.axhline(limite_inferior, color="red", linestyle="--", label="Límite Inf.")
    ax.set_title("Gráfico de Control", fontsize=10)
    ax.set_xlabel("ID", fontsize=8)
    ax.set_ylabel("Promedio", fontsize=8)
    ax.legend(fontsize=6)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    st.pyplot(fig, use_container_width=False)

# ======================================
# DIAGRAMA ISHIKAWA (CAUSA-EFECTO)
# ======================================
def grafico_ishikawa(df_factores):
    st.subheader("🧩 Diagrama de Ishikawa - Causas de Reprobación")

    if df_factores.empty:
        st.warning("No hay factores registrados aún para generar el diagrama.")
        return

    causas = df_factores["tipo_factor"].value_counts()
    fig, ax = plt.subplots(figsize=(5,3))
    ax.barh(causas.index, causas.values, color="orange")
    ax.set_title("Principales Causas", fontsize=10)
    ax.set_xlabel("Frecuencia", fontsize=8)
    ax.set_ylabel("Causa", fontsize=8)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    st.pyplot(fig, use_container_width=False)


# ======================================
# NUEVOS GRÁFICOS BASADOS EN INSCRIPCIONES
# ======================================
from conexion import supabase  # usa la conexión ya existente

def grafico_promedio_materias():
    """Gráfico de promedio final por materia a partir de inscripciones."""
    st.subheader("📚 Promedio de Calificaciones por Materia")

    try:
        datos = supabase.table("inscripciones").select("calif_final, grupos(materias(nombre))").execute()
        df = pd.json_normalize(datos.data)
        if df.empty:
            st.warning("No hay datos de inscripciones para mostrar.")
            return

        df = df.groupby("grupos.materias.nombre")["calif_final"].mean().reset_index()

        fig, ax = plt.subplots(figsize=(5,3))
        ax.bar(df["grupos.materias.nombre"], df["calif_final"], color="orchid")
        ax.set_xlabel("Materia", fontsize=8)
        ax.set_ylabel("Promedio", fontsize=8)
        ax.set_title("Promedio Final por Materia", fontsize=10)
        plt.xticks(rotation=25, fontsize=7)
        plt.yticks(fontsize=7)
        st.pyplot(fig, use_container_width=False)
    except Exception as e:
        st.error(f"Error al generar gráfico: {e}")


def grafico_reprobacion_materias():
    """Gráfico del porcentaje de reprobación por materia."""
    st.subheader("📉 Porcentaje de Reprobación por Materia")

    try:
        datos = supabase.table("inscripciones").select("reprobado, grupos(materias(nombre))").execute()
        df = pd.json_normalize(datos.data)
        if df.empty:
            st.warning("No hay inscripciones registradas.")
            return

        df["reprobado"] = df["reprobado"].astype(int)
        resumen = df.groupby("grupos.materias.nombre")["reprobado"].mean().reset_index()
        resumen["% Reprobación"] = resumen["reprobado"] * 100

        fig, ax = plt.subplots(figsize=(5,3))
        ax.bar(resumen["grupos.materias.nombre"], resumen["% Reprobación"], color="tomato")
        ax.set_xlabel("Materia", fontsize=8)
        ax.set_ylabel("% Reprobación", fontsize=8)
        ax.set_title("Tasa de Reprobación", fontsize=10)
        plt.xticks(rotation=25, fontsize=7)
        plt.yticks(fontsize=7)
        st.pyplot(fig, use_container_width=False)
    except Exception as e:
        st.error(f"Error al generar gráfico: {e}")

