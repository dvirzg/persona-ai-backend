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
    """Pretty print a step's input/output"""
    print("\n" + "="*50)
    print(f"STEP: {step_name}")
    print("="*50)
    print(json.dumps(data, indent=2, default=str))

async def test_pipeline():
    """Test the message processing pipeline with detailed logging"""
    print("\nInitializing test...")
    
    # Create database connection
    db_url = os.getenv("DATABASE_URL")
    print(f"\nConnecting to database: {db_url}")
    pool = await asyncpg.create_pool(db_url)
    
    # Initialize pipeline
    api_key = os.getenv("OPENAI_API_KEY")
    pipeline = MessageProcessingPipeline(pool, api_key)
    
    # Get test user ID
    async with pool.acquire() as conn:
        test_user_id = await conn.fetchval("SELECT id FROM users WHERE email = 'test@example.com'")
        if not test_user_id:
            raise ValueError("Test user not found. Please run migrations first.")
    
    # Generate a test chat ID
    test_chat_id = str(uuid.uuid4())
    
    # Test message data
    message_data = {
        "content": "I had a great conversation with Sarah about machine learning yesterday. She's really passionate about AI ethics.",
        "chat_id": test_chat_id,
        "user_id": test_user_id,
        "message_history": [],
        "system_prompt": None
    }
    
    try:
        # Step 1: Extract insights using ListeningIdentifier
        print("\nStep 1: Extracting insights...")
        insights = await pipeline.listener.process(message_data)
        await print_step("Insights Extraction", {
            "input": message_data["content"],
            "extracted_insights": insights
        })
        
        # Step 2: Save insights and fetch context
        print("\nStep 2: Saving insights and fetching context...")
        context = await pipeline.fetcher.process(message_data, insights)
        await print_step("Context Generation", {
            "insights_saved": insights,
            "retrieved_context": context
        })
        
        # Step 3: Generate initial response
        print("\nStep 3: Generating initial response...")
        initial_response = await pipeline.generator.process(message_data, context)
        await print_step("Initial Response", {
            "context_used": context,
            "generated_response": initial_response
        })
        
        # Step 4: Adjust response style
        print("\nStep 4: Adjusting response style...")
        adjustment_data = {
            "content": initial_response,
            "role": "assistant",  # Indicate this is an AI response
            "chat_id": test_chat_id
        }
        final_response = await pipeline.adjustor.process(adjustment_data, context)
        await print_step("Final Response", {
            "initial_response": initial_response,
            "adjusted_response": final_response
        })
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        raise
    finally:
        await pool.close()

if __name__ == "__main__":
    asyncio.run(test_pipeline()) 