import os
import signal
from logging import getLogger

from calendar_interface import CalendarInterface
from flask import Flask, jsonify, render_template, request
from ollama_interface import OllamaInterface

logger = getLogger(__name__)
app = Flask(__name__)
event = None

# Initialize the conversation with the first bot message
conversations = [
    {
        "sender": "bot",
        "message": """Hi, I'm your calendar assistant.
        What event would you like to add to your calendar?""",
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
    logger.info(f"User message: {user_message}")
    conversations.append({"sender": "user", "message": user_message})

    global event
    response = ollama_interface.chat(user_message)
    if response:
        event, bot_response = ollama_interface.refine_message(response)
    else:
        event = None
        bot_response = (
            "I'm sorry, I didn't understand that. Could you please add more details?"
        )

    # logger.info(f"Bot response: {bot_response}")
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


@app.route("/add_event", methods=["POST"])
def add_event():
    global event
    if event:
        # add event to the calendar
        calendar_interface = CalendarInterface()
        # remove spaces from event keys and make only first letter lowercase
        event = {k.replace(" ", "").lower(): v for k, v in event.items()}
        normalised_event = {
            "summary": event["summary"],
            "description": event["description"],
            "location": event["location"],
            "start": {
                "dateTime": event["startdatetime"],
                "timeZone": (
                    event["timezone"] if "timezone" in event else "Europe/Berlin"
                ),
            },
            "end": {
                "dateTime": event["enddatetime"],
                "timeZone": (
                    event["timezone"] if "timezone" in event else "Europe/Berlin"
                ),
            },
        }

        # drops keys with None values or ""
        normalised_event = {k: v for k, v in normalised_event.items() if v}
        logger.info(f"Normalised event: {normalised_event}")
        calendar_interface.add_event(normalised_event)
        logger.info("Event added to the calendar.")
    else:
        logger.info("No event data available to add to the calendar.")

    return jsonify(conversations)


@app.route("/quit", methods=["POST"])
def quit():
    os.kill(os.getpid(), signal.SIGINT)
    return "Server shutting down..."


if __name__ == "__main__":
    app.run(debug=True)
