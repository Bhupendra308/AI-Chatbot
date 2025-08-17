# AI-Powered Chatbot with FastAPI & MySQL

## Features:
- Contextual AI chatbot using Huggingface DialoGPT
- FastAPI backend with REST API
- MySQL database to store chat logs

## Run Steps:
1. Set MySQL credentials in `db_config.py`
2. Create database using provided SQL
3. Install Python dependencies
4. Run server with Uvicorn

## API Endpoint:
POST /chat  
Body: `{ "message": "Your message here" }`
