from typing import Dict, Any, Optional
from openai import AsyncOpenAI
import json

class ResponseGenerator:
    def __init__(self, api_key: str):
        self.model = AsyncOpenAI(api_key=api_key)
        
    async def process(self, message_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate a response using the message and context."""
        
        # Create a context-aware system prompt
        system_prompt = self._create_system_prompt(context)
        
        # Format the conversation history
        messages = self._format_conversation_history(message_data)
        
        # Add the system prompt at the beginning
        messages.insert(0, {"role": "system", "content": system_prompt})
        
        try:
            response = await self.model.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in ResponseGenerator: {str(e)}")
            return "I apologize, but I encountered an error while processing your message. Could you please try again?"
    
    def _create_system_prompt(self, context: Dict[str, Any]) -> str:
        """Create a system prompt that incorporates user context."""
        
        # Get user profile information
        profile = context.get("profile", {})
        personality = profile.get("personality_traits", [])
        communication_style = profile.get("communication_style", "")
        
        # Get recent context
        interests = context.get("interests", [])
        people = context.get("people", [])
        stories = context.get("stories", [])
        
        # Build the context-aware prompt
        prompt_parts = [
            "You are a friendly and helpful AI assistant with access to the following context about the user:",
            
            # Add personality context if available
            f"Personality traits: {', '.join(personality)}" if personality else "",
            f"Communication style: {communication_style}" if communication_style else "",
            
            # Add interests
            "Recent interests: " + ", ".join(i["name"] for i in interests) if interests else "",
            
            # Add people context
            "Known people: " + ", ".join(f"{p['name']} ({p['relationship']})" for p in people) if people else "",
            
            # Add recent stories
            "Recent stories: " + ", ".join(s["title"] for s in stories) if stories else "",
            
            # Add behavioral instructions
            "Use this context to provide more personalized and relevant responses.",
            "Maintain a consistent tone matching their communication style.",
            "Reference relevant past interactions when appropriate.",
            "Be empathetic and understanding of their perspective."
        ]
        
        # Combine all parts, filtering out empty strings
        return "\n".join(part for part in prompt_parts if part)
    
    def _format_conversation_history(self, message_data: Dict[str, Any]) -> list:
        """Format the conversation history for the API call."""
        history = message_data.get("message_history", [])
        current_message = {
            "role": "user",
            "content": message_data["content"]
        }
        
        # Ensure we don't exceed token limits by taking recent messages
        return history[-5:] + [current_message]  # Keep last 5 messages + current 