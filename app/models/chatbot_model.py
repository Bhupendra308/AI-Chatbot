import os
import random
import numpy as np
import pickle
import difflib
import requests
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from app.db_config import get_db_connection
from app.session_manager import get_session_history, update_session_history
import json

# ------------------ BASE PATHS ------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRAINED_MODEL_DIR = os.path.join(BASE_DIR, "trained_model")
DATA_DIR = os.path.join(BASE_DIR, "data")

# ------------------ LOAD MODEL ------------------
MODEL_PATH = os.path.join(TRAINED_MODEL_DIR, "chatbot_model.h5")
model = load_model(MODEL_PATH)

# ------------------ LOAD TOKENIZER & LABEL ENCODER ------------------
with open(os.path.join(TRAINED_MODEL_DIR, "tokenizer.pickle"), "rb") as handle:
    tokenizer = pickle.load(handle)

with open(os.path.join(TRAINED_MODEL_DIR, "label_encoder.pickle"), "rb") as efile:
    lbl_encoder = pickle.load(efile)

MAX_SEQ_LEN = 20  # Same as training

# ------------------ LOAD INTENTS ------------------
INTENTS_PATH = os.path.join(DATA_DIR, "intents.json")
with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    intents = json.load(f)

# ------------------ HUGGING FACE API ------------------
HF_API_TOKEN = "YOUR API KEY HERE"
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# ------------------ HELPER FUNCTIONS ------------------
def fetch_learned_response(user_input, threshold=0.6):
    """Fetch response from learned Q&A in database with fuzzy matching."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_message, bot_response FROM chats WHERE learned=1")
    learned_chats = cursor.fetchall()
    conn.close()

    best_score = 0
    best_response = None
    for chat in learned_chats:
        score = difflib.SequenceMatcher(None, user_input.lower(), chat["user_message"].lower()).ratio()
        if score > best_score:
            best_score = score
            best_response = chat["bot_response"]

    if best_score >= threshold:
        return best_response
    return None

def predict_intent(user_input):
    """Predict intent from trained model and return random response."""
    seq = tokenizer.texts_to_sequences([user_input])
    padded = pad_sequences(seq, truncating='post', maxlen=MAX_SEQ_LEN)
    result = model.predict(padded, verbose=0)
    intent_index = np.argmax(result)
    intent_tag = lbl_encoder.inverse_transform([intent_index])[0]

    for intent in intents["intents"]:
        if intent["tag"] == intent_tag:
            return random.choice(intent["responses"])
    return None

def query_huggingface(user_input):
    """Optional fallback using Hugging Face API."""
    try:
        payload = {"inputs": user_input}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"]
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
    except Exception as e:
        print("Hugging Face API error:", e)
    return None

# ------------------ MAIN HYBRID RESPONSE ------------------
def generate_response(user_input, session_id=None):
    """
    Hybrid response combining:
    1️⃣ Learned DB responses
    2️⃣ Trained model
    3️⃣ Optional Hugging Face API fallback
    4️⃣ Session-aware dynamic conversation
    """
    # Get recent conversation for context
    chat_history = get_session_history(session_id) if session_id else []

    # 1️⃣ Check learned responses
    learned = fetch_learned_response(user_input)
    if learned:
        if session_id:
            update_session_history(session_id, user_input, learned)
        return learned

    # 2️⃣ Use trained AI model
    model_resp = predict_intent(user_input)
    if model_resp:
        if session_id:
            update_session_history(session_id, user_input, model_resp)
        return model_resp

    # 3️⃣ Check for support escalation
    if any(word in user_input.lower() for word in ["manager", "supervisor", "human support"]):
        response = "I understand you need human assistance. My manager will help you shortly."
        if session_id:
            update_session_history(session_id, user_input, response)
        return response

    # 4️⃣ Fallback Hugging Face API
    hf_resp = query_huggingface(user_input)
    if hf_resp:
        if session_id:
            update_session_history(session_id, user_input, hf_resp)
        return hf_resp

    # 5️⃣ Dynamic fallback for alive conversation
    fallback_responses = [
        "Hmm, I’m thinking… can you give me more details?",
        "I hear you. Can you elaborate?",
        "Interesting… tell me more!",
        "I’m following you. What happened next?",
        "Could you clarify that for me?",
        "I’m listening, please continue."
    ]
    response = random.choice(fallback_responses)
    if session_id:
        update_session_history(session_id, user_input, response)
    return response
