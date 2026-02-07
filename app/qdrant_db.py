from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext
from app.config import QDRANT_URL, COLLECTION_NAME

def get_storage_context():
    client = QdrantClient(
        url=QDRANT_URL,
        prefer_grpc=False
    )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    return storage_context
