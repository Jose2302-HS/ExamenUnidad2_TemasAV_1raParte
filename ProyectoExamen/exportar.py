import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import io

# ===========================
# Exportar datos a Excel
# ===========================
def exportar_excel(df_estudiantes, df_asistencias, df_factores, ruta="reporte_calidad.xlsx"):
    """Exporta todas las tablas a un archivo Excel."""
    with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
        df_estudiantes.to_excel(writer, index=False, sheet_name="Estudiantes")
        df_asistencias.to_excel(writer, index=False, sheet_name="Asistencias")
        df_factores.to_excel(writer, index=False, sheet_name="Factores")
    return ruta


# ===========================
# Exportar reporte a PDF
# ===========================
def exportar_pdf(df_estudiantes, df_asistencias, df_factores, ruta="reporte_calidad.pdf"):
    """Genera un reporte PDF con datos resumidos y gráficas."""
    doc = SimpleDocTemplate(ruta, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph("📄 Reporte de Calidad Académica - TecNM Tijuana", styles["Title"]))
    story.append(Spacer(1, 12))

    # --- Resumen de estudiantes ---
    story.append(Paragraph("<b>Resumen General de Estudiantes</b>", styles["Heading2"]))
    total_estudiantes = len(df_estudiantes)
    promedio_general = df_estudiantes[["unidad1", "unidad2", "unidad3"]].mean(axis=1).mean()
    story.append(Paragraph(f"Total de estudiantes: {total_estudiantes}", styles["Normal"]))
    story.append(Paragraph(f"Promedio general: {promedio_general:.2f}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # --- Gráfico promedio por estudiante ---
    fig, ax = plt.subplots(figsize=(5, 3))
    df_estudiantes["promedio"] = df_estudiantes[["unidad1", "unidad2", "unidad3"]].mean(axis=1)
    ax.bar(df_estudiantes["nombre"], df_estudiantes["promedio"], color="cornflowerblue")
    ax.set_title("Promedio por Estudiante", fontsize=10)
    plt.xticks(rotation=30, fontsize=7)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png", bbox_inches="tight")
    plt.close(fig)
    img_buf.seek(0)
    story.append(Image(img_buf, width=400, height=240))
    story.append(Spacer(1, 12))

    # --- Factores de reprobación ---
    story.append(Paragraph("<b>Factores de Reprobación</b>", styles["Heading2"]))
    conteo = df_factores["tipo_factor"].value_counts() if not df_factores.empty else {}
    if len(conteo) > 0:
        for factor, cantidad in conteo.items():
            story.append(Paragraph(f"{factor}: {cantidad} casos", styles["Normal"]))
    else:
        story.append(Paragraph("No hay factores registrados.", styles["Normal"]))

    story.append(Spacer(1, 20))
    story.append(Paragraph("Reporte generado automáticamente por el Sistema de Gestión Académica.", styles["Italic"]))

    doc.build(story)
    return ruta


from conexion import supabase

def exportar_pdf_avanzado(ruta="reporte_academico.pdf"):
    """Genera un reporte más completo con información de inscripciones."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO

    try:
        datos = supabase.table("inscripciones").select("calif_final, reprobado, grupos(materias(nombre))").execute()
        df = pd.json_normalize(datos.data)
        if df.empty:
            st.warning("No hay datos en inscripciones para generar el reporte.")
            return None

        promedio = df.groupby("grupos.materias.nombre")["calif_final"].mean()
        reprob = df.groupby("grupos.materias.nombre")["reprobado"].mean() * 100

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(180, 760, "Reporte Académico General - TecNM Tijuana")

        y = 720
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Promedios por materia:")
        y -= 20
        c.setFont("Helvetica", 10)
        for materia, valor in promedio.items():
            c.drawString(70, y, f"- {materia}: {valor:.2f}")
            y -= 15

        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Porcentaje de reprobación:")
        y -= 20
        c.setFont("Helvetica", 10)
        for materia, valor in reprob.items():
            c.drawString(70, y, f"- {materia}: {valor:.1f}%")
            y -= 15

        c.save()
        buffer.seek(0)
        st.download_button(
            label="📄 Descargar PDF Avanzado",
            data=buffer,
            file_name=ruta,
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error al generar reporte avanzado: {e}")
