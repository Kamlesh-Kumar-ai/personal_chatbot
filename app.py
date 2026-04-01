from fastapi import FastAPI
from pydantic import BaseModel
from search import search_docs
from llm import generate_answer

app = FastAPI()

chat_memory = {}

#  Home endpoint
@app.get("/")
def home():
    return {"message": "Chatbot is live 🚀"}

#  Request body for POST
class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"

# Existing GET (fixed properly)
@app.get("/ask")
def ask(query: str = "", session_id: str = "default"):
    if not query:
        return {"error": "Please provide query parameter"}

    user_data = chat_memory.get(session_id, {
        "history": [],
        "introduced": False   
    })

    history = user_data["history"]
    introduced = user_data["introduced"]

    docs = search_docs(query)
    answer = generate_answer(query, docs, history, introduced)

    # Update state
    if "Youngcel Assistant" in answer:
        user_data["introduced"] = True

    history.append({"user": query, "assistant": answer})
    user_data["history"] = history

    chat_memory[session_id] = user_data

    return {
        "query": query,
        "answer": answer
    }

# POST version (same logic, no change)
@app.post("/ask")
def ask_post(data: ChatRequest):
    query = data.query
    session_id = data.session_id

    user_data = chat_memory.get(session_id, {
        "history": [],
        "introduced": False   
    })

    history = user_data["history"]
    introduced = user_data["introduced"]

    docs = search_docs(query)
    answer = generate_answer(query, docs, history, introduced)

    # Update state
    if "Youngcel Assistant" in answer:
        user_data["introduced"] = True

    history.append({"user": query, "assistant": answer})
    user_data["history"] = history

    chat_memory[session_id] = user_data

    return {
        "query": query,
        "answer": answer
    }