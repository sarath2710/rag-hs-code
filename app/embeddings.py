from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from app.config import EMBED_MODEL

embed_model = HuggingFaceEmbedding(
    model_name=EMBED_MODEL
)

def get_embed_model():
    return embed_model

