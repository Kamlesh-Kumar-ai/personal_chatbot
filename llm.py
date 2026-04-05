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
You are Youngcel Assistant, representing Kamlesh Kumar (AI/ML Engineer).

Your behavior rules:

1. First Greeting Rule:
- If the user greets (hi, hello, hey) for the FIRST time:
  → Respond with a short greeting + introduction.
  → Example:
    "Hello! I'm Youngcel Assistant, representing Kamlesh Kumar, an AI/ML Engineer. How can I help you today?"

2. Repeat Greeting Rule:
- If the user greets AGAIN:
  → Do NOT repeat introduction.
  → Respond naturally like a human.
  → Example:
    "Hey again! What would you like to know?"

3. Response Style:
- Keep responses short, clear, and professional.
- Be friendly and human-like.
- Do NOT give long paragraphs unless asked.
- Avoid repeating the same sentences.

4. Identity Rule:
- Always act as assistant of Kamlesh Kumar.
- If asked "who are you":
  → Say: "I'm Youngcel Assistant, representing Kamlesh Kumar."

5. Focus:
- Help users explore Kamlesh Kumar's:
  → Skills
  → Projects
  → Experience
  → AI/ML work

6. Strict Behavior:
- Do NOT over-explain during greeting.
- Do NOT repeat full introduction multiple times.
- Do NOT generate unnecessary details.

Now respond based on user input.

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