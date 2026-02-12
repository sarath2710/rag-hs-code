import re
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from app.qdrant_db import get_storage_context

def get_index():
    storage_context = get_storage_context()
    return VectorStoreIndex.from_vector_store(
        storage_context.vector_store
    )

def retrieve(question, top_k=50):
    index = get_index()
    docs = []

    hs_match = re.search(r"\b\d{6,12}\b", question)

    # CASE 1️ : EXACT 12 DIGIT
    if hs_match and len(hs_match.group()) == 12:
        hs_code = hs_match.group()

        filters = MetadataFilters(
            filters=[
                ExactMatchFilter(
                    key="new_hs_code",
                    value=hs_code
                )
            ]
        )

        retriever = index.as_retriever(
            similarity_top_k=1,
            filters=filters
        )

        nodes = retriever.retrieve("hs code lookup")

    # CASE 2️ : Prefix search
    # elif hs_match:
    #     prefix = hs_match.group()

    #     # Fetch many → filter manually
    #     retriever = index.as_retriever(similarity_top_k=top_k)
    #     nodes = retriever.retrieve(prefix)

    #     nodes = [
    #         n for n in nodes
    #         if n.metadata
    #         and n.metadata.get("new_hs_code", "").startswith(prefix)
    #     ]

    elif hs_match:
        prefix = hs_match.group()

        # guard: avoid too-short prefixes
        if len(prefix) < 6:
            return []

        retriever = index.as_retriever(
            similarity_top_k=10000   # should cover full dataset
        )

        # neutral query = no semantic bias
        nodes = retriever.retrieve("")

        # manual prefix filtering
        nodes = [
            n for n in nodes
            if n.metadata
            and n.metadata.get("new_hs_code", "").startswith(prefix)
        ]

    # CASE 3️ : DESCRIPTION
    else:
        retriever = index.as_retriever(similarity_top_k=10)
        nodes = retriever.retrieve(question)

    # Final output
    for n in nodes:
        if n.metadata:
            docs.append({
                "new_hs_code": n.metadata.get("new_hs_code"),
                "old_hs_code": n.metadata.get("old_hs_code"),
                "duty_percentage": n.metadata.get("duty_percentage"),
                "description": n.text
            })

    return docs
