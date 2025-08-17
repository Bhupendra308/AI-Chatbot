# **AI Chatbot Project**
An intelligent chatbot with dynamic learning and multi-turn conversation support.

---

## Overview
This project is an AI-powered chatbot that supports multi-turn conversations, dynamic learning from users, and a fallback to the Hugging Face API when a direct answer isn't available. The chatbot uses a custom intent model built with TensorFlow and stores user interactions and newly learned responses in a MySQL database.

The chatbot's core capabilities include:

* Responding to greetings, goodbyes, and various custom queries.

* Simulating a customer support agent.

* Learning new responses and information from user inputs.

* Maintaining conversation context through in-memory session management.

---

## Features
* **Intent-based Responses**: Utilizes a custom, trained TensorFlow model to understand user intent.

* **Dynamic Learning**: The chatbot can dynamically learn new questions and answers, storing them in a database for future use.

* **Fallback AI**: Integrates with the Hugging Face BlenderBot for general queries that the intent model cannot handle, ensuring a more fluid conversation.

* **Session Management**: A dedicated session manager maintains the conversational context over multiple messages.

* **Frontend Integration**: A FastAPI server is used to serve a simple, static HTML frontend, making the project easy to run and test.

---

## Project Structure
```text
ai_chatbot/
│
├── app/
│ ├── main.py             # FastAPI entry point for the application
│ ├── db_config.py        # Handles MySQL database connection setup
│ ├── session_manager.py  # Manages multi-turn conversation sessions
│ ├── models/
│ │ ├── chatbot_model.py  # Integrates the AI model and generates responses
│ │ └── text_preprocessor.py # Handles text cleaning and tokenization
│ └── data/
│   └── intents.json      # JSON file containing the training data
│
├── trained_model/
│ ├── chatbot_model.h5    # The trained TensorFlow model file
│ ├── tokenizer.pickle    # The tokenizer used for text preprocessing
│ └── label_encoder.pickle# The label encoder for intent classification
│
├── static/
│ └── index.html          # The simple static HTML frontend
│
├── requirements.txt      # List of project dependencies
└── README.md             # This file
```

---

## Installation

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd ai_chatbot
    ```

2.  **Create a virtual environment**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup `.env` (Optional but recommended)**
    Create a `.env` file in the root directory and add your credentials. This file is not included in version control for security.
    ```text
    HF_API_TOKEN=your_huggingface_token
    MYSQL_HOST=localhost
    MYSQL_USER=root
    MYSQL_PASSWORD=yourpassword
    MYSQL_DB=chatbot_db
    ```

---

## Usage

1.  **Run the FastAPI server**
    Start the application server using `uvicorn`. The `--reload` flag is useful for development as it automatically restarts the server on code changes.
    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Open the frontend**
    Once the server is running, open a web browser and navigate to the following URL to access the chatbot interface:
    ```
    [http://127.0.0.1:8000](http://127.0.0.1:8000)
    ```

3.  **Chat with the bot**
    You can now interact with the chatbot! The chatbot will automatically manage the session context to maintain a multi-turn conversation. Feel free to ask questions, type queries, or even teach the bot new responses.
