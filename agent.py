from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

from tools import create_reminder, list_reminders , read_file

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = [create_reminder, list_reminders , read_file]
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

def run_agent_manual(chat, user_request: str):
    
    
    response = chat.send_message(user_request)

    part = response.candidates[0].content.parts[0]
    function_call = part.function_call

    print(f"Gemini wannts to call: {function_call.name}")
    print(f"with arguments: {function_call.args}")

    available_functions = {
        "create_reminder": create_reminder,
        "list_reminders": list_reminders,
        "read_file": read_file,
    }
    function_to_call = available_functions[function_call.name]
    result = function_to_call(**function_call.args)

    print(f"Execution result: {result}")
    function_response_part = types.Part.from_function_response(
        name=function_call.name,
        response={"result": result},
    )

    final_response = chat.send_message(function_response_part)
    print(f"Final reply: {final_response.text}")
    


if __name__ == "__main__":
    manual_config = types.GenerateContentConfig(
            tools=tools,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        )
    chat = client.chats.create(model='gemini-3.6-flash',config = manual_config)
    print("Task Agent ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        run_agent_manual(chat, user_input)
        print()