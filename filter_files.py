import streamlit as st
from conection import conn
import pandas as pd

def filter_docs(fecha_inicio, fecha_fin):
    """Consulta los documentos que están entre las fechas especificadas."""
    try:
        cursor = conn.cursor()
        query = """
            SELECT f.title, f.author, f.type_file, f.date_publication, f.description, f.file_path, s.name AS materia
            FROM files_repo f
            JOIN subjects s ON f.id_materia = s.id_materia
            WHERE f.date_publication BETWEEN %s AND %s
            ORDER BY f.date_publication DESC;
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()

        # Convertir los resultados a un formato compatible con la visualización
        documentos = []
        for row in resultados:
            documentos.append({
                "title": row[0],
                "author": row[1],
                "type": row[2],
                "date_publication": row[3],
                "description": row[4],
                "file_path": row[5],
                "materia": row[6]
            })
        
        return documentos

    except Exception as e:
        st.error(f"Error al filtrar documentos por fecha: {e}")
        return []  # Retorna vacío si hay error

    finally:
        cursor.close()
