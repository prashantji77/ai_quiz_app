import requests
import os
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self, api_key=None):
        # Use env variable 
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def call_ai(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "openai/gpt-3.5-turbo",  # or another free model
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        # print("Sending request to OpenRouter...")
        # print(f"prompt: {prompt}")
        response = requests.post(self.url, headers=headers, json=data)
        response.raise_for_status()
        # print(f"response: {response.json()}")
        return response.json()["choices"][0]["message"]["content"]
