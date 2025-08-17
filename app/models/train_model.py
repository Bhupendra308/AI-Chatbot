import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import pickle
from text_preprocessor import load_data, preprocess_data

# Get base directory (project root = ai_chatbot)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRAINED_MODEL_DIR = os.path.join(BASE_DIR, "trained_model")

# Ensure trained_model directory exists
os.makedirs(TRAINED_MODEL_DIR, exist_ok=True)

# Load and preprocess data
data = load_data()
X, y, tokenizer, lbl_encoder, responses = preprocess_data(data)

# Build model
model = Sequential()
model.add(Embedding(input_dim=2000, output_dim=64, input_length=20))
model.add(LSTM(64, return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(32))
model.add(Dense(32, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(set(y)), activation="softmax"))

# Compile
model.compile(loss="sparse_categorical_crossentropy",
              optimizer=Adam(learning_rate=0.001),
              metrics=["accuracy"])

# Train
model.fit(X, np.array(y), epochs=200, batch_size=8, verbose=1)

# Save model
model.save(os.path.join(TRAINED_MODEL_DIR, "chatbot_model.h5"))

# Save tokenizer and label encoder
with open(os.path.join(TRAINED_MODEL_DIR, "tokenizer.pickle"), "wb") as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.join(TRAINED_MODEL_DIR, "label_encoder.pickle"), "wb") as efile:
    pickle.dump(lbl_encoder, efile, protocol=pickle.HIGHEST_PROTOCOL)

print("✅ Model trained and saved successfully in 'trained_model/' folder!")
