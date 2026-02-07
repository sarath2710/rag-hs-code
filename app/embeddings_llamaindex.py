from llama_index.embeddings.huggingface import HuggingFaceEmbedding

EMBED_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

def get_embed_model():
    return HuggingFaceEmbedding(
        model_name=EMBED_MODEL_NAME
    )
