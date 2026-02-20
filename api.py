from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import run_rag
from app.llama_settings import init_llama_settings
init_llama_settings() 


app = FastAPI()

class Question(BaseModel):
    question: str


# @app.post("/hs-code-query")
# def ask_question(data: Question):
#     q = data.question
#     if not q.strip():
#         return {"error": "Question is empty"}
#     print("hi")
#     answer = run_rag(q)
#     print("hello")
#     return {
#         "question": q,
#         "answer": answer
#     }

@app.post("/hs-code-query")
def ask_question(data: Question):
    return {"answer": "test working"}