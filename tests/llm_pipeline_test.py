import os
import json
import asyncio
import asyncpg
from datetime import datetime
from typing import Dict, Any, List
from openai import AsyncOpenAI
from dotenv import load_dotenv
from uuid import UUID

# Load environment variables
load_dotenv()

# Custom JSON encoder to handle UUIDs and other special types
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class ExperimentalListener:
    """Experimental version of ListeningIdentifier for testing different prompts and strategies."""
    def __init__(self, client: AsyncOpenAI):
        self.client = client
    
    async def process(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a message to extract key insights."""
        system_prompt = """
        You are an expert at understanding user messages and extracting key insights.
        Analyze the message to identify:
        1. Main topics and themes
        2. Mentioned people and relationships
        3. Emotional undertones
        4. Technical concepts
        5. Questions or requests
        
        Return your analysis in a structured JSON format.
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

class ExperimentalFetcher:
    """Experimental version of FetcherAndSaver for testing different context building strategies."""
    def __init__(self, persona_data: Dict[str, Any]):
        self.persona_data = persona_data
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        return text.lower().strip()
    
    def _texts_match(self, text1: str, text2: str) -> bool:
        """Check if two texts match, handling partial matches."""
        text1 = self._normalize_text(text1)
        text2 = self._normalize_text(text2)
        return text1 in text2 or text2 in text1
    
    async def process(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Build context based on message insights and persona data."""
        context = {
            "profile": self.persona_data["profile"],
            "relevant_interests": [],
            "relevant_people": [],
            "relevant_stories": []
        }
        
        # Extract all possible topics and concepts
        topics = []
        if "Main topics and themes" in insights:
            topics.extend(insights["Main topics and themes"])
        if "Technical concepts" in insights:
            topics.extend(insights["Technical concepts"])
        topics = [self._normalize_text(topic) for topic in topics]
        
        # Extract mentioned people
        mentioned_people = []
        if "Mentioned people and relationships" in insights:
            mentioned_people = list(insights["Mentioned people and relationships"].keys())
        mentioned_people = [self._normalize_text(name) for name in mentioned_people]
        
        # Match interests
        for interest in self.persona_data["interests"]:
            interest_name = self._normalize_text(interest["name"])
            interest_summary = self._normalize_text(interest["summary"])
            
            if any(topic for topic in topics if 
                  self._texts_match(topic, interest_name) or 
                  self._texts_match(topic, interest_summary)):
                context["relevant_interests"].append(interest)
        
        # Match people
        for person in self.persona_data["people"]:
            person_name = self._normalize_text(person["name"])
            
            if any(name for name in mentioned_people if self._texts_match(name, person_name)):
                context["relevant_people"].append(person)
                
                # Also add any stories involving this person
                for story in self.persona_data["stories"]:
                    if self._texts_match(person_name, story["description"]):
                        if story not in context["relevant_stories"]:
                            context["relevant_stories"].append(story)
        
        # Match stories by topic
        for story in self.persona_data["stories"]:
            story_text = f"{story['title']} {story['description']}"
            story_text = self._normalize_text(story_text)
            
            if any(topic for topic in topics if self._texts_match(topic, story_text)):
                if story not in context["relevant_stories"]:
                    context["relevant_stories"].append(story)
            
            # Also match by tags if available
            if "tags" in story:
                story_tags = [self._normalize_text(tag) for tag in story["tags"]]
                if any(topic for topic in topics for tag in story_tags if self._texts_match(topic, tag)):
                    if story not in context["relevant_stories"]:
                        context["relevant_stories"].append(story)
        
        return context

class ExperimentalGenerator:
    """Experimental version of ResponseGenerator for testing different generation strategies."""
    def __init__(self, client: AsyncOpenAI):
        self.client = client
    
    async def process(self, message: str, context: Dict[str, Any]) -> str:
        """Generate a response based on the message and context."""
        system_prompt = f"""
        You are an AI assistant helping with technical discussions. 
        Use the following context to inform your response:
        
        User Profile:
        {json.dumps(context['profile'], indent=2, cls=CustomJSONEncoder)}
        
        Relevant Interests:
        {json.dumps(context['relevant_interests'], indent=2, cls=CustomJSONEncoder)}
        
        Relevant People:
        {json.dumps(context['relevant_people'], indent=2, cls=CustomJSONEncoder)}
        
        Relevant Stories:
        {json.dumps(context['relevant_stories'], indent=2, cls=CustomJSONEncoder)}
        
        Generate a response that:
        1. Addresses the user's question or concern
        2. Leverages relevant context from their profile and interests
        3. References relevant past experiences or discussions if applicable
        4. Maintains appropriate technical depth and formality
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        
        return response.choices[0].message.content

class ExperimentalAdjustor:
    """Experimental version of ResponseAdjustor for testing different adjustment strategies."""
    def __init__(self, client: AsyncOpenAI):
        self.client = client
    
    async def process(self, response: str, context: Dict[str, Any]) -> str:
        """Adjust response based on user's communication preferences."""
        system_prompt = f"""
        Adjust the following response according to these communication preferences:
        {json.dumps(context['profile']['communication_style'], indent=2, cls=CustomJSONEncoder)}
        
        Maintain the core message while adapting:
        1. Length and detail level
        2. Technical depth
        3. Tone and formality
        4. Structure and organization
        """
        
        completion = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": response}
            ]
        )
        
        return completion.choices[0].message.content

