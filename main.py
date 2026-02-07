from app.ingest import ingest_excel
from app.rag_pipeline import run_rag

from app.llama_settings import init_llama_settings
init_llama_settings() 

# Run once to ingest data
# ingest_excel(r"/home/ubuntu/rag-hs-code/data/hs_code.xlsx")


while True:
    q = input("Ask: ")
    print("------------------------- Retrieved data --------------------------")
    if q.lower() in ["exit", "quit"]:
        break
    print(run_rag(q))
    print("-------------------------------------------------------------------")
