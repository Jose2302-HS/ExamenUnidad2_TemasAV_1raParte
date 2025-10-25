from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# Conexión a Supabase
URL = "https://jqwyocwoaguhcnzuotww.supabase.co"   # 🔹 cambia por tu URL
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impxd3lvY3dvYWd1aGNuenVvdHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwODU1OTUsImV4cCI6MjA3NjY2MTU5NX0.nn-pipZpwmrB2x-7LBa1wT1htflRShXbDG0se_1GGIM"  
supabase: Client = create_client(URL, KEY)


def registrar_factor(id_estudiante, tipo_factor, impacto):
    """Registra un nuevo factor de reprobación en Supabase."""
    nuevo = {
        "id_estudiante": id_estudiante,
        "tipo_factor": tipo_factor,
        "impacto": impacto,
        "fecha_registro": datetime.now().isoformat()
    }
    try:
        supabase.table("factores_reprobacion").insert(nuevo).execute()
    except Exception as e:
        print("Error al registrar factor:", e)


def obtener_factores():
    """Obtiene todos los factores registrados."""
    try:
        response = supabase.table("factores_reprobacion").select("*").execute()
        data = response.data
        return pd.DataFrame(data)
    except Exception as e:
        print("Error al obtener factores:", e)
        return pd.DataFrame()


def obtener_factores_por_estudiante(id_estudiante):
    """Obtiene los factores específicos de un estudiante."""
    try:
        response = supabase.table("factores_reprobacion").select("*").eq("id_estudiante", id_estudiante).execute()
        data = response.data
        return pd.DataFrame(data)
    except Exception as e:
        print("Error al obtener factores del estudiante:", e)
        return pd.DataFrame()
