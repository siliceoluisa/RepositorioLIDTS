import streamlit as st
import re
import os
from conection import conn
from PIL import Image


def validar_correo(correo):
    """Verifica que el correo cumpla con el formato institucional."""
    patron = r'^[a-zA-Z]+[.][a-zA-Z]+[0-9]{2}@unach\.mx$'
    return bool(re.match(patron, correo))


def registrar_usuario(nombre, correo, contrasena, tipo_usuario, foto_perfil):
    """Registra un nuevo usuario en la base de datos."""
    if not nombre or not correo or not contrasena or not tipo_usuario:
        st.error("Por favor, completa todos los campos.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email = %s", (correo,))
    if cursor.fetchone():
        st.error("El correo ya está registrado.")
        cursor.close()
        return

    # Crear carpeta si no existe
    photo_dir = "profile_pics"
    os.makedirs(photo_dir, exist_ok=True)

    ruta_foto = None
    if foto_perfil:
        # Crear nombre de archivo único basado en el correo
        nombre_archivo = correo.replace('@', '_').replace('.', '_') + "_profile.jpg"
        ruta_foto = os.path.join(photo_dir, nombre_archivo)

        # Guardar imagen físicamente
        with open(ruta_foto, "wb") as f:
            f.write(foto_perfil.getbuffer())

    if conn:
        try:
            query = """
            INSERT INTO users (name, email, password, type_user, profile_picture)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (nombre, correo, contrasena, tipo_usuario, ruta_foto))
            conn.commit()
            st.success(f"Usuario {nombre} registrado correctamente!")
            st.session_state.view = "login"  # Cambia a la vista de login después del registro
            st.rerun()
        except Exception as e:
            st.error(f"Error al registrar el usuario: {e}")
        finally:
            cursor.close()


def vista_registro():
    """Vista del formulario de registro."""
    st.title("Formulario de Registro Institucional")

    nombre = st.text_input("Nombre", placeholder="👤 Ingresa tu nombre completo...")
    correo = st.text_input("Correo Institucional", placeholder="✉️ Ingresa tu correo institucional...", key="register_email")
    contrasena = st.text_input("Contraseña", type="password", placeholder="🔒 Ingresa tu contraseña...", key="register_password")
    tipo_usuario = st.selectbox("Tipo de Usuario", ["Alumno", "Profesor", "Administrativo", "Otro"])
    foto_perfil = st.file_uploader("Sube tu foto de perfil", type=["jpg", "png", "jpeg"])

    if correo and not validar_correo(correo):
        st.error("El correo debe seguir el formato 'nombre.apellidoXX@unach.mx', donde XX son dos números.")

    if st.button("Registrar"):
        if validar_correo(correo):
            registrar_usuario(nombre, correo, contrasena, tipo_usuario, foto_perfil)
        else:
            st.error("Correo institucional inválido.")

    st.subheader("¿Ya tienes cuenta? Inicia sesión aquí:")

    if st.button("Login"):
        st.session_state.view = "login"
        st.rerun()

