from app.retriever import retrieve
from app.llm_client import ask_llm
import requests as r
def run_rag(question):
    docs = retrieve(question)

    if not docs:
        return "Not available in provided data...."

    context = ""

    for d in docs:
        context += (
            f"HS Code: {d.get('new_hs_code', 'N/A')}\n"
            f"Old HS Code: {d.get('old_hs_code', 'N/A')}\n"
            f"Duty Percentage: {d.get('duty_percentage', 'N/A')}\n"
            f"Description:\n{d.get('description', 'N/A')}\n\n"
        )

    print(context)
    print("----------------------- The final output is -----------------------")

    prompt = f"""
You are a customs HS code assistant.

STRICT RULES:
- You MUST read EVERY row in the context
- You MUST NOT skip any row
- You MUST NOT guess or assume
- You MUST answer ONLY using the context
- Do NOT return JSON
- Respond ONLY in plain English text
- If no matching data exists, say exactly:
  "Not available in provided data!"

TASK INSTRUCTIONS (VERY IMPORTANT):

If the question contains a PARTIAL HS code (6 or 8 digits):
- Treat the given number as a PREFIX
- CHECK EVERY "HS Code" in the context
- SELECT ALL rows where:
  HS Code STARTS WITH the given digits
- For EACH matching row, output exactly:
  <new_hs_code> – <English Description>
- Output ONE result per line
- Do NOT explain anything
- Do NOT merge rows
- Do NOT add extra text


UNDERSTAND THE QUESTION TYPE CAREFULLY:

1. If the user asks for an HS code based on a product description:
   - Provide BOTH HS codes
   - old_hs_code must be exactly 8 digits
   - new_hs_code must be exactly 12 digits
   - Format:
     The HS code for <product> is <new_hs_code>.
     The old HS code is <old_hs_code> and the new HS code is <new_hs_code>.

2. If the user asks for the description of a given HS code:
   - Identify whether it matches HS code or Old hs code
   - Return ONLY the description text in a full sentence

3. If the user asks for the duty percentage of a given HS code:
   - Return ONLY the duty percentage in a clear sentence

"LANGUAGE RULE:\n"
    "- Detect the language of the user's question.\n"
    "- If the question is in English, reply in English.\n"
    "- If the question is in Arabic, reply in Arabic.\n"
    "- Do NOT mix languages.\n"
    "- Use the same language as the user."
DO NOT include extra explanations.
DO NOT mix multiple answers.
Answer ONLY what the question asks.

Context:
{context}

Question:
{question}

Answer:
"""


    try:
        return ask_llm(prompt)
    except Exception as e:
        return context
