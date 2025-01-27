import asyncio
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from components.pipeline import MessageProcessingPipeline
import asyncpg
import uuid

# Load environment variables
load_dotenv()

async def print_step(step_name: str, data: dict):
    """Format step output in a frontend-friendly, collapsible structure"""
    # Header section (always visible)
    print("\n" + "="*50)
    print(f"▶ {step_name} {'.'*(40-len(step_name))} {data.get('status', 'IN_PROGRESS')}")
    print("="*50)
    
    # Detailed thinking section (collapsible in frontend)
    print("📝 Thinking Process:")
    print(json.dumps({
        "main_thought": data.get("thinking", "Processing..."),
        "details": {
            k: v for k, v in data.items() 
            if k not in ["thinking", "status", "response"]
        }
    }, indent=2, default=str))
    
    # Results section if available
    if "response" in data:
        print("\n🎯 Final Results:")
        print(json.dumps(data["response"], indent=2, default=str))

async def test_pipeline():
    """Test the message processing pipeline with narrative output."""
    print("\n🚀 Initializing test pipeline...")
    
    # Initialize database connection
    db_pool = await asyncpg.create_pool(
        os.getenv("DATABASE_URL"),
        ssl="require"
    )
    
    try:
        # Get test user
        async with db_pool.acquire() as conn:
            test_user = await conn.fetchrow(
                "SELECT id, name FROM users WHERE email = 'test@example.com'"
            )
            if not test_user:
                raise ValueError("Test user not found. Please run migrations first.")
        
        print(f"\n👤 Found test user: {test_user['name']}")
        
        # Initialize pipeline
        pipeline = MessageProcessingPipeline(db_pool, os.getenv("OPENAI_API_KEY"))
        
        # Test message data
        message_data = {
            "content": "I had an interesting conversation with Sarah yesterday about machine learning. She's really passionate about AI ethics.",
            "chat_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "user_id": test_user['id']
        }
        
        print("\n⚙️ Processing message through pipeline...")
        
        async for step in pipeline.process_message(message_data):
            # Print step details using the print_step function
            await print_step(
                f"{step['phase']}", 
                {
                    "status": step["status"],
                    "thinking": step["thinking"],
                    **(step.get("details", {})),
                    **({"response": step["response"]} if "response" in step else {})
                }
            )
    
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
    
    finally:
        await db_pool.close()

if __name__ == "__main__":
    asyncio.run(test_pipeline()) 