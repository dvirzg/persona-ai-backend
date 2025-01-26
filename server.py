from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
import message_processor  # Changed to simple import
from typing import List, Optional

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://persona-ai-git-main-dvir-zagury-grynbaums-projects.vercel.app",  # Vercel preview
        "https://persona-e9n3v7xkf-dvir-zagury-grynbaums-projects.vercel.app",  # Vercel preview
        "https://dvirzg.com",  # Custom domain
        "https://www.dvirzg.com"  # www subdomain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class MessageRequest(BaseModel):
    user_message: str = Field(..., description="The user's message")
    chat_id: str = Field(..., description="The chat ID")
    user_id: str = Field(..., description="The user's ID")
    message_history: List[dict] = Field(default_factory=list, description="Previous messages in the chat")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt")

# Security setup
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY", "your-secret-api-key")  # You'll set this in Railway
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Initialize message processor
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY is not set!")
message_processor_instance = message_processor.MessageProcessor(api_key=OPENAI_API_KEY)

# Add a root endpoint for health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

@app.post("/process-message")
async def process_message(
    request: Request,
    request_data: MessageRequest,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = message_processor_instance.process_message(
            user_message=request_data.user_message,
            chat_id=request_data.chat_id,
            user_id=request_data.user_id,
            message_history=request_data.message_history,
            system_prompt=request_data.system_prompt
        )
        return result
    except Exception as e:
        print("Error processing message:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-title")
async def generate_title(
    request: Request,
    request_data: dict,
    api_key: str = Depends(verify_api_key)
):
    try:
        title = message_processor_instance.generate_title(request_data.get("message"))
        return {"title": title}
    except Exception as e:
        print("Error generating title:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
