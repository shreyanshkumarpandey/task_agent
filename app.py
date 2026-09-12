from flask import Flask, request
from google.genai import types
from agent import client, tools, run_agent_manual

app = Flask(__name__)
config = types.GenerateContentConfig(
    tools=tools,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    system_instruction="You are a personal task assistant. Use the available tools to help the user manage reminders and read files. Be concise.",
)
chat = client.chats.create(model="gemini-3.6-flash", config=config)

conversation_history = []  


@app.route("/")
def home():
    return "Hello, this is my agent!"


@app.route("/chat", methods=["GET", "POST"])
def chat_route():
    if request.method == "POST":
        user_message = request.form["message"]
        conversation_history.append({"role": "user", "text": user_message})

        reply = run_agent_manual(chat, user_message)
        conversation_history.append({"role": "agent", "text": reply})

    messages_html = ""
    for msg in conversation_history:
        css_class = "user-msg" if msg["role"] == "user" else "agent-msg"
        messages_html += f'<div class="{css_class}">{msg["text"]}</div>'

    return f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: sans-serif;
                    max-width: 600px;
                    margin: 40px auto;
                    background: #f4f4f4;
                }}
                h1 {{ text-align: center; color: #333; }}
                .chat-box {{
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    height: 400px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }}
                .user-msg {{
                    align-self: flex-end;
                    background: #007bff;
                    color: white;
                    padding: 8px 14px;
                    border-radius: 14px;
                    max-width: 75%;
                }}
                .agent-msg {{
                    align-self: flex-start;
                    background: #e5e5ea;
                    color: black;
                    padding: 8px 14px;
                    border-radius: 14px;
                    max-width: 75%;
                }}
                form {{
                    display: flex;
                    margin-top: 15px;
                    gap: 8px;
                }}
                input[type=text] {{
                    flex: 1;
                    padding: 10px;
                    border-radius: 8px;
                    border: 1px solid #ccc;
                }}
                button {{
                    padding: 10px 18px;
                    border-radius: 8px;
                    border: none;
                    background: #007bff;
                    color: white;
                    cursor: pointer;
                }}
            </style>
        </head>
        <body>
            <h1>Task Agent</h1>
            <div class="chat-box">
                {messages_html}
            </div>
            <form method="POST">
                <input type="text" name="message" autocomplete="off" autofocus>
                <button type="submit">Send</button>
            </form>
        </body>
        </html>
    '''


if __name__ == "__main__":
    app.run(debug=True)