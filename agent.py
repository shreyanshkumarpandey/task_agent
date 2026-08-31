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


def inspect_raw_call(user_request: str):
    # Disable automatic function execution so we can see Gemini's raw decision
    manual_config = types.GenerateContentConfig(
        tools=tools,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    chat = client.chats.create(model="gemini-3.6-flash", config=manual_config)
    response = chat.send_message(user_request)

    print("Full response object:")
    print(response.candidates[0].content.parts)


def run_agent(user_request: str):
    chat = client.chats.create(model="gemini-3.6-flash", config=config)
    response = chat.send_message(user_request)
    print(response.text)


if __name__ == "__main__":
    inspect_raw_call("Remind me to buy milk at 6pm")