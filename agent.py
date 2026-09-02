from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

from tools import create_reminder, list_reminders, read_file

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

tools = [create_reminder, list_reminders, read_file]

available_functions = {
    "create_reminder": create_reminder,
    "list_reminders": list_reminders,
    "read_file": read_file,
}


def run_agent_manual(chat, user_request: str):
    """
    Sends a user request to Gemini and manually handles the full agent loop:
      1. Send the request + available tools to Gemini
      2. Check whether Gemini wants to call a tool or just reply with text
      3. If a tool call is requested, execute the real Python function
      4. Send the result back to Gemini and print its final natural-language reply
    """
    response = chat.send_message(user_request)
    part = response.candidates[0].content.parts[0]

    # Case 1: Gemini just wants to reply with text, no tool needed
    if part.function_call is None:
        print(f"Agent: {response.text}")
        return

    # Case 2: Gemini wants to call a tool
    function_call = part.function_call
    print(f"  [calling tool: {function_call.name}({function_call.args})]")

    function_to_call = available_functions[function_call.name]
    result = function_to_call(**function_call.args)

    function_response_part = types.Part.from_function_response(
        name=function_call.name,
        response={"result": result},
    )
    final_response = chat.send_message(function_response_part)
    print(f"Agent: {final_response.text}")


def main():
    config = types.GenerateContentConfig(
        tools=tools,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        system_instruction=(
            "You are a personal task assistant. Use the available tools to help "
            "the user manage reminders and read files. Be concise in your replies."
        ),
    )
    chat = client.chats.create(model="gemini-3.6-flash", config=config)

    print("Task Agent ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        run_agent_manual(chat, user_input)
        print()


if __name__ == "__main__":
    main()
