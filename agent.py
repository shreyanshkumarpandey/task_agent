from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

from tools import create_reminder, list_reminders

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = [create_reminder, list_reminders]

config = types.GenerateContentConfig(
    tools=tools,
)
def run_agent(user_request: str):
    chat = client.chats.create(model="gemini-3.6-flash", config=config)
    response = chat.send_message(user_request)
    print(response.text)


if __name__ == "__main__":
    run_agent("What reminders do I have?")