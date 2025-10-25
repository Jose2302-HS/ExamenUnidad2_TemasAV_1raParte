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

# ---------- CARRERAS ----------
def obtener_carreras():
    try:
        data = supabase.table("carreras").select("*").order("nombre").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        print("Error al obtener carreras:", e)
        return pd.DataFrame()

def agregar_carrera(nombre):
    try:
        supabase.table("carreras").insert({"nombre": nombre}).execute()
    except Exception as e:
        print("Error al agregar carrera:", e)


# ---------- MATERIAS ----------
def obtener_materias():
    try:
        data = supabase.table("materias").select("*").order("nombre").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        print("Error al obtener materias:", e)
        return pd.DataFrame()

def agregar_materia(nombre, semestre):
    try:
        supabase.table("materias").insert({
            "nombre": nombre,
            "semestre": semestre
        }).execute()
    except Exception as e:
        print("Error al agregar materia:", e)


# ---------- GRUPOS ----------
def obtener_grupos():
    try:
        data = supabase.table("grupos").select("*, materias(nombre)").order("id").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        print("Error al obtener grupos:", e)
        return pd.DataFrame()

def agregar_grupo(materia_id, periodo, grupo, docente):
    try:
        supabase.table("grupos").insert({
            "materia_id": materia_id,
            "periodo": periodo,
            "grupo": grupo,
            "docente": docente
        }).execute()
    except Exception as e:
        print("Error al agregar grupo:", e)


# ---------- INSCRIPCIONES ----------
def obtener_inscripciones():
    try:
        data = supabase.table("inscripciones").select("*").execute()
        return pd.DataFrame(data.data)
    except Exception as e:
        print("Error al obtener inscripciones:", e)
        return pd.DataFrame()

def agregar_inscripcion(estudiante_id, grupo_id, asistencia_pct=0, u1=0, u2=0, u3=0):
    try:
        calif_final = round((u1 + u2 + u3) / 3.0, 2)
        supabase.table("inscripciones").insert({
            "estudiante_id": int(estudiante_id),
            "grupo_id": int(grupo_id),
            "asistencia_pct":float( asistencia_pct),
            "u1": float(u1), "u2": float(u2), "u3": float(u3),
            "calif_final":float (calif_final),
            "reprobado": calif_final < 70
        }).execute()
    except Exception as e:
        print("Error al agregar inscripción:", e)