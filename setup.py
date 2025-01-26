import os
import shutil
from pathlib import Path

def setup_dev_environment():
    """Set up the development environment."""
    print("Setting up development environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("Created .env file from .env.example")
        print("Please edit .env with your credentials")
    
    # Create migrations directory if it doesn't exist
    migrations_dir = Path('migrations')
    migrations_dir.mkdir(exist_ok=True)
    print("Ensured migrations directory exists")
    
    # Create components directory if it doesn't exist
    components_dir = Path('components')
    components_dir.mkdir(exist_ok=True)
    print("Ensured components directory exists")
    
    # Install requirements
    print("\nInstalling requirements...")
    os.system('pip install -r requirements.txt')
    
    print("\nSetup complete! Next steps:")
    print("1. Edit .env with your database and OpenAI credentials")
    print("2. Run python init_db.py to initialize the database")
    print("3. Run uvicorn message_processor:app --reload to start the server")

if __name__ == "__main__":
    setup_dev_environment() 