import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from qdrant_client.http import models

from src.agent.model import llm
from src.rag.rag_config import qdrant_client, COLLECTION_NAME
from src.rag.rag_retriver import get_retriever

def find_context(query: str) -> str:
    try:
        target_process = detect_document_target(query)
        results = get_retriever(process_filter=target_process).invoke(query)
        if not results:
            return ""
        accumulated_context = ""
        for doc in results:
            nombre_doc = os.path.basename(doc.metadata.get('source', 'desconocido'))
            accumulated_context += f"\n--- PROCESO COMPLETO ({nombre_doc}) ---\n{doc.page_content}\n"
        return accumulated_context + "\n--------------------------------\n"

    except Exception as e:
        print(f"Error RAG (Parent Retriever): {e}")
        return ""


def get_master_index() -> str:
    try:
        res = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.source",
                        match=models.MatchValue(value="INDICE_MAESTRO")
                    )
                ]
            ),
            limit=1
        )
        points, _ = res

        if points:
            # En Qdrant puro el contenido suele estar en payload['page_content']
            content = points[0].payload.get('page_content', '')
            return f"\n--- LISTADO OFICIAL DE PROCESOS ---\n{content}\n--------------------------------\n"

        return "Error: El Índice Maestro no se encuentra en la base de datos."

    except Exception as e:
        print(f"Error recuperando índice directo: {e}")
        return ""

def detect_document_target(query: str) -> str:
    master_index = get_master_index()

    prompt = ChatPromptTemplate.from_template(
        """ERES EL GESTOR DE UNA BIBLIOTECA DE PROCEDIMIENTOS.

        TU CATÁLOGO ACTUAL (Recuperado de Base de Datos):
        {indice}

        SOLICITUD DEL USUARIO: "{query}"

        TAREA:
        Identifica cuál de los archivos del catálogo es el más adecuado para responder al usuario.

        REGLAS:
        1. Responde ÚNICAMENTE con el nombre exacto del archivo (ej: 'alta_cliente.md').
        2. Si la solicitud es ambigua, genérica o no encaja claro, responde "TODOS".
        3. No expliques nada. Solo el nombre del archivo.

        NOMBRE DEL ARCHIVO:"""
    )

    chain = prompt | llm | StrOutputParser()

    try:
        # 3. Invocamos al LLM con el índice real
        file_name = chain.invoke({
            "indice": master_index,
            "query": query
        }).strip()

        # Limpieza básica por si el LLM devuelve comillas o espacios extra
        file_name = file_name.replace("'", "").replace('"', "")

        print(f"Documento Objetivo: '{file_name}'")
        return file_name

    except Exception as e:
        print(f"Error en detectando el documento objetivo: {e}")
        return "TODOS"