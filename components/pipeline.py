from typing import Dict, Any, AsyncGenerator
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
        
    async def process_message(self, message_data: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """Process a message through the complete pipeline, yielding thinking steps."""
        try:
            # Phase 1: Understanding the Input
            yield {
                "phase": "understanding",
                "thinking": "Understanding the message and extracting key insights...",
                "status": "in_progress"
            }
            
            # 1. Extract insights from the message
            insights = await self.listener.process(message_data)
            
            yield {
                "phase": "understanding",
                "thinking": "Extracted key insights about people, topics, and context",
                "status": "complete",
                "details": {
                    "insights": insights
                }
            }

            # Phase 2: Building Context
            yield {
                "phase": "context",
                "thinking": "Building comprehensive context from past interactions...",
                "status": "in_progress"
            }
            
            # 2. Save insights and fetch context
            context = await self.fetcher.process(message_data, insights)
            
            yield {
                "phase": "context",
                "thinking": "Retrieved user profile, interests, and relevant history",
                "status": "complete",
                "details": {
                    "context_elements": [
                        "User profile",
                        "Communication preferences",
                        "Past interactions",
                        "Shared interests"
                    ]
                }
            }

            # Phase 3: Generating Response
            yield {
                "phase": "generation",
                "thinking": "Crafting initial response based on context...",
                "status": "in_progress"
            }
            
            # 3. Generate initial response
            initial_response = await self.generator.process(message_data, context)
            
            yield {
                "phase": "generation",
                "thinking": "Generated contextually-aware response",
                "status": "complete",
                "details": {
                    "response_length": len(initial_response),
                    "includes_context": True
                }
            }

            # Phase 4: Style Adjustment
            yield {
                "phase": "adjustment",
                "thinking": "Adjusting response style to match user preferences...",
                "status": "in_progress"
            }
            
            # 4. Adjust response style
            adjustment_data = {
                "content": initial_response,
                "chat_id": message_data.get("chat_id", ""),
                "user_id": message_data.get("user_id", ""),
                "message_history": message_data.get("message_history", []),
                "system_prompt": message_data.get("system_prompt")
            }
            
            # Stream adjustment thinking steps
            adjusted_response = await self.adjustor.process(adjustment_data, context)
            
            yield {
                "phase": "adjustment",
                "thinking": "Completed style adjustment",
                "status": "complete",
                "details": {
                    "preserved_elements": [
                        "Core message",
                        "Context relevance",
                        "Engagement aspects"
                    ]
                }
            }

            # Create final response object
            response = {
                "status": "success",
                "assistant_message": {
                    "id": message_data.get("message_id", ""),
                    "role": "assistant",
                    "content": adjusted_response,
                    "created_at": datetime.now().isoformat(),
                    "chat_id": message_data.get("chat_id", "")
                },
                "insights": insights
            }
            
            yield {
                "phase": "complete",
                "thinking": "Response ready for delivery",
                "status": "complete",
                "response": response
            }
            
        except Exception as e:
            yield {
                "phase": "error",
                "thinking": f"Error in message processing: {str(e)}",
                "status": "error",
                "details": {
                    "error": str(e),
                    "phase": "message_processing"
                }
            } 