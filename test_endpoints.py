import requests
import json

BASE_URL = "http://localhost:8000"

def test_generate_title():
    response = requests.post(
        f"{BASE_URL}/generate-title",
        json={"message": "Hello, how are you?"}
    )
    print("\nTest generate_title:")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_process_message():
    response = requests.post(
        f"{BASE_URL}/process-message",
        json={
            "user_message": "Hello, how are you?",
            "chat_id": "test-chat-1",
            "user_id": "test-user-1",
            "message_history": [],
            "system_prompt": "You are a helpful assistant."
        }
    )
    print("\nTest process_message:")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("Testing backend endpoints...")
    test_generate_title()
    test_process_message() 