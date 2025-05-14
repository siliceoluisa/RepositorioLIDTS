import streamlit as st
from login import login_vista
from register import vista_registro
from dashboard import dashboard_vista 
from upload_files import subir_archivo
from view_documents import mostrar_documentos
from profile_repo import vista_perfil

# Inicializar el estado de sesión si no existe
if "view" not in st.session_state:
    st.session_state.view = "login"  # Vista inicial

# Control de navegación entre vistas
if st.session_state.view == "login":
    login_vista()
elif st.session_state.view == "registro":
    vista_registro()
elif st.session_state.view == "dashboard":
    dashboard_vista()
elif st.session_state.view == "upload":
    subir_archivo()
elif st.session_state.view == "docs":
    mostrar_documentos()
elif st.session_state.view == "profile":
    vista_perfil()