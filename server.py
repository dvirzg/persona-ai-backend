from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
from components.pipeline import MessageProcessingPipeline
from typing import List, Optional
from routes import pipeline
import asyncpg

# Load environment variables
load_dotenv()

app = FastAPI()

# Include pipeline route
app.include_router(pipeline.router, prefix="/api")

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

# Database pool
db_pool = None

@app.on_event("startup")
async def startup():
    global db_pool
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL environment variable is not set")
    db_pool = await asyncpg.create_pool(database_url, ssl="require")

@app.on_event("shutdown")
async def shutdown():
    global db_pool
    if db_pool:
        await db_pool.close()

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
        # Initialize pipeline for this request
        pipeline = MessageProcessingPipeline(db_pool, os.getenv("OPENAI_API_KEY"))
        
        # Process message
        message_data = {
            "content": request_data.user_message,
            "chat_id": request_data.chat_id,
            "user_id": request_data.user_id,
            "message_history": request_data.message_history,
            "system_prompt": request_data.system_prompt
        }
        
        # Process through pipeline and get final result
        result = None
        async for step in pipeline.process_message(message_data):
            if step.get("phase") == "complete":
                result = step.get("response")
        
        if not result:
            raise HTTPException(status_code=500, detail="Pipeline did not produce a response")
            
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
        # Initialize pipeline for this request
        pipeline = MessageProcessingPipeline(db_pool, os.getenv("OPENAI_API_KEY"))
        
        # Use the generator component directly for title generation
        message_data = {
            "content": request_data["message"],
            "system_prompt": "Generate a short, descriptive title (2-6 words) for a chat that starts with this message."
        }
        
        initial_response = await pipeline.generator.process(message_data, {})
        return {"title": initial_response.strip('"').strip()}
        
    except Exception as e:
        print("Error generating title:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
