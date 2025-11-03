import streamlit as st
from services.database import DatabaseService
from services.analytics import AnalyticsService
from components.dashboard import mostrar_dashboard_principal
from components.registro_datos import mostrar_registro_datos
from components.analisis_calidad import mostrar_analisis_calidad
from components.exportacion import mostrar_exportar_reportes
from components.login import mostrar_login


st.set_page_config(
    page_title="Sistema de Análisis Educativo - ITT",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1f3a60; text-align: center; margin-bottom: 2rem; font-weight: bold; }
    .sub-header { font-size: 1.8rem; color: #2c3e50; margin-bottom: 1rem; font-weight: bold; }
    .metric-card { background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #3498db; margin-bottom: 1rem; }
    .success-text { color: #27ae60; } .warning-text { color: #f39c12; } .danger-text { color: #e74c3c; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def inicializar_servicios():
    """Cache de la inicialización de servicios - OPTIMIZADO"""
    database_service = DatabaseService()
    analytics = AnalyticsService(database_service)
    return database_service, analytics

def main():

    database_service, analytics = inicializar_servicios()
    

    st.markdown('<div class="main-header">🎓 SISTEMA DE ANÁLISIS EDUCATIVO - ITT</div>', unsafe_allow_html=True)
 
    if "user" not in st.session_state:
        st.session_state["user"] = None

    if st.session_state["user"] is None:
        st.title("Acceso")
        mostrar_login()
        st.stop()


    with st.sidebar:
        st.caption(f"Usuario: **{st.session_state['user']['usuario']}**")
        if st.button("Cerrar sesión"):
            st.session_state["user"] = None
            st.rerun()

    

    with st.sidebar:
        st.image("https://www.tijuana.tecnm.mx/wp-content/themes/tecnm/images/logo_TECT.png", width=150)
        st.title("Navegación")
        
        opcion = st.radio(
            "Selecciona una opción:",
            ["🏠 Dashboard Principal", "📊 Análisis de Calidad", 
             "📋 Registro de Datos", "📤 Exportar Reportes"]
        )
        

        st.divider()
        if st.button("🔄 Actualizar Datos", use_container_width=True):
            analytics.actualizar_datos()
            st.rerun()
        

        st.divider()
        st.caption("💡 Los datos se actualizan automáticamente cada 5 minutos")
        st.caption("🔄 Usa el botón 'Actualizar Datos' para forzar una actualización")
    

    try:
        if opcion == "🏠 Dashboard Principal":
            mostrar_dashboard_principal(analytics)
        elif opcion == "📊 Análisis de Calidad":
            mostrar_analisis_calidad(analytics)
        elif opcion == "📋 Registro de Datos":
            mostrar_registro_datos(database_service)
        elif opcion == "📤 Exportar Reportes":
            mostrar_exportar_reportes(database_service)
    except Exception as e:
        st.error(f"❌ Error cargando la sección: {e}")
        st.info("💡 Esto puede ser normal cuando la base de datos está vacía o hay problemas de conexión.")

if __name__ == "__main__":
    main()