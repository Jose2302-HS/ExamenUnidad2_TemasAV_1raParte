from supabase import create_client, Client
import pandas as pd
from datetime import date

# Conexión (usa los mismos valores que en conexion_supabase.py)
URL = "https://jqwyocwoaguhcnzuotww.supabase.co"   # 🔹 cambia por tu URL
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impxd3lvY3dvYWd1aGNuenVvdHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwODU1OTUsImV4cCI6MjA3NjY2MTU5NX0.nn-pipZpwmrB2x-7LBa1wT1htflRShXbDG0se_1GGIM"                        # 🔹 cambia por tu anon key
supabase: Client = create_client(URL, KEY)


def registrar_asistencia(id_estudiante, fecha, asistio=True):
    """Registra la asistencia de un estudiante en Supabase."""
    nuevo = {
        "id_estudiante": id_estudiante,
        "fecha": str(fecha),
        "asistio": asistio
    }
    try:
        supabase.table("asistencias").insert(nuevo).execute()
    except Exception as e:
        print("Error al registrar asistencia:", e)


def obtener_asistencias():
    """Obtiene todas las asistencias registradas."""
    try:
        response = supabase.table("asistencias").select("*").execute()
        data = response.data
        return pd.DataFrame(data)
    except Exception as e:
        print("Error al obtener asistencias:", e)
        return pd.DataFrame()


def obtener_asistencia_por_estudiante(id_estudiante):
    """Obtiene la asistencia específica de un estudiante."""
    try:
        response = supabase.table("asistencias").select("*").eq("id_estudiante", id_estudiante).execute()
        data = response.data
        return pd.DataFrame(data)
    except Exception as e:
        print("Error al obtener asistencia del estudiante:", e)
        return pd.DataFrame()
