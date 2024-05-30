import os
import signal
from logging import getLogger

from flask import Flask, jsonify, render_template, request
from icalendar_interface import ICalendarInterface
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
icalendar_interface = ICalendarInterface()


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
    # Sample prompt:
    # I have a dentist appointment on Monday at 10:00 AM which lasts for 1 hour in Munich.
    global event
    if event:
        # remove spaces from event keys and make only first letter lowercase
        event = {k.replace(" ", "").lower(): v for k, v in event.items()}
        icalendar_interface.add_event(
            summary=event["summary"],
            description=event["description"],
            start_time=event["startdatetime"],
            end_time=event["enddatetime"],
        )
        logger.info(f"event added to the calendar: {event}")
        icalendar_interface.write(file_path="calendar.ics")
    else:
        logger.info("No event data available to add to the calendar.")

    return jsonify(conversations)


@app.route("/quit", methods=["POST"])
def quit():
    os.kill(os.getpid(), signal.SIGINT)
    return "Server shutting down..."


if __name__ == "__main__":
    app.run(debug=True)
