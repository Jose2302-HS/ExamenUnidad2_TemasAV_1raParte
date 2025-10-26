import pandas as pd
from supabase import create_client, Client
import json

# ============================================
# 🔹 Conexión a Supabase
# ============================================
URL = "https://jqwyocwoaguhcnzuotww.supabase.co"  
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impxd3lvY3dvYWd1aGNuenVvdHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEwODU1OTUsImV4cCI6MjA3NjY2MTU5NX0.nn-pipZpwmrB2x-7LBa1wT1htflRShXbDG0se_1GGIM"  
supabase: Client = create_client(URL, KEY)

# ============================================
# 🔹 Funciones auxiliares
# ============================================
def limpiar_json(data):
    """Convierte los valores int64 o numpy a tipos nativos de Python."""
    return json.loads(json.dumps(data, default=str))

# ============================================
# 🧑 ESTUDIANTES
# ============================================
def obtener_estudiantes():
    res = supabase.table("estudiantes").select("*").execute()
    if res.data:
        return pd.DataFrame(res.data)
    return pd.DataFrame()

def agregar_estudiante(nombre, carrera, semestre, cal1, cal2, cal3):
    data = {
        "nombre": nombre,
        "carrera": carrera,
        "semestre": semestre,
        "unidad1": cal1,
        "unidad2": cal2,
        "unidad3": cal3
    }
    supabase.table("estudiantes").insert(limpiar_json(data)).execute()

# ============================================
# 🎓 CARRERAS
# ============================================
def obtener_carreras():
    res = supabase.table("carreras").select("*").execute()
    if res.data:
        return pd.DataFrame(res.data)
    return pd.DataFrame()

def agregar_carrera(nombre):
    supabase.table("carreras").insert(limpiar_json({"nombre": nombre})).execute()

# ============================================
# 📘 MATERIAS
# ============================================
def obtener_materias():
    res = supabase.table("materias").select("*").execute()
    if res.data:
        return pd.DataFrame(res.data)
    return pd.DataFrame()

def agregar_materia(nombre, semestre):
    data = {"nombre": nombre, "semestre": semestre}
    supabase.table("materias").insert(limpiar_json(data)).execute()

# ============================================
# 👩‍🏫 GRUPOS
# ============================================
def obtener_grupos():
    res = supabase.table("grupos").select("*").execute()
    if res.data:
        return pd.DataFrame(res.data)
    return pd.DataFrame()

def agregar_grupo(materia_id, periodo, grupo, docente):
    data = {
        "materia_id": int(materia_id),
        "periodo": periodo,
        "grupo": grupo,
        "docente": docente
    }
    supabase.table("grupos").insert(limpiar_json(data)).execute()

# ============================================
# 🧾 INSCRIPCIONES
# ============================================
def obtener_inscripciones():
    res = supabase.table("inscripciones").select("*").execute()
    if res.data:
        return pd.DataFrame(res.data)
    return pd.DataFrame()

def agregar_inscripcion(estudiante_id, grupo_id, u1, u2, u3, u4, u5, asistencia_pct, horas_estudio):
    data = {
        "estudiante_id": int(estudiante_id),
        "grupo_id": int(grupo_id),
        "u1": float(u1),
        "u2": float(u2),
        "u3": float(u3),
        "u4": float(u4),
        "u5": float(u5),
        "asistencia_pct": float(asistencia_pct),
        "horas_estudio": int(horas_estudio),
        "desertor": False
    }
    supabase.table("inscripciones").insert(limpiar_json(data)).execute()

# ============================================
# ⚠️ FACTORES
# ============================================
def obtener_factores():
    res = supabase.table("factores").select("*").execute()
    if res.data:
        return pd.DataFrame(res.data)
    return pd.DataFrame()

def agregar_factor(categoria, nombre):
    data = {"categoria": categoria, "nombre": nombre}
    supabase.table("factores").insert(limpiar_json(data)).execute()

# ============================================
# 📊 INSCRIPCIONES - FACTORES
# ============================================
def obtener_insc_factores():
    res = supabase.table("insc_factores").select("*").execute()
    if res.data:
        return pd.DataFrame(res.data)
    return pd.DataFrame()

def agregar_insc_factor(inscripcion_id, factor_id, gravedad):
    data = {
        "inscripcion_id": int(inscripcion_id),
        "factor_id": int(factor_id),
        "gravedad": int(gravedad)
    }
    supabase.table("insc_factores").insert(limpiar_json(data)).execute()
