# Simple in-memory session store
session_store = {}

def get_session_history(session_id):
    return session_store.get(session_id, [])

def update_session_history(session_id, user_input, bot_response):
    if session_id not in session_store:
        session_store[session_id] = []

    # Add latest user message and bot response as a pair
    session_store[session_id].append({
        "user": user_input,
        "bot": bot_response
    })

    # Keep only last 8 exchanges (16 messages total)
    if len(session_store[session_id]) > 8:
        session_store[session_id] = session_store[session_id][-2:]
