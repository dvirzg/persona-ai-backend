import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_schema():
    """Check the database schema."""
    print("Checking database schema...")
    
    # Create connection pool
    pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
    
    async with pool.acquire() as conn:
        try:
            # Check users table schema
            result = await conn.fetch("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users'
            """)
            print("\nUsers table schema:")
            for r in result:
                print(f"{r['column_name']}: {r['data_type']}")
                
            # Check if tables exist
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            print("\nExisting tables:")
            for t in tables:
                print(t['table_name'])
                
        except Exception as e:
            print(f"Error checking schema: {str(e)}")
            raise
            
    await pool.close()

if __name__ == "__main__":
    asyncio.run(check_schema()) 