async def get_test_persona(pool: asyncpg.Pool):
    """Fetch Sophie Martinez's complete profile with interests and social circle."""
    async with pool.acquire() as conn:
        # Get user profile
        user = await conn.fetchrow(
            """
            SELECT id, name, personality_traits, communication_style, demographic
            FROM users
            WHERE email = 'sophie.m@example.com'
            """
        )
        
        if not user:
            raise ValueError("Test user 'sophie.m@example.com' not found in database")
        
        # Parse JSON strings in user data
        user_dict = dict(user)
        for field in ['personality_traits', 'communication_style', 'demographic']:
            if field in user_dict and isinstance(user_dict[field], str):
                try:
                    user_dict[field] = json.loads(user_dict[field])
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse JSON in {field}")
        
        # Get interests
        interests = await conn.fetch(
            """
            SELECT name, summary
            FROM interests
            WHERE user_id = $1
            """,
            user['id']
        )
        
        # Get social circle
        people = await conn.fetch(
            """
            SELECT name, relationship, demographic, notes
            FROM people
            WHERE user_id = $1
            """,
            user['id']
        )
        
        # Parse JSON in people data
        people_list = []
        for person in people:
            person_dict = dict(person)
            if 'demographic' in person_dict and isinstance(person_dict['demographic'], str):
                try:
                    person_dict['demographic'] = json.loads(person_dict['demographic'])
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse JSON in demographic for {person_dict['name']}")
            people_list.append(person_dict)
        
        # Get stories
        stories = await conn.fetch(
            """
            SELECT title, description, location, timestamp, tags
            FROM stories
            WHERE user_id = $1
            ORDER BY timestamp DESC
            """,
            user['id']
        )
        
        return {
            "profile": user_dict,
            "interests": [dict(i) for i in interests],
            "people": people_list,
            "stories": [dict(s) for s in stories]
        }

async def process_test_message(message: str, persona_data: Dict[str, Any], client: AsyncOpenAI):
    """Process a test message through our experimental pipeline."""
    try:
        # Initialize components
        listener = ExperimentalListener(client)
        fetcher = ExperimentalFetcher(persona_data)
        generator = ExperimentalGenerator(client)
        adjustor = ExperimentalAdjustor(client)
        
        print("\n1. Extracting Insights...")
        insights = await listener.process(message)
        print(json.dumps(insights, indent=2, cls=CustomJSONEncoder))
        
        print("\n2. Building Context...")
        context = await fetcher.process(insights)
        print(json.dumps(context, indent=2, cls=CustomJSONEncoder))
        
        print("\n3. Generating Initial Response...")
        initial_response = await generator.process(message, context)
        print(initial_response)
        
        print("\n4. Adjusting Response...")
        adjusted_response = await adjustor.process(initial_response, context)
        print(adjusted_response)
    
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise

async def main():
    # Initialize OpenAI client
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create database pool
    pool = await asyncpg.create_pool(
        os.getenv("DATABASE_URL"),
        min_size=1,
        max_size=10,
        command_timeout=60
    )
    
    try:
        # Get test persona data
        print("Fetching test persona data...")
        persona = await get_test_persona(pool)
        print(json.dumps(persona, indent=2, cls=CustomJSONEncoder))
        
        # Test message
        test_message = """
        I've been feeling overwhelmed lately and keep venting to Lisa about everything.
        She's always there for me, but I noticed she seems a bit distant recently.
        I'm worried I might be burdening her too much with my problems.
        How can I maintain our friendship while being more mindful of her boundaries?
        """
        
        # Process test message
        await process_test_message(test_message, persona, client)
    
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise
    
    finally:
        # Close the pool with a timeout
        print("\nClosing database pool...")
        try:
            await asyncio.wait_for(pool.close(), timeout=10.0)
        except asyncio.TimeoutError:
            print("Warning: Pool closing timed out")

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    finally:
        loop.close()
        # Clean up any remaining tasks
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        asyncio.set_event_loop(None) 