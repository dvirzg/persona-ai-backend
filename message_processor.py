from typing import List, Dict, Optional, Union, Any
import os
from dataclasses import dataclass, asdict
from openai import OpenAI
from datetime import datetime
import asyncpg
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from components.pipeline import MessageProcessingPipeline

@dataclass
class Message:
    id: str
    role: str
    content: str
    created_at: datetime
    chat_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "chat_id": self.chat_id
        }

@dataclass
class Chat:
    id: str
    user_id: str
    title: str
    created_at: datetime

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
async def get_db_pool():
    if not hasattr(app.state, "db_pool"):
        db_url = os.getenv("DATABASE_URL")
        print(f"Connecting to database with URL: {db_url}")
        app.state.db_pool = await asyncpg.create_pool(
            db_url,
            min_size=1,
            max_size=10
        )
    return app.state.db_pool

# Initialize pipeline
async def get_pipeline(db_pool: asyncpg.Pool = Depends(get_db_pool)):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    return MessageProcessingPipeline(db_pool, api_key)

# Request models
class MessageRequest(BaseModel):
    user_message: str
    chat_id: str
    user_id: str
    message_history: Optional[list] = None
    system_prompt: Optional[str] = None

@app.post("/process-message")
async def process_message(
    request: MessageRequest,
    pipeline: MessageProcessingPipeline = Depends(get_pipeline)
):
    """Process a message through the AI pipeline."""
    try:
        # Format message data
        message_data = {
            "content": request.user_message,
            "chat_id": request.chat_id,
            "user_id": request.user_id,
            "message_history": request.message_history or [],
            "system_prompt": request.system_prompt
        }
        
        # Process through pipeline
        result = await pipeline.process_message(message_data)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-title")
async def generate_title(
    request: dict,
    pipeline: MessageProcessingPipeline = Depends(get_pipeline)
):
    """Generate a title for a new chat."""
    try:
        # Use the generator component directly for title generation
        message_data = {
            "content": request["message"],
            "system_prompt": "Generate a short, descriptive title (2-6 words) for a chat that starts with this message."
        }
        
        response = await pipeline.generator.process(message_data, {})
        
        return {
            "title": response.strip('"').strip()  # Remove any quotes from the title
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Startup event
@app.on_event("startup")
async def startup():
    # Initialize database pool
    await get_db_pool()

# Shutdown event
@app.on_event("shutdown")
async def shutdown():
    if hasattr(app.state, "db_pool"):
        await app.state.db_pool.close()

def generate_uuid() -> str:
    """Generate a UUID for messages"""
    import uuid
    return str(uuid.uuid4()) 