# backend/core/llm.py
import httpx
from typing import List

# --- CHANGE 1: Use the /api/chat endpoint ---
OLLAMA_API_URL = "http://localhost:11434/api/chat"

# The specific model you want to use
OLLAMA_MODEL = "casemate"

# --- CHANGE 2: The function now accepts a list of message dictionaries ---
async def get_ollama_response(history: List[dict]) -> str:
    """
    Sends the entire conversation history to the Ollama chat API.
    The 'casemate' model's built-in system prompt will be used automatically.
    """
    # --- CHANGE 3: The payload now uses the "messages" format ---
    payload = {
        "model": OLLAMA_MODEL,
        "messages": history, # Pass the whole conversation
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            # --- CHANGE 4: The response structure for /api/chat is different ---
            # The content is nested inside a "message" object.
            return response_data.get("message", {}).get("content", "Sorry, I couldn't generate a response.").strip()

    except httpx.RequestError as e:
        print(f"Error connecting to Ollama: {e}")
        return "Sorry, I am currently unable to connect to the AI model."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred while generating a response."