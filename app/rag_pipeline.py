# ================
from app.retriever import retrieve
from app.llm_client import ask_llm

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

#     prompt = f"""
# You are a customs HS code assistant.

# STRICT RULES:
# - Answer ONLY using the context
# - Do NOT guess
# - Do NOT call any tools or functions
# - Do NOT return JSON
# - Respond in plain English text
# - Provide both HS codes for the output:
#     * old_hs_code must be 8 digits
#     * new_hs_code must be 12 digits
# - If answer not found, say exactly:
#   "Not available in provided data!"

# Context:
# {context}

# Question:
# {question}

# Answer:
# """

    prompt = f"""
You are a customs HS code assistant.

STRICT RULES:
- Answer ONLY using the context provided
- Do NOT guess or assume
- Do NOT call any tools or functions
- Do NOT return JSON
- Respond in plain English text only
- If the answer is NOT found in the context, say exactly:
  "Not available in provided data!"

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

4. If the user provides a PARTIAL HS code (6 or 8 digits):
   - List ALL matching HS codes that start with the given digits
   - Format each result as:
     <new_hs_code> – <English Description>
   - One result per line

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
