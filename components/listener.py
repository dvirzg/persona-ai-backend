from openai import AsyncOpenAI
import json

class ListeningIdentifier:
    def __init__(self, api_key):
        self.model = AsyncOpenAI(api_key=api_key)

    async def process(self, message):
        try:
            prompt = f"""Extract key insights from this message. Focus on identifying:

Message: {message}

Please extract and structure the following elements:
1. People mentioned (names and any context about them)
2. Topics discussed (specific subjects, technologies, concepts)
3. Interests demonstrated (what the speaker shows interest in)
4. Personality traits revealed (how the speaker expresses themselves)
5. Communication style shown (how they prefer to communicate)
6. Stories or experiences shared (any narratives or events)

Format the response as a JSON object with these exact keys:
{{
    "people": [{{ "name": "string", "context": "string" }}],
    "interests": [{{ "name": "string", "summary": "string" }}],
    "personality_traits": ["string"],
    "communication_style": {{ "key_aspects": ["string"] }},
    "stories": [{{
        "title": "string",
        "description": "string",
        "people": ["string"],
        "location": "string"
    }}]
}}

Extract only what is explicitly present or strongly implied in the message. Do not invent or assume details."""

            response = await self.model.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at extracting structured insights from conversations, focusing on people, interests, and communication patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # Low temperature for consistent, factual extraction
            )
            
            # Parse the response into structured data
            try:
                insights = json.loads(response.choices[0].message.content.strip())
                return insights
            except json.JSONDecodeError as e:
                print(f"Error parsing insights: {str(e)}")
                return {
                    "people": [],
                    "interests": [],
                    "personality_traits": [],
                    "communication_style": {"key_aspects": []},
                    "stories": []
                }
                
        except Exception as e:
            print(f"Error in insight extraction: {str(e)}")
            return {
                "people": [],
                "interests": [],
                "personality_traits": [],
                "communication_style": {"key_aspects": []},
                "stories": []
            } 