import streamlit as st
import os
from conection import conn
from datetime import datetime
from PIL import Image

def guardar_archivo_en_bd(title, author, type_file, editor, place_publication, date_publication, description, file_path, id_materia):
    if conn:
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO files_repo (title, author, type_file, editor, place_publication, date_publication, description, file_path, id_materia)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (title, author, type_file, editor, place_publication, date_publication, description, file_path, id_materia))
            conn.commit()
            st.success("Archivo subido correctamente!")
        except Exception as e:
            st.error(f"Error al subir el archivo: {e}")
        finally:
            cursor.close()

def subir_archivo():
    st.title("Subir Archivos al Repositorio")
    
    # Sidebar con información del usuario
    st.sidebar.title("Información del Usuario")
    if "username" in st.session_state and "email" in st.session_state:
        profile_picture = st.session_state.get('profile_picture', None)

        if profile_picture and os.path.exists(profile_picture):
            st.sidebar.image(profile_picture, width=300)
        else:
            st.sidebar.write("**No hay foto de perfil disponible.**")
        st.sidebar.write(f"**Nombre:** {st.session_state.username}")
        st.sidebar.write(f"**Correo:** {st.session_state.email}")

    else:
        st.sidebar.write("No hay usuario autenticado.")
    
    if st.sidebar.button("Inicio"):
        st.session_state.view = "dashboard"
        st.rerun()
    
    title = st.text_input("Título del Archivo")
    author = st.text_input("Autor")
    type_file = st.selectbox("Tipo de Archivo", ["Tesis", "Artículo", "Libro", "Otro"])
    editor = st.text_input("Editor (Opcional)")
    place_publication = st.text_input("Lugar de Publicación")
    date_publication = st.date_input("Fecha de Publicación")
    description = st.text_area("Descripción")
    file = st.file_uploader("Subir Archivo", type=["pdf", "docx", "txt"])  # Restringimos a ciertos formatos
    
    materias = ["Sistemas operativos", "Inteligencia artificial", "Desarrollo de aplicaciones web y móviles", "Conmutadores y redes inalámbricas", "Seguridad en cómputo", "Análisis de vulnerabilidades"]
    id_materia = st.selectbox("Selecciona una materia", materias)
    
    if file and st.button("Subir Archivo"):
        save_path = os.path.join("uploads", file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        
        guardar_archivo_en_bd(title, author, type_file, editor, place_publication, date_publication, description, save_path, id_materia)

if __name__ == "__main__":
    subir_archivo()
