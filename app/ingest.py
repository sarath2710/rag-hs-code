import pandas as pd
from llama_index.core import Document, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from app.qdrant_db import get_storage_context
from app.config import EMBED_MODEL

def ingest_excel(path):
    df = pd.read_excel(path)

    documents = []
    for _, row in df.iterrows():
        old_code = str(row["OldHSCode"]).zfill(8)
        new_code = str(row["NewHSCode"]).zfill(12)
        
        text = (
            f"HS Code Information.\n"
            f"Old HS Code: {old_code}\n"
            f"New HS Code: {new_code}\n"
            f"Arabic Description: {row['LongDescAr']}\n"
            f"English Description: {row['LongDescEn']}\n"
            f"Duty Percentage: {row['DutyPercentage']}"
        )

        documents.append(
            Document(
                text=text,
                metadata={
                    "old_hs_code": old_code,
                    "new_hs_code": new_code,
                    "duty_percentage": row["DutyPercentage"],
                    "description": str(row["LongDescEn"]),
                }
            )
        )

    # EXPLICIT EMBEDDING MODEL
    embed_model = HuggingFaceEmbedding(
        model_name=EMBED_MODEL
    )

    # EXPLICIT STORAGE CONTEXT (Qdrant)
    storage_context = get_storage_context()

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,   # REQUIRED
        show_progress=True
    )

    print("---> Ingest completed successfully")
