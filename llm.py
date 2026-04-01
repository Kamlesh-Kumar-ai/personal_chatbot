import os
import requests
from dotenv import load_dotenv

# Load env
load_dotenv()

USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load OpenAI only if needed
if USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key = GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-3-flash-preview")



SYSTEM_PROMPT = """
You are Youngcel Assistant of Kamlesh Kumar.

Rules:
- If user greets for the first time → greet + introduce yourself.
- If user greets again → do NOT repeat full introduction.
- Instead respond naturally and continue conversation.
- Be friendly, human-like, and conversational.
- Never repeat the same sentence again and again.
"""


def build_prompt(query, docs, history, introduced):
    context = "\n".join(docs)

    history_text = ""
    for h in history[-5:]:
        history_text += f"User: {h['user']}\nAssistant: {h['assistant']}\n"

    prompt = f"""
    {SYSTEM_PROMPT}

    Conversation History:
    {history_text}

    User already introduced: {"YES" if introduced else "NO"}

    Context:
    {context}

    User Query:
    {query}

    Answer:
    """

    return prompt


#  OpenAI function
def gemini_generate(prompt):
    response = model.generate_content(
       prompt
    )
    return response.text


#  Ollama function (your original)
def ollama_generate(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


#  MAIN FUNCTION (SMART SWITCH)
def generate_answer(query, docs, history, introduced):
    prompt = build_prompt(query, docs, history, introduced)

    try:
        # Try OpenAI first (if enabled)
        if USE_GEMINI and GEMINI_API_KEY:
            return gemini_generate(prompt)

        # fallback use Ollama
        return ollama_generate(prompt)

    except Exception as e:
        print("⚠️ GEMINI failed, fallback to Ollama:", e)
        return ollama_generate(prompt)