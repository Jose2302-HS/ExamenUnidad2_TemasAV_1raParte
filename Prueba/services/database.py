import pandas as pd
from supabase import create_client
import streamlit as st

class DatabaseService:
    def __init__(self):
        self.supabase = self._inicializar_supabase()
    
    def _inicializar_supabase(self):
        """Inicializar conexión con Supabase"""
        try:
            supabase_url = st.secrets.get("SUPABASE_URL")
            supabase_key = st.secrets.get("SUPABASE_KEY")
            if supabase_url and supabase_key:
                return create_client(supabase_url, supabase_key)
            else:
                st.warning("🔶 Credenciales de Supabase no encontradas. La base de datos estará vacía.")
                return None
        except Exception as e:
            st.warning(f"🔶 Error conectando a Supabase: {e}. La base de datos estará vacía.")
            return None
    
    @st.cache_data(ttl=300)  
    def cargar_estudiantes(_self):
        """Cargar estudiantes desde Supabase CON CACHE"""
        try:
            if _self.supabase:
                response = _self.supabase.table('estudiantes').select('*').execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error cargando estudiantes: {e}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)  
    def cargar_calificaciones(_self):
        """Cargar registro_calificaciones desde Supabase CON CACHE"""
        try:
            if _self.supabase:
                response = _self.supabase.table('registro_calificaciones').select('*').execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error cargando calificaciones: {e}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)  
    def cargar_factores(_self):
        """Cargar factores desde Supabase CON CACHE"""
        try:
            if _self.supabase:
                response = _self.supabase.table('factores').select('*').execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error cargando factores: {e}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)  
    def cargar_materias(_self):
        """Cargar materias desde Supabase CON CACHE"""
        try:
            if _self.supabase:
                response = _self.supabase.table('materias').select('*').execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error cargando materias: {e}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300) 
    def cargar_grupos(_self):
        """Cargar grupos desde Supabase CON CACHE"""
        try:
            if _self.supabase:
                response = _self.supabase.table('grupos').select('*').execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error cargando grupos: {e}")
            return pd.DataFrame()
    
    def insertar_estudiante(self, estudiante_data):
        """Insertar nuevo estudiante en la base de datos"""
        try:
            if self.supabase:

                data_convertida = self._convertir_tipos_datos(estudiante_data)
                response = self.supabase.table('estudiantes').insert(data_convertida).execute()
                

                st.cache_data.clear()
                
                return response.data[0] if response.data else None
            else:
                st.warning("Modo demo no disponible. Conecta a Supabase para insertar datos.")
                return None
        except Exception as e:
            st.error(f"Error insertando estudiante: {e}")
            return None
    
    def insertar_factor(self, factor_data):
        """Insertar nuevo factor de riesgo en la base de datos"""
        try:
            if self.supabase:

                data_convertida = self._convertir_tipos_datos(factor_data)
                response = self.supabase.table('factores').insert(data_convertida).execute()
                

                st.cache_data.clear()
                
                return response.data[0] if response.data else None
            else:
                st.warning("Modo demo no disponible. Conecta a Supabase para insertar datos.")
                return None
        except Exception as e:
            st.error(f"Error insertando factor: {e}")
            return None
    
    def insertar_calificacion(self, calificacion_data):
        """Insertar nuevo registro de calificaciones en la base de datos"""
        try:
            if self.supabase:
                if 'materia_id' not in calificacion_data:
                    st.error("❌ Error: falta materia_id en los datos de calificación")
                    return None
                

                data_convertida = self._convertir_tipos_datos(calificacion_data)
                response = self.supabase.table('registro_calificaciones').insert(data_convertida).execute()
                
                st.cache_data.clear()
                
                return response.data[0] if response.data else None
            else:
                st.warning("Modo demo no disponible. Conecta a Supabase para insertar datos.")
                return None
        except Exception as e:
            st.error(f"Error insertando calificación: {e}")
            return None
    
    def insertar_materia(self, materia_data):
        """Insertar nueva materia en la base de datos"""
        try:
            if self.supabase:
                data_convertida = self._convertir_tipos_datos(materia_data)
                response = self.supabase.table('materias').insert(data_convertida).execute()
                
                st.cache_data.clear()
                
                return response.data[0] if response.data else None
            else:
                st.warning("Modo demo no disponible. Conecta a Supabase para insertar datos.")
                return None
        except Exception as e:
            st.error(f"Error insertando materia: {e}")
            return None
    
    def insertar_grupo(self, grupo_data):
        """Insertar nuevo grupo en la base de datos"""
        try:
            if self.supabase:

                data_convertida = self._convertir_tipos_datos(grupo_data)
                response = self.supabase.table('grupos').insert(data_convertida).execute()
                
                st.cache_data.clear()
                
                return response.data[0] if response.data else None
            else:
                st.warning("Modo demo no disponible. Conecta a Supabase para insertar datos.")
                return None
        except Exception as e:
            st.error(f"Error insertando grupo: {e}")
            return None
    
    def _convertir_tipos_datos(self, data):
        """Convertir tipos de datos de pandas/python nativos a tipos JSON serializables"""
        import numpy as np
        try:
            data_convertida = {}
            for key, value in data.items():
                if value is None:
                    data_convertida[key] = None
                elif hasattr(value, 'item'):  # Para numpy types
                    data_convertida[key] = value.item()
                elif isinstance(value, (int, float, str, bool)):
                    data_convertida[key] = value
                elif isinstance(value, (np.integer, np.floating)):
                    data_convertida[key] = value.item()
                else:
                    # Convertir a string como último recurso
                    data_convertida[key] = str(value)
            return data_convertida
        except Exception as e:
            st.error(f"Error convirtiendo tipos de datos: {e}")
            return data
    
    def obtener_materias_por_carrera(self, carrera_id):
        """Obtener materias filtradas por carrera"""
        try:
            if self.supabase:
                response = self.supabase.table('materias').select('*').eq('carrera_id', carrera_id).execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error obteniendo materias: {e}")
            return pd.DataFrame()
    
    def obtener_grupos_por_materia(self, materia_id, periodo):
        """Obtener grupos filtrados por materia y periodo"""
        try:
            if self.supabase:
                response = self.supabase.table('grupos').select('*').eq('materia_id', materia_id).eq('periodo', periodo).execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error obteniendo grupos: {e}")
            return pd.DataFrame()
    
    def limpiar_cache(self):
        """Método para limpiar manualmente el cache"""
        st.cache_data.clear()
        st.success("✅ Cache limpiado correctamente")

    def obtener_materias_profesor(self, profesor_id):
        """Obtener materias asignadas a un profesor"""
        try:
            if self.supabase:
                response = self.supabase.table('profesor_materias')\
                    .select('materia_id, materias(*)')\
                    .eq('profesor_id', profesor_id)\
                    .execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error obteniendo materias del profesor: {e}")
            return pd.DataFrame()

    def obtener_estudiantes_por_materia(self, materia_id):
        """Obtener estudiantes de una materia específica"""
        try:
            if self.supabase:
                response = self.supabase.table('registro_calificaciones')\
                    .select('*, estudiantes(*)')\
                    .eq('materia_id', materia_id)\
                    .execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error obteniendo estudiantes: {e}")
            return pd.DataFrame()

    def obtener_profesores(self):
        """Obtener lista de todos los profesores"""
        try:
            if self.supabase:
                response = self.supabase.table('profesores')\
                    .select('*')\
                    .order('nombre')\
                    .execute()
                return pd.DataFrame(response.data) if response.data else pd.DataFrame()
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error obteniendo profesores: {e}")
            return pd.DataFrame()