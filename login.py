import streamlit as st
from conection import conn  
from PIL import Image

def check_credentials(correo, contrasena):
    """Verifica las credenciales del usuario en la base de datos."""
    if conn:
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (correo, contrasena))
            user = cursor.fetchone()
            return user  
        except Exception as e:
            st.error(f"Error al verificar las credenciales: {e}")
        finally:
            cursor.close()
    return None  

def login_vista():

    """Vista de inicio de sesión."""
    st.title("Login")

    correo = st.text_input("Correo", placeholder="👤 Ingresa tu correo institucional...", key="login_email")
    contrasena = st.text_input("Contraseña", type="password", placeholder="🔒 Ingresa tu contraseña...")

    if st.button("Iniciar sesión"):
        user = check_credentials(correo, contrasena)
        if user:
            # Guarda los detalles del usuario en la sesión
            st.session_state.view = "dashboard"
            st.session_state.id_user = user[0]  # Cambia a la vista de dashboard
            st.session_state.username = user[1]  # Guarda el nombre del usuario en la sesión
            st.session_state.email = user[2]
            st.session_state.profile_picture = user[6]  # Suponiendo que la columna 'profile_picture' contiene la ruta de la imagen
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    
    st.subheader("¿No tienes cuenta? Regístrate aquí:")
    
    if st.button("Registrar"):
        st.session_state.view = "registro"
        st.rerun()


