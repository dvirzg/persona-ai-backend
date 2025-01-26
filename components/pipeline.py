from typing import Dict, Any
import asyncpg
from datetime import datetime

from .listener import ListeningIdentifier
from .fetcher import FetcherAndSaver
from .generator import ResponseGenerator
from .adjustor import ResponseAdjustor

class MessageProcessingPipeline:
    def __init__(self, db_pool: asyncpg.Pool, api_key: str):
        self.db = db_pool
        self.listener = ListeningIdentifier(api_key)
        self.fetcher = FetcherAndSaver(db_pool)
        self.generator = ResponseGenerator(api_key)
        self.adjustor = ResponseAdjustor(api_key)
        
    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a message through the complete pipeline."""
        try:
            # 1. Extract insights from the message
            insights = await self.listener.process(message_data)
            
            # 2. Save insights and fetch context
            context = await self.fetcher.process(message_data, insights)
            
            # 3. Generate initial response
            initial_response = await self.generator.process(message_data, context)
            
            # 4. Adjust response style
            adjustment_data = {
                "content": initial_response,
                "chat_id": message_data.get("chat_id", ""),
                "user_id": message_data.get("user_id", ""),
                "message_history": message_data.get("message_history", []),
                "system_prompt": message_data.get("system_prompt")
            }
            final_response = await self.adjustor.process(adjustment_data, context)
            
            # Create response object
            response = {
                "status": "success",
                "assistant_message": {
                    "id": message_data.get("message_id", ""),  # Should be provided by caller
                    "role": "assistant",
                    "content": final_response,
                    "created_at": datetime.now().isoformat(),
                    "chat_id": message_data.get("chat_id", "")
                },
                "insights": insights  # Optionally include extracted insights
            }
            
            return response
            
        except Exception as e:
            print(f"Error in message processing pipeline: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            } 