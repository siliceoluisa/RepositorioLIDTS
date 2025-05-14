import streamlit as st
import pandas as pd
from conection import conn
import os
from PIL import Image
from pdf2image import convert_from_path

def obtener_documentos_por_materia(materias_seleccionadas):
    """Obtiene los documentos de la base de datos filtrados por materia."""
    documentos = []
    if conn and materias_seleccionadas:
        cursor = conn.cursor()
        try:
            placeholders = ', '.join(['%s'] * len(materias_seleccionadas))
            query = f"""
                SELECT f.title, f.author, f.type_file, f.date_publication, f.description, f.file_path, s.name AS materia
                FROM files_repo f
                JOIN subjects s ON f.id_materia = s.id_materia
                WHERE s.name IN ({placeholders})
            """
            cursor.execute(query, materias_seleccionadas)
            documentos = cursor.fetchall()
        except Exception as e:
            st.error(f"Error al obtener documentos: {e}")
        finally:
            cursor.close()
    return documentos


def generar_portada_pdf(pdf_path):
    # Crear la carpeta "portadas" si no existe
    output_dir = "portadas"
    os.makedirs(output_dir, exist_ok=True)

    # Obtener el nombre del archivo sin extensión
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(output_dir, f"{file_name}.png")

    # Convertir la primera página del PDF en una imagen
    images = convert_from_path(pdf_path, first_page=1, last_page=1)

    if images:
        # Guardar la primera página como imagen
        portada = images[0]
        portada.save(output_path, 'PNG')  # Guardar la imagen en formato PNG
        return output_path
    else:
        return None

def mostrar_documentos(materias_seleccionadas):
    st.sidebar.title("Filtrar por Materia")
    categorias = [
        "Inteligencia Artificial", "Sistemas Operativos", "Aplicaciones Web y Móviles", 
        "Conmutadores y Redes Inalámbricas", "Seguridad en Cómputo", "Análisis de Vulnerabilidades"
    ]
    
    if materias_seleccionadas:
        documentos = obtener_documentos_por_materia(materias_seleccionadas)
        if documentos:
            # Dividir el espacio en 3 columnas
            cols = st.columns(3)
            # Iterar sobre los documentos y distribuirlos en las columnas
            for i, doc in enumerate(documentos):
                col = cols[i % 3]  # Usar la columna correspondiente

                with col:
                    st.subheader(doc[0])  # Título
                    st.write(f"**Autor:** {doc[1]}")
                    st.write(f"**Tipo:** {doc[2]}")
                    st.write(f"**Fecha de Publicación:** {doc[3]}")
                    st.write(f"**Descripción:** {doc[4]}")

                    # Ruta del archivo (documento PDF)
                    file_path = doc[5]

                    # Generar portada desde el PDF si es un documento PDF
                    if file_path.lower().endswith(".pdf"):
                        portada_path = generar_portada_pdf(file_path)
                        if portada_path:
                            img = Image.open(portada_path)
                            st.image(img, caption="Portada del Documento", width=150, use_container_width=True)  # Ajuste de tamaño de la imagen
                        else:
                            st.warning("No se pudo generar la portada del documento.")
                    else:
                        st.warning("El documento no es un PDF o no tiene portada.")

                    # Mostrar el botón de descarga solo si el archivo existe
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="Descargar Documento",
                                data=file,
                                file_name=os.path.basename(file_path),  # Nombre del archivo en la descarga
                                mime="application/octet-stream"  # Tipo MIME para archivos genéricos binarios
                            )
                    else:
                        st.error(f"El archivo no se encuentra disponible en la ruta {file_path}.")
                    st.divider()
        else:
            st.info("No hay documentos disponibles para la materia seleccionada.")
    else:
        st.warning("Selecciona al menos una materia para mostrar los documentos.")
    

if __name__ == "__main__":
    mostrar_documentos()
 