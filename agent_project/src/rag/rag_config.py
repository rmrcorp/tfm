from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore

EMBEDDING_MODEL = "bge-m3"
EMBEDDING_MODEL_SIZE = 1024
COLLECTION_NAME = "procesos"
QDRANT_URL = "http://localhost:6333"
SCORE_THRESHOLD = 0.55
FOLDER_FILES_NAME = 'procesos'

def _create_qdrant_collection():
    if not qdrant_client.collection_exists(collection_name=COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=EMBEDDING_MODEL_SIZE,
                distance=models.Distance.COSINE
            )
        )
        print(f"Colección '{COLLECTION_NAME}' creada automáticamente.")

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
qdrant_client = QdrantClient(url=QDRANT_URL)

_create_qdrant_collection()

vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

'''
Hijo: pequeños para afinar en la búsqueda
'''
child_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
'''
Padre: Grande para devolver todo el contexto (recupera el .md entero)
asuminos que 5000 es suficiente para que entre el documento entero. Como vamos a contextualizar al modelo con el documento
hay que asegurarse que el LLM puede dentro de su ventana de contexto, en modelos grandes esa ventana es muy grande.
'''
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)