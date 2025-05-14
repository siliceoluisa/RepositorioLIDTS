import streamlit as st
from PIL import Image
import pandas as pd
from view_documents import mostrar_documentos
from  filter_files import filter_docs

logo_img = Image.open("./img/logounach.png")
st.set_page_config(page_title='Repositorio LIDTS', page_icon=logo_img, layout="wide")

def dashboard_vista():
    sidebar()
    with st.container():
        cols = st.columns([1, 3, 1, 1, 1])
        
        cols[0].image(logo_img, width=80)
        cols[1].write("")  

        if cols[2].button("Subir Archivo"):
            st.session_state.view = "upload"
            st.rerun()
        
        if cols[3].button("Perfil"):
            st.session_state.view = "profile" 
            st.rerun()
        
        if cols[4].button("Cerrar Sesión"):
            st.session_state.view = "login"
            del st.session_state["username"]
            del st.session_state["email"]
            st.rerun()

    st.title("Repositorio Licenciatura en Ingeniería en Desarrollo y Tecnologías de Software")
    
    # Bienvenida al usuario
    if "username" in st.session_state:
        st.success(f"¡Bienvenido, {st.session_state.username}! 🎉")
    
    # Barra de búsqueda (a implementar si deseas filtrar por título u autor)
    st.text_input("", placeholder="🔍 Escribe tu búsqueda aquí...")
    st.write("\n")

    # Video de presentación
    with open("./multimedios/lidts.mp4", "rb") as video_file:
        st.video(video_file.read(), start_time=0)  

    # Contenidos destacados
    st.subheader("Contenidos Destacados")
    st.write("Aquí algunos de nuestros contenidos más relevantes.")

    num_columns = 6  
    contents = [
        {"title": "Título 1", "description": "Descripción corta de este contenido destacado.", "image": "./img/logounach.png"},
        {"title": "Título 2", "description": "Descripción corta de este contenido destacado.", "image": "./img/logounach.png"},
        {"title": "Título 3", "description": "Descripción corta de este contenido destacado.", "image": "./img/logounach.png"},
        {"title": "Título 4", "description": "Descripción corta de este contenido destacado.", "image": "./img/logounach.png"},
        {"title": "Título 5", "description": "Descripción corta de este contenido destacado.", "image": "./img/logounach.png"},
        {"title": "Título 6", "description": "Descripción corta de este contenido destacado.", "image": "./img/logounach.png"},
    ]

    cols = st.columns(3)
    for i in range(0, num_columns, 3):
        with cols[0]:
            if i < num_columns:
                content = contents[i]
                img = Image.open(content["image"])
                st.image(img, use_container_width=True)
                st.write(f"**{content['title']}**")
                st.write(content["description"])

        if i + 1 < num_columns:
            with cols[1]:
                content = contents[i + 1]
                img = Image.open(content["image"])
                st.image(img, use_container_width=True)
                st.write(f"**{content['title']}**")
                st.write(content["description"])

        if i + 2 < num_columns:
            with cols[2]:
                content = contents[i + 2]
                img = Image.open(content["image"])
                st.image(img, use_container_width=True)
                st.write(f"**{content['title']}**")
                st.write(content["description"])

def sidebar():
    st.sidebar.image(logo_img, use_container_width=True)
    menu = ["Inicio", "Materias", "Tesis", "Artículos", "Conócenos"]
    option = st.sidebar.selectbox("Categorías", menu)

    # Filtro por fechas
    st.sidebar.title("Filtrar por Fechas")
    with st.sidebar.expander("Seleccionar fechas", expanded=True):
        start_date = st.date_input("Desde", pd.to_datetime("2024-01-01"))
        end_date = st.date_input("Hasta", pd.to_datetime("2025-12-31"))

    if st.sidebar.button("Buscar por fechas"):
        resultados_fecha = filter_docs(start_date, end_date)
        st.subheader("Resultados filtrados por fecha:")
        st.dataframe(resultados_fecha, use_container_width=True)

    # Filtro por categoría (materias)
    st.sidebar.title("Materias")
    categories = [
        "Inteligencia Artificial", "Sistemas Operativos", "Aplicaciones Web y Móviles", 
        "Conmutadores y Redes Inalámbricas", "Seguridad en Cómputo", "Análisis de Vulnerabilidades"
    ]
    selected_categories = [cat for cat in categories if st.sidebar.checkbox(cat, value=False)]

    if selected_categories:
        mostrar_documentos(selected_categories)
    else:
        st.sidebar.write("Selecciona categorías para filtrar")

    if option == "Tesis":
        st.write("Aquí puedes ver las tesis disponibles...")
    elif option == "Artículos":
        st.write("Aquí puedes ver los artículos relacionados...")
    elif option == "Conócenos":
        st.write("Información sobre LIDTS...")

# Main
if __name__ == "__main__":
    dashboard_vista()
