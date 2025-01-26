from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
from lib.message_processor import MessageProcessor

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://persona-ai-git-main-dvir-zagury-grynbaums-projects.vercel.app",  # Vercel preview
        "https://persona-e9n3v7xkf-dvir-zagury-grynbaums-projects.vercel.app",  # Vercel preview
        "https://dvirzg.com",  # Custom domain
        "https://www.dvirzg.com"  # www subdomain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security setup
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY", "your-secret-api-key")  # You'll set this in Railway
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Initialize message processor
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
message_processor = MessageProcessor(api_key=OPENAI_API_KEY)

# Add a root endpoint for health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

@app.post("/process-message")
async def process_message(
    request_data: dict,
    api_key: str = Depends(verify_api_key)
):
    try:
        result = message_processor.process_message(
            user_message=request_data.get("message"),
            chat_id=request_data.get("chat_id"),
            user_id=request_data.get("user_id"),
            message_history=request_data.get("message_history"),
            system_prompt=request_data.get("system_prompt")
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-title")
async def generate_title(
    request_data: dict,
    api_key: str = Depends(verify_api_key)
):
    try:
        title = message_processor.generate_title(request_data.get("message"))
        return {"title": title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
