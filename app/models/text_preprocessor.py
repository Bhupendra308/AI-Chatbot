import json
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# ------------------ BASE PATHS ------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_FILE = os.path.join(BASE_DIR, "data", "intents.json")

MAX_SEQ_LEN = 20  # Same as in training

# ------------------ LOAD INTENTS ------------------
def load_data():
    """Load intents.json as a Python dictionary."""
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)  # ✅ parse JSON, not just read string
    return data

# ------------------ PREPROCESS INTENTS ------------------
def preprocess_data():
    """
    Preprocess intents data for training and runtime usage:
    - Tokenization
    - Padding
    - Label encoding
    - Mapping tags to responses
    """
    data = load_data()  # Load JSON dict
    sentences = []
    labels = []
    responses = {}

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            sentences.append(pattern)
            labels.append(intent["tag"])
        responses[intent["tag"]] = intent["responses"]

    # Tokenizer
    tokenizer = Tokenizer(num_words=2000, oov_token="<OOV>")
    tokenizer.fit_on_texts(sentences)
    sequences = tokenizer.texts_to_sequences(sentences)
    padded_sequences = pad_sequences(sequences, truncating="post", maxlen=MAX_SEQ_LEN)

    # Label Encoder
    lbl_encoder = LabelEncoder()
    lbl_encoder.fit(labels)
    encoded_labels = lbl_encoder.transform(labels)

    return padded_sequences, encoded_labels, tokenizer, lbl_encoder, responses

# ------------------ PREPROCESS USER INPUT ------------------
def preprocess_text(text):
    """
    Preprocess a single user message for runtime prediction:
    - lowercase
    - strip whitespace
    """
    return text.lower().strip()
