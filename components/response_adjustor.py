from openai import AsyncOpenAI

class ResponseAdjustor:
    def __init__(self, api_key):
        self.model = AsyncOpenAI(api_key=api_key)

    async def process(self, message, context):
        try:
            # Extract message content and style preferences
            message_content = message.get("content", "") if isinstance(message, dict) else message
            style = context.get('profile', {}).get('communication_style', {})
            
            prompt = f"""Adjust this AI response to match the user's communication style while maintaining the AI's perspective.

AI Response to Adjust: {message_content}

User's Communication Style: {style}

Instructions:
1. Keep the AI's perspective (third-person)
2. Maintain all key information and intent
3. Adjust vocabulary and tone to match user's style
4. Keep engagement elements (questions, examples)
5. Make it feel natural and conversational

Adjust the response now."""

            response = await self.model.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You adjust AI responses to match user communication styles while preserving content and the AI's perspective."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error in style adjustment: {str(e)}")
            return message_content  # Return original if adjustment fails 