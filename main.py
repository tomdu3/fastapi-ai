import os
from fastapi import FastAPI
from models import ChatRequest, ChatResponse
from ai.gemini import Gemini
from dotenv import load_dotenv
from auth.throttling import apply_rate_limit

# Load environment variables from .env file
load_dotenv()

# --- FastAPI Application Setup ---
app = FastAPI()


# --- AI Configuration ---
def load_system_prompt():
    try:
        with open("prompts/system_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Create an instance of the Gemini AI platform
ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)


# --- API Routes ---
@app.get("/")
async def read_root():
    return {"message": "Api is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    apply_rate_limit("global_unauthenticated_user")
    response_text = ai_platform.chat(request.prompt)
    if not response_text:
        response_text = "No response generated."
    elif response_text.startswith("Error:"):
        response_text = "An error occurred while generating the response."
    elif response_text.startswith("Warning:"):
        response_text = "A warning was issued during response generation."
    else:
        response_text = response_text.strip()
    # Return the response wrapped in ChatResponse model
    return ChatResponse(response=response_text)