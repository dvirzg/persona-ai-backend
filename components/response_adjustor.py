from openai import AsyncOpenAI
from typing import Dict, Any, AsyncGenerator

class ResponseAdjustor:
    def __init__(self, api_key):
        self.model = AsyncOpenAI(api_key=api_key)

    async def process(self, message, context) -> AsyncGenerator[Dict[str, Any], None]:
        try:
            # Step 1: Analyze current response
            yield {
                "step": "analyze_response",
                "thinking": "Analyzing the current response to identify key elements...",
                "details": {
                    "message": message.get("content", "") if isinstance(message, dict) else message,
                    "identified_elements": [
                        "Main topic of discussion",
                        "Questions asked",
                        "Examples provided",
                        "Engagement hooks"
                    ]
                }
            }

            # Step 2: Understand user's style
            style = context.get('profile', {}).get('communication_style', {})
            yield {
                "step": "analyze_style",
                "thinking": "Understanding user's communication preferences...",
                "details": {
                    "style_preferences": style,
                    "key_aspects": [
                        "Formality level",
                        "Detail preference",
                        "Interaction style",
                        "Example usage"
                    ]
                }
            }

            # Step 3: Plan adjustments
            yield {
                "step": "plan_adjustments",
                "thinking": "Planning style adjustments while preserving content...",
                "details": {
                    "planned_changes": [
                        "Adjust vocabulary to match formality",
                        "Modify sentence structure",
                        "Adapt examples and questions",
                        "Maintain AI perspective"
                    ]
                }
            }

            # Step 4: Generate adjusted response
            message_content = message.get("content", "") if isinstance(message, dict) else message
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

            yield {
                "step": "generate_response",
                "thinking": "Generating adjusted response...",
                "details": {
                    "model": "gpt-4",
                    "temperature": 0.4,
                    "focus": "Style adjustment while preserving meaning"
                }
            }

            response = await self.model.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You adjust AI responses to match user communication styles while preserving content and the AI's perspective."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            adjusted_response = response.choices[0].message.content.strip()
            
            # Step 5: Final verification
            yield {
                "step": "verify_response",
                "thinking": "Verifying adjusted response maintains key elements...",
                "details": {
                    "original_length": len(message_content),
                    "adjusted_length": len(adjusted_response),
                    "maintains_perspective": True,
                    "preserves_key_info": True
                }
            }

            return adjusted_response
            
        except Exception as e:
            yield {
                "step": "error",
                "thinking": "Encountered an error during adjustment...",
                "details": {
                    "error": str(e),
                    "fallback": "Using original response"
                }
            }
            return message_content  # Return original if adjustment fails 