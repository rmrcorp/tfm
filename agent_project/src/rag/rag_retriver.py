import pickle

from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import LocalFileStore, EncoderBackedStore
from pathlib import Path

from qdrant_client import models

from src.rag.rag_config import vector_store, child_splitter, parent_splitter
from src.rag.rag_index import DOC_STORE_PATH


def get_retriever(process_filter: str = None):
    fs = LocalFileStore(Path(DOC_STORE_PATH))  # Mismo path que en indexación
    store = EncoderBackedStore(
        store=fs,
        key_encoder=lambda x: x,
        value_serializer=pickle.dumps,
        value_deserializer=pickle.loads
    )
    search_kwargs = {
        "k": 3,
        "score_threshold": 0.6
    }
    if process_filter and process_filter != "TODOS":
        # Creamos el filtro nativo de Qdrant
        qdrant_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.source",
                    match=models.MatchValue(value=process_filter)
                )
            ]
        )
        search_kwargs["filter"] = qdrant_filter

    retriever = ParentDocumentRetriever(
        vectorstore=vector_store,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
        search_kwargs=search_kwargs
    )

    return retriever