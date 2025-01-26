from typing import Dict, Any, List
import asyncpg
from datetime import datetime
import json

class FetcherAndSaver:
    def __init__(self, db_pool: asyncpg.Pool):
        self.db = db_pool
        
    async def process(self, message_data: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """Process insights and manage user context."""
        
        # Save new insights
        await self.save_insights(message_data["user_id"], insights)
        
        # Fetch relevant context
        context = await self.fetch_context(message_data["user_id"])
        
        return context
        
    async def save_insights(self, user_id: str, insights: Dict[str, Any]) -> None:
        """Save new insights to the database."""
        async with self.db.acquire() as conn:
            # Save personality traits and communication style
            if insights["personality_traits"] or insights["communication_style"]:
                await conn.execute("""
                    UPDATE users 
                    SET personality_traits = COALESCE(personality_traits, '{}'::jsonb) || $1::jsonb,
                        communication_style = COALESCE(communication_style, '{}'::jsonb) || $2::jsonb
                    WHERE id = $3
                """, json.dumps(insights["personality_traits"]), 
                     json.dumps(insights.get("communication_style", {})),
                     user_id)
            
            # Save interests
            for interest in insights.get("interests", []):
                await conn.execute("""
                    INSERT INTO interests (user_id, name, summary)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (user_id, name) DO UPDATE
                    SET summary = EXCLUDED.summary
                """, user_id, interest["name"], interest.get("summary", ""))
            
            # Save people
            for person in insights.get("people", []):
                await conn.execute("""
                    INSERT INTO people (user_id, name, relationship, notes)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (user_id, name) DO UPDATE
                    SET relationship = EXCLUDED.relationship,
                        notes = COALESCE(people.notes, '') || ' ' || EXCLUDED.notes
                """, user_id, person["name"], 
                     person.get("relationship", ""),
                     person.get("notes", ""))
            
            # Save stories
            for story in insights.get("stories", []):
                story_id = await conn.fetchval("""
                    INSERT INTO stories (user_id, title, description, location, timestamp)
                    VALUES ($1, $2, $3, $4, $5)
                    RETURNING id
                """, user_id, story["title"], 
                     story["description"],
                     story.get("location", ""),
                     datetime.now())
                
                # Link people to story if mentioned
                if "people" in story:
                    for person in story["people"]:
                        person_id = await conn.fetchval(
                            "SELECT id FROM people WHERE user_id = $1 AND name = $2",
                            user_id, person
                        )
                        if person_id:
                            await conn.execute("""
                                INSERT INTO story_people (story_id, person_id)
                                VALUES ($1, $2)
                                ON CONFLICT DO NOTHING
                            """, story_id, person_id)
    
    async def fetch_context(self, user_id: str) -> Dict[str, Any]:
        """Fetch user context including profile, interests, people, and stories."""
        async with self.db.acquire() as conn:
            # Fetch user profile
            user = await conn.fetchrow("""
                SELECT 
                    name,
                    COALESCE(personality_traits, '{}'::jsonb) as personality_traits,
                    COALESCE(communication_style, '{}'::jsonb) as communication_style,
                    COALESCE(demographic, '{}'::jsonb) as demographic
                FROM users 
                WHERE id = $1
            """, user_id)
            
            if not user:
                return {}

            # Fetch interests
            interests = await conn.fetch("""
                SELECT name, summary
                FROM interests
                WHERE user_id = $1
            """, user_id)

            # Fetch people
            people = await conn.fetch("""
                SELECT name, relationship, notes
                FROM people
                WHERE user_id = $1
            """, user_id)

            # Fetch stories
            stories = await conn.fetch("""
                SELECT title, description, location, timestamp
                FROM stories
                WHERE user_id = $1
                ORDER BY timestamp DESC
                LIMIT 5
            """, user_id)

            return {
                "profile": {
                    "name": user["name"],
                    "personality_traits": user["personality_traits"],
                    "communication_style": user["communication_style"],
                    "demographic": user["demographic"]
                },
                "interests": [dict(i) for i in interests],
                "people": [dict(p) for p in people],
                "stories": [dict(s) for s in stories]
            } 