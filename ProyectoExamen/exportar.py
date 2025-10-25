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
