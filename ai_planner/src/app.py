from flask import Flask, render_template, request, jsonify

# from calendar_interface import CalendarInterface
from ollama_interface import OllamaInterface
import signal
import os
from logging import getLogger

logger = getLogger(__name__)
app = Flask(__name__)

# Initialize the conversation with the first bot message
conversations = [
    {
        "sender": "bot",
        "message": "Hi, I'm your calendar assistant. What event would you like to add to your calendar?",
    }
]

# calendar_interface = CalendarInterface()
ollama_interface = OllamaInterface()


@app.route("/")
def index():
    return render_template("index.html", conversations=conversations)


@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.form["message"]
    # Add user message to conversation
    logger.warning(f"User message: {user_message}")
    conversations.append({"sender": "user", "message": user_message})

    bot_response = ollama_interface.chat(user_message)
    logger.warning(f"Bot response: {bot_response}")
    conversations.append({"sender": "bot", "message": bot_response})

    # if the user typed quit then the chat will be closed
    if user_message.lower() == "quit":
        conversations.append(
            {
                "sender": "bot",
                "message": "Thank you for using the calendar assistant. Have a great day!",
            }
        )

    return jsonify(conversations)


@app.route("/quit", methods=["POST"])
def quit():
    os.kill(os.getpid(), signal.SIGINT)
    return "Server shutting down..."


if __name__ == "__main__":
    app.run(debug=True)
