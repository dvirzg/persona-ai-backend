from typing import Dict, Any
from openai import AsyncOpenAI

class ResponseAdjustor:
    def __init__(self, api_key: str):
        self.model = AsyncOpenAI(api_key=api_key)
        
    async def process(self, message_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Adjust the response to match the user's communication style."""
        
        # Get the user's communication style
        style = context.get("profile", {}).get("communication_style", "")
        if not style:
            return message_data["content"]  # No adjustment needed
            
        system_prompt = f"""You are an AI trained to adjust message style while preserving meaning.
        
        The user's communication style is: {style}
        
        Adjust the following response to match this style, while keeping the core message intact.
        Be subtle in your adjustments - don't make dramatic changes unless the style difference is very significant.
        
        Original response:
        {message_data["content"]}
        
        Provide only the adjusted response, with no explanations or additional text."""
        
        try:
            response = await self.model.chat.completions.create(
                model="gpt-3.5-turbo",  # Using 3.5 for faster, lighter adjustments
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Please adjust this response."}
                ],
                temperature=0.7
            )
            
            # Return the adjusted response, not the input message
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error in ResponseAdjustor: {str(e)}")
            return message_data["content"]  # Return original response if adjustment fails 