import os
import pathlib
import signal

from flask import Flask, jsonify, render_template, request, send_file
from icalendar_interface import ICalendarInterface
from lib import custom_logger
from ollama_interface import OllamaInterface

logger = custom_logger()
app = Flask(__name__)
event = None

# Initialize the conversation with the first bot message
conversations = [
    {
        "sender": "bot",
        "message": """Hi, I'm your calendar assistant.
        What event would you like to add to your calendar?
        Please provide the event details including event start and end time and some description.
        """,
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

    # Add processing message immediately
    conversations.append(
        {
            "sender": "bot",
            "message": "Please wait while I am processing your request...",
        }
    )

    global event
    response = ollama_interface.chat(user_message)
    if response:
        event, bot_response = ollama_interface.refine_message(response)
        bot_response = response
    else:
        event = None
        bot_response = "I'm sorry, I didn't understand that. Could you please rephrase your request?"  # noqa E501

    # Replace the processing message with the actual bot response
    conversations.pop()
    conversations.append({"sender": "bot", "message": bot_response})

    # if the user typed quit then the chat will be closed
    if user_message.lower() == "quit":
        conversations.append(
            {
                "sender": "bot",
                "message": "Thank you for using aiplanner. Have a great day!",
            }
        )

    return jsonify(conversations)


@app.route("/add_event", methods=["POST"])
def add_event():
    # Sample prompt:
    # Got have a dentist appointment on 26th of August 2024 of 10:00 AM for 1 hour in Berlin.
    global event
    if event:
        logger.info("Event has been extracted.")
        # remove spaces from event keys and make only first letter lowercase
        event = {k.replace(" ", "").lower(): v for k, v in event.items()}
        logger.info(f"Event data: {event}")
        icalendar_interface.add_event(
            summary=event["summary"],
            description=event["description"] if "description" in event else " ",
            start_time=event["startdatetime"],
            end_time=event["enddatetime"],
        )
        logger.info(f"event added to the calendar: {event}")
        icalendar_interface.write(
            file_path=os.path.join(
                pathlib.Path(__file__).parent.absolute(), "calendar.ics"
            )
        )
        logger.info(
            f"Calendar file created successfully on path: {os.path.join(pathlib.Path(__file__).parent.absolute(), 'calendar.ics')}"  # noqa E501
        )
    else:
        logger.info("No event data available to add to the calendar.")

    return jsonify(conversations)


@app.route("/download", methods=["GET"])
def download():
    # check if the calendar file exists
    if not os.path.exists(pathlib.Path(__file__).parent.absolute() / "calendar.ics"):
        return "No calendar file found.", 404
    return send_file(
        pathlib.Path(__file__).parent.absolute() / "calendar.ics", as_attachment=True
    )


@app.route("/quit", methods=["POST"])
def quit():
    os.kill(os.getpid(), signal.SIGINT)
    # delete the calendar file
    if os.path.exists(pathlib.Path(__file__).parent.absolute() / "calendar.ics"):
        os.remove(pathlib.Path(__file__).parent.absolute() / "calendar.ics")
    return "Server shutting down..."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
