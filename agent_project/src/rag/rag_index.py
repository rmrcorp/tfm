import os
import pickle
import shutil
from pathlib import Path

from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import LocalFileStore, EncoderBackedStore
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

from qdrant_client.http import models
from src.rag.rag_config import FOLDER_FILES_NAME, qdrant_client, COLLECTION_NAME, vector_store, child_splitter, \
    parent_splitter

# Carpeta donde guardaremos los textos completos (Padres)
DOC_STORE_PATH = "./doc_store_cache"

def index_process_files():
    print("--- Indexando Documentos Procesos .md ---")
    raw_docs = DirectoryLoader(FOLDER_FILES_NAME, glob="**/*.md", loader_cls=TextLoader).load()
    if not raw_docs:
        print("No hay procesos para indexar.")
        return

    _override_metadata(raw_docs)
    _add_master_index_doc(raw_docs)

    try:
        _clean_current_data()

        fs = LocalFileStore(Path(DOC_STORE_PATH))
        store = EncoderBackedStore(
            store=fs,
            key_encoder=lambda x: x,
            value_serializer=pickle.dumps,
            value_deserializer=pickle.loads
        )

        retriever = ParentDocumentRetriever(
            vectorstore=vector_store,
            docstore=store,
            child_splitter=child_splitter,
            parent_splitter=parent_splitter
        )

        # - Guardar hijos en Qdrant (vector_store).
        # - Guardar padres en doc_store (fs).
        retriever.add_documents(raw_docs, ids=None)
        print(f"Indexación completada. Documentos padres guardados en '{DOC_STORE_PATH}'.")
    except Exception as e:
        print(f"Error en la indexación: {e}")


def _override_metadata(raw_docs: list[Document]):
    for doc in raw_docs:
        # Obtenemos la ruta original: "procesos/nombre_proceso.md"
        full_path = doc.metadata.get("source", "")
        # Obtenemos solo el nombre del fichero: "nombre_proceso.md"
        file_name = os.path.basename(full_path)
        # se sobreescribe el metadata "source"
        doc.metadata["source"] = file_name


def _clean_current_data():
    qdrant_client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=models.FilterSelector(
            filter=models.Filter(must=[])
        )
    )
    print("Colección limpiada.")
    if os.path.exists(DOC_STORE_PATH):
        shutil.rmtree(DOC_STORE_PATH)
        print("Cache local de documentos limpiada.")


def _add_master_index_doc(raw_docs: list[Document]):
    # --- Generación del Índice Maestro ---
    process_names = []
    for d in raw_docs:
        name = os.path.basename(d.metadata.get('source', ''))
        process_names.append(f"- {name}")
    processes = "\n".join(process_names)
    content_index_prompt = f"""
        ESTE DOCUMENTO ES UN RESUMEN DE CAPACIDADES DEL SISTEMA.

        Listado de procesos disponibles actualmente en la base de datos:
       {processes}

        PALABRAS CLAVE PARA ACTIVAR ESTE DOCUMENTO:
        procesos a realizar, todo lo que se puede hacer, qué sabes hacer, lista de tareas, 
        menú de opciones, capacidades, catálogo de servicios, qué opciones tengo,
        qué procesos sabes, qué procesos conoces, dime tus procesos, menú, opciones, catálogo, listado de tareas,
        posibles procesos, capacidades.
        """

    raw_docs.append(Document(
        page_content=content_index_prompt,
        metadata={"source": "INDICE_MAESTRO", "type": "system_index"}
    ))