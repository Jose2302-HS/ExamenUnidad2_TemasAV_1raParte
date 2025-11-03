import streamlit as st
from services.auth_service import AuthService

def mostrar_login():
    st.markdown("""
    <style>
      .login-card {max-width:420px;margin:6rem auto;padding:2rem;border:1px solid #ddd;border-radius:12px;background:#fff;box-shadow:0 8px 24px rgba(0,0,0,.06)}
    </style>
    """, unsafe_allow_html=True)

    if "user" in st.session_state and st.session_state["user"] is not None:
        st.success(f"Sesión activa: {st.session_state['user']['usuario']}")
        if st.button("Cerrar sesión"):
            st.session_state["user"] = None
            st.rerun()
        return

    tab_login, tab_signup = st.tabs(["🔐 Iniciar sesión", "🆕 Crear usuario"])

    with tab_login:
        with st.form("login"):
            usuario = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            ok = st.form_submit_button("Entrar")
        if ok:
            auth = AuthService()
            u = auth.verificar_login(usuario, password)
            if u:
                st.session_state["user"] = u
                st.success("Acceso concedido")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

    with tab_signup:
        st.info("Crea un usuario local (tabla `usuarios`).")
        with st.form("signup"):
            usuario = st.text_input("Nuevo usuario")
            password = st.text_input("Contraseña", type="password")
            password2 = st.text_input("Repite la contraseña", type="password")
            ok = st.form_submit_button("Crear")
        if ok:
            if not usuario or not password:
                st.error("Completa usuario y contraseña")
            elif password != password2:
                st.error("Las contraseñas no coinciden")
            else:
                auth = AuthService()
                creado = auth.crear_usuario(usuario, password)
                if creado:
                    st.success("Usuario creado. Ahora inicia sesión en la pestaña anterior.")
                else:
                    st.warning("Ese usuario ya existe")
