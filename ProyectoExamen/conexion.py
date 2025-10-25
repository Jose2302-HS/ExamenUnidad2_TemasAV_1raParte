from supabase import create_client, Client
import pandas as pd

# 🔧 Coloca tus datos reales de Supabase aquí
URL = "https://jqwyocwoaguhcnzuotww.supabase.co"  
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impxd3lvY3dvYWd1aGNuenVvdHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwODU1OTUsImV4cCI6MjA3NjY2MTU5NX0.nn-pipZpwmrB2x-7LBa1wT1htflRShXbDG0se_1GGIM"                      

supabase: Client = create_client(URL, KEY)

def obtener_estudiantes():
    """Consulta todos los registros de la tabla 'estudiantes' en Supabase"""
    try:
        response = supabase.table("estudiantes").select("*").execute()
        data = response.data
        return pd.DataFrame(data)
    except Exception as e:
        print("Error al obtener datos:", e)
        return pd.DataFrame()

def agregar_estudiante(nombre, carrera, semestre, cal1, cal2, cal3):
    """Inserta un nuevo estudiante en la tabla Supabase"""
    if not nombre:
        return
    nuevo = {
        "nombre": nombre,
        "carrera": carrera,
        "semestre": semestre,
        "unidad1": cal1,
        "unidad2": cal2,
        "unidad3": cal3
    }
    try:
        supabase.table("estudiantes").insert(nuevo).execute()
    except Exception as e:
        print("Error al insertar datos:", e)
