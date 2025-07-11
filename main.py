from src.ai.mistral import MistralClient, ChatSession
from dotenv import load_dotenv
import os


mistral = MistralClient(
    api_key=os.environ.get("MISTRAL_API_KEY"), model="mistral-medium-2505"
)
session = ChatSession(mistral)

while True:
    print(session.send(input()))
