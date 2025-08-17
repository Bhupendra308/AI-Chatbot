from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.db_config import get_db_connection
from app.models.chatbot_model import generate_response  # updated model
from app.models.text_preprocessor import preprocess_text
from app.session_manager import get_session_history, update_session_history
import random

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found."}

# Chat request schema
class ChatRequest(BaseModel):
    session_id: str = None  # Optional
    message: str
    teach_response: str = None  # Optional user-taught answer

@app.post("/chat")
def chat(chat_request: ChatRequest):
    # Assign or generate session_id
    session_id = chat_request.session_id
    if not session_id:
        session_id = f"session_{random.randint(1000,9999)}"

    user_message = preprocess_text(chat_request.message)

    # Retrieve chat history for multi-turn context
    chat_history = get_session_history(session_id)

    # Generate AI response
    response = generate_response(user_message, session_id=session_id)

    # Update session history
    update_session_history(session_id, user_message, response)

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Handle user teaching a new response
    if chat_request.teach_response:
        cursor.execute(
            "INSERT INTO chats (session_id, user_message, bot_response, timestamp, learned) VALUES (%s, %s, %s, %s, %s)",
            (session_id, user_message, chat_request.teach_response, datetime.datetime.now(), 1)
        )
        conn.commit()
        conn.close()
        return {"response": f"Got it! I learned: {chat_request.teach_response}", "session_id": session_id}

    # Normal conversation logging
    cursor.execute(
        "INSERT INTO chats (session_id, user_message, bot_response, timestamp) VALUES (%s, %s, %s, %s)",
        (session_id, user_message, response, datetime.datetime.now())
    )
    conn.commit()
    conn.close()

    return {
        "response": response,
        "session_id": session_id,
        "history": chat_history + [{"user": user_message, "bot": response}]
    }
