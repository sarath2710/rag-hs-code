import requests
from app.config import LLM_URL, LLM_API_KEY, LLM_MODEL

def ask_llm(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}"
    }

    payload = {
        "model": LLM_MODEL,

        # IMPORTANT: Disable tool / function calling
        "tool_choice": "none",

        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a customs HS code assistant.\n"
                    "Answer ONLY using the given context.\n"
                    "Do NOT guess.\n"
                    "Do NOT call any functions.\n"
                    "Do NOT return JSON.\n"
                    "Respond ONLY in plain text."
                    "\n"
                    "LANGUAGE RULE:\n"
                    "- Detect the language of the user's question.\n"
                    "- If the question is in English, reply in English.\n"
                    "- If the question is in Arabic, reply in Arabic.\n"
                    "- Do NOT mix languages.\n"
                    "- Use the same language as the user."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 2000
    }

    response = requests.post(LLM_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]

    return f"Error: {response.status_code} - {response.text}"
