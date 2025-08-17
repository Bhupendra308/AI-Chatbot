# AI Chatbot Project

## Overview
This project is an AI-powered chatbot that supports multi-turn conversations, dynamic learning from users, and fallback to Hugging Face API when needed. The chatbot is trained using a custom intent model with TensorFlow and stores user interactions in MySQL.  

It supports:
- Greeting, goodbye, thanks, and custom queries.
- Customer support simulation.
- Learning from user-provided answers.
- Multi-turn context using in-memory session management.

---

## Features
- **Intent-based responses** using a trained TensorFlow model.
- **Database learning**: Chatbot can learn new responses dynamically.
- **Fallback AI**: Hugging Face BlenderBot integration for general queries.
- **Session management**: Maintains conversation context across messages.
- **Frontend-ready**: FastAPI serves a static HTML frontend.

---

## Project Structure
ai_chatbot/
│
├── app/
│ ├── main.py # FastAPI entry point
│ ├── db_config.py # MySQL connection setup
│ ├── session_manager.py # Multi-turn session management
│ ├── models/
│ │ ├── chatbot_model.py # AI model integration & response generation
│ │ └── text_preprocessor.py
│ └── data/
│ └── intents.json # Training data
│
├── trained_model/
│ ├── chatbot_model.h5
│ ├── tokenizer.pickle
│ └── label_encoder.pickle
│
├── static/
│ └── index.html # Frontend HTML
│
├── requirements.txt
└── README.md


---

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ai_chatbot

2. **Create a virtual environment**
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3. **Install dependencies**
pip install -r requirements.txt

4. **Setup .env (Optional but recommended)**
HF_API_TOKEN=your_huggingface_token
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=chatbot_db

Usage
1. **Run the FastAPI server**

uvicorn app.main:app --reload

2. **Open the frontend**
Go to http://127.0.0.1:8000

3. **Chat**

Use the session ID to keep context.

Type queries, ask questions, or teach new responses.