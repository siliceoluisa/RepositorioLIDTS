import streamlit as st
from conection import conn
import os
from PIL import Image


def obtener_datos_usuario(id_user):
    """Obtiene los datos del usuario de la base de datos."""
    cursor = conn.cursor()
    try:
        query = "SELECT name, email, type_user, profile_picture FROM users WHERE id_user = %s"
        cursor.execute(query, (id_user,))
        return cursor.fetchone()
    except Exception as e:
        st.error(f"Error al obtener los datos del usuario: {e}")
    finally:
        cursor.close()
    return None

def actualizar_foto_perfil(id_user, nueva_foto):
    """Actualiza la foto de perfil del usuario en la base de datos."""
    cursor = conn.cursor()
    try:
        query = "UPDATE users SET profile_picture = %s WHERE id_user = %s"
        cursor.execute(query, (nueva_foto, id_user))
        conn.commit()
        st.success("Foto de perfil actualizada con éxito.")
    except Exception as e:
        st.error(f"Error al actualizar la foto de perfil: {e}")
    finally:
        cursor.close()

def vista_perfil():
    """Vista del perfil del usuario, donde se puede editar la información personal y la contraseña."""

    st.title("Perfil del Usuario")

    # Verificar que el usuario esté logueado
    if 'id_user' not in st.session_state:
        st.warning("Debes iniciar sesión para ver tu perfil.")
        return

    # Obtener información del usuario desde la base de datos
    user_id = st.session_state.id_user
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id_user = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        name, email, password, type_user, fecha_registro, profile_picture = user[1:7]

        # Mostrar la foto de perfil actual, si existe
        if profile_picture and os.path.exists(profile_picture):
            st.image(profile_picture, width=100)
        else:
            st.image("./img/default_profile.png", width=100)  # Imagen por defecto si no tiene foto

        # Mostrar nombre y correo (no editable)
        st.write(f"**Nombre:** {name}")
        st.write(f"**Correo:** {email}")
        st.write(f"**Tipo de Usuario:** {type_user}")
        st.write(f"**Fecha de Registro:** {fecha_registro}")

        # Campo para editar nombre y tipo de usuario
        nuevo_nombre = st.text_input("Nuevo Nombre", value=name)
        nuevo_tipo_usuario = st.selectbox("Nuevo Tipo de Usuario", ["Alumno", "Profesor", "Administrativo", "Otro"], index=["Alumno", "Profesor", "Administrativo", "Otro"].index(type_user))

        # Campo para cambiar la foto de perfil
        nueva_foto = st.file_uploader("Sube una nueva foto de perfil", type=["jpg", "png", "jpeg"])

        # Campo para cambiar la contraseña
        nueva_contrasena = st.text_input("Nueva Contraseña", type="password", placeholder="🔒 Ingresa tu nueva contraseña...")
        confirmar_contrasena = st.text_input("Confirmar Contraseña", type="password", placeholder="🔒 Confirma tu nueva contraseña...")

        # Comprobar si las contraseñas coinciden
        if nueva_contrasena and nueva_contrasena != confirmar_contrasena:
            st.error("Las contraseñas no coinciden.")
        
        # Botón de guardar cambios
        if st.button("Guardar Cambios"):
            # Validar cambios
            if nueva_contrasena == confirmar_contrasena:
                # Guardar la nueva foto si se ha subido
                if nueva_foto:
                    photo_path = f"./profile_pics/{user_id}_profile.jpg"
                    with open(photo_path, "wb") as f:
                        f.write(nueva_foto.getbuffer())
                else:
                    photo_path = profile_picture  # No cambiar la foto si no se subió una nueva

                # Actualizar la información del usuario
                cursor = conn.cursor()
                try:
                    # Si no se ha ingresado una nueva contraseña, no actualizar la contraseña
                    if nueva_contrasena:
                        cursor.execute("""
                            UPDATE users SET name = %s, type_user = %s, profile_picture = %s, password = %s WHERE id_user = %s
                        """, (nuevo_nombre, nuevo_tipo_usuario, photo_path, nueva_contrasena, user_id))
                    else:
                        cursor.execute("""
                            UPDATE users SET name = %s, type_user = %s, profile_picture = %s WHERE id_user = %s
                        """, (nuevo_nombre, nuevo_tipo_usuario, photo_path, user_id))
                    conn.commit()
                    st.success("¡Tu perfil ha sido actualizado exitosamente!")
                except Exception as e:
                    st.error(f"Error al actualizar el perfil: {e}")
                finally:
                    cursor.close()
            else:
                st.error("Por favor, ingresa las contraseñas correctamente.")
    else:
        st.error("Usuario no encontrado en la base de datos.")

    if st.button("Salir"):
        st.session_state.view = "dashboard"
        st.rerun()


# Si este script se ejecuta directamente, ejecutamos la vista de perfil
if __name__ == "__main__":
    vista_perfil()
