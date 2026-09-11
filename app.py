from flask import Flask , request
from google.genai import types
from agent import client,tools, run_agent_manual

app = Flask(__name__)
config = types.GenerateContentConfig(
    tools=tools,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    system_instruction="You are a personal task assistant. Use the available tools to help the user manage reminders and read files. Be concise.",
)
chat = client.chats.create(model="gemini-3.6-flash", config=config)

@app.route("/")
def home():
    return "Hello, this is my agent!"

@app.route("/chat", methods=["GET", "POST"])
def chat_route():
    if request.method == "POST":
        user_message = request.form["message"]
        reply = run_agent_manual(chat, user_message)
        return f'''
            <p><b>You:</b> {user_message}</p>
            <p><b>Agent:</b> {reply}</p>
            <form method="POST">
                <input type="text" name="message">
                <button type="submit">Send</button>
            </form>
        '''

    return '''
        <form method="POST">
            <input type="text" name="message">
            <button type="submit">Send</button>
        </form>
    '''
if __name__ == "__main__":
    app.run(debug=True)
