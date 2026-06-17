import chainlit as cl
from search import search_docs
from llm import generate_answer

# Session storage
chat_history = {}

@cl.on_chat_start
async def start():
    """Called when a new chat session starts"""
    session_id = cl.user_session.get("session_id")
    if not session_id:
        session_id = f"session_{cl.user_session.get('id')}"
        cl.user_session.set("session_id", session_id)
        chat_history[session_id] = {
            "history": [],
            "introduced": False
        }
    
    # Send welcome message
    await cl.Message(
        content="👋 Welcome! I'm **Youngcel Assistant**, Kamlesh Kumar's personal AI assistant. How can I help you today?",
        author="Youngcel Assistant"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    query = message.content
    session_id = cl.user_session.get("session_id")
    
    if session_id not in chat_history:
        chat_history[session_id] = {
            "history": [],
            "introduced": False
        }
    
    user_data = chat_history[session_id]
    history = user_data["history"]
    introduced = user_data["introduced"]
    
    # Search for relevant documents
    docs = search_docs(query)
    
    # Generate answer
    answer = generate_answer(query, docs, history, introduced)
    
    # Update introduction state
    if "Youngcel Assistant" in answer:
        user_data["introduced"] = True
    
    # Update chat history
    history.append({"user": query, "assistant": answer})
    user_data["history"] = history
    
    # Send response
    await cl.Message(
        content=answer,
        author="Youngcel Assistant"
    ).send()


if __name__ == "__main__":
    cl.run()
