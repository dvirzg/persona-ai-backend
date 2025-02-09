import asyncio
import websockets
import json
import uuid

async def test_websocket():
    uri = "ws://localhost:8000/api/ws/pipeline"
    
    async with websockets.connect(uri) as websocket:
        # Test message data
        message_data = {
            "content": "Hello, how are you?",
            "chat_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "role": "user"
        }
        
        print(f"Sending message with data: {json.dumps(message_data, indent=2)}")
        
        # Send message data
        await websocket.send(json.dumps(message_data))
        
        # Receive and print responses
        while True:
            try:
                response = await websocket.recv()
                print(f"Received: {response}")
            except websockets.exceptions.ConnectionClosed:
                break

if __name__ == "__main__":
    asyncio.run(test_websocket()) 