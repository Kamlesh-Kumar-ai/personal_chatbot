from fastapi import FastAPI
from search import search_docs
from llm import generate_answer

app = FastAPI()

chat_memory = {}

@app.get("/ask")
def ask(query: str, session_id: str = "default"):
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