from fastapi import APIRouter, WebSocket
from components.pipeline import MessageProcessingPipeline
import json
import os
from dotenv import load_dotenv
import asyncpg
from typing import Dict, Any

# Load environment variables
load_dotenv()

router = APIRouter()

@router.websocket("/ws/pipeline")
async def pipeline_websocket(websocket: WebSocket):
    await websocket.accept()
    
    # Initialize database connection with explicit environment variables
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        await websocket.send_json({
            "error": "DATABASE_URL environment variable is not set"
        })
        await websocket.close()
        return
        
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        await websocket.send_json({
            "error": "OPENAI_API_KEY environment variable is not set"
        })
        await websocket.close()
        return
    
    db_pool = await asyncpg.create_pool(
        database_url,
        ssl="require"
    )
    
    try:
        # Initialize pipeline with explicit API key
        pipeline = MessageProcessingPipeline(db_pool, openai_api_key)
        
        while True:
            # Wait for message data from frontend
            message_data = await websocket.receive_json()
            
            # Process message through pipeline
            async for step in pipeline.process_message(message_data):
                # Send step data to frontend
                await websocket.send_json({
                    "phase": step["phase"],
                    "status": step["status"],
                    "thinking": step["thinking"],
                    "details": step.get("details", {}),
                    **({"response": step["response"]} if "response" in step else {})
                })
    
    except Exception as e:
        await websocket.send_json({
            "error": str(e)
        })
    
    finally:
        await db_pool.close()
        await websocket.close() 