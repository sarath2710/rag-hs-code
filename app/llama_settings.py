from llama_index.core import Settings
from app.embeddings_llamaindex import get_embed_model

def init_llama_settings():
    Settings.embed_model = get_embed_model()

# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.core import Settings
# from app.config import EMBED_MODEL

# Settings.embed_model = HuggingFaceEmbedding(
#     model_name=EMBED_MODEL
# )
