from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
import message_processor  # Changed to simple import

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
message_processor_instance = message_processor.MessageProcessor(api_key=OPENAI_API_KEY)

# Add a root endpoint for health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

async def verify_api_key(api_key: str = Depends(api_key_header)):
    print(f"Received API key: {api_key[:4]}...")  # Only log first 4 chars for security
    print(f"Expected API key: {API_KEY[:4]}...")
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

@app.post("/process-message")
async def process_message(
    request: Request,
    request_data: dict,
    api_key: str = Depends(verify_api_key)
):
    try:
        print("Received request headers:", dict(request.headers))
        print("Received request data:", request_data)
        
        result = message_processor_instance.process_message(
            user_message=request_data.get("message"),
            chat_id=request_data.get("chat_id"),
            user_id=request_data.get("user_id"),
            message_history=request_data.get("message_history"),
            system_prompt=request_data.get("system_prompt")
        )
        print("Processing result:", result)
        return result
    except Exception as e:
        print("Error processing message:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-title")
async def generate_title(
    request: Request,
    request_data: dict,
    api_key: str = Depends(verify_api_key)
):
    try:
        print("Received request headers:", dict(request.headers))
        print("Received request data:", request_data)
        
        title = message_processor_instance.generate_title(request_data.get("message"))
        print("Generated title:", title)
        return {"title": title}
    except Exception as e:
        print("Error generating title:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
