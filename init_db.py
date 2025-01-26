import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import asyncpg

# Load environment variables
load_dotenv()

async def init_db():
    """Initialize the database schema."""
    print("Initializing database...")
    
    # Get database URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    try:
        # Connect to the database
        pool = await asyncpg.create_pool(db_url)
        async with pool.acquire() as conn:
            # Drop existing tables in reverse order to handle dependencies
            print("Dropping existing tables...")
            await conn.execute("""
                DROP TABLE IF EXISTS person_interests CASCADE;
                DROP TABLE IF EXISTS story_people CASCADE;
                DROP TABLE IF EXISTS interests CASCADE;
                DROP TABLE IF EXISTS stories CASCADE;
                DROP TABLE IF EXISTS people CASCADE;
                DROP TABLE IF EXISTS users CASCADE;
            """)
            
            # Get all migration files
            migrations_dir = Path("migrations")
            migration_files = sorted([f for f in migrations_dir.glob("*.sql")])
            
            # Apply each migration in a transaction
            for migration_file in migration_files:
                print(f"Applying migration: {migration_file.name}")
                try:
                    with open(migration_file, 'r') as f:
                        migration_sql = f.read()
                    await conn.execute(migration_sql)
                    print(f"Successfully applied migration: {migration_file.name}")
                except Exception as e:
                    print(f"Error applying migration {migration_file.name}: {str(e)}")
                    raise
        
        await pool.close()
        print("Successfully initialized database schema")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db()) 