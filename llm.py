import os
import requests
from dotenv import load_dotenv

# Load env
load_dotenv()

USE_GEMINI = os.getenv(
    "USE_GEMINI",
    "false"
).lower() == "true"

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

# Ollama Config
OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gemma3:4b"
)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

# Load Gemini only if needed
if USE_GEMINI and GEMINI_API_KEY:
    import google.generativeai as genai

    genai.configure(
        api_key=GEMINI_API_KEY
    )

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )


SYSTEM_PROMPT = """
You are Youngcel Assistant, Kamlesh Kumar's personal assistant (AI/ML Engineer).

Your behavior rules:

1. First Greeting Rule:
- If the user greets (hi, hello, hey) for the FIRST time:
  → Respond with a short greeting + introduction.

2. Repeat Greeting Rule:
- If the user greets AGAIN:
  → Do NOT repeat introduction.
  → Respond naturally like a human.

3. Response Style:
- Keep responses short, clear, and professional.
- Be friendly and human-like.
- Do NOT give long paragraphs unless asked.
- Avoid repeating the same sentences.

4. Identity Rule:
- Always act as assistant of Kamlesh Kumar.
- If asked "who are you":
  → Say:
  "I'm Youngcel Assistant, representing Kamlesh Kumar."

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
        history_text += (
            f"User: {h['user']}\n"
            f"Assistant: {h['assistant']}\n"
        )

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{history_text}

User already introduced:
{"YES" if introduced else "NO"}

Context:
{context}

User Query:
{query}

Answer:
"""

    return prompt


# Gemini Function
def gemini_generate(prompt):

    response = model.generate_content(
        prompt
    )

    return response.text


# Ollama Function
def ollama_generate(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]


# MAIN FUNCTION
def generate_answer(
    query,
    docs,
    history,
    introduced
):

    prompt = build_prompt(
        query,
        docs,
        history,
        introduced
    )

    try:

        # Use Gemini if enabled
        if USE_GEMINI and GEMINI_API_KEY:
            return gemini_generate(prompt)

        # Otherwise use Ollama
        return ollama_generate(prompt)

    except Exception as e:

        print(
            f"⚠️ Primary model failed: {e}"
        )

        # Fallback to Ollama
        try:
            return ollama_generate(prompt)

        except Exception as ollama_error:

            print(
                f"⚠️ Ollama failed: {ollama_error}"
            )

            return (
                "Sorry, I am temporarily unavailable."
            )