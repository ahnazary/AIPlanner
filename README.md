![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Code style: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)
![flake8](https://img.shields.io/badge/flake8-checked-blue)


<p align="center">
  <img src="docs/logo.png" width="400" height="400">
</p>


# AI PLanner

AIPlanner is a Python based tool for summarizing descriptions of events and adding them into a downloadable `.ics` file which can be then added to any calendar application (e.g. Google Calendar, Outlook, etc.). The tool uses a chat interface to interact with the user and extract the event's details. 

At its core, the tool uses 2 main components:

1. [Ollama](https://ollama.com/) for natural language understanding. Generates responses and interacts with the user to extract info of the event to be added to the calendar.
2. [Flask](https://flask.palletsprojects.com/en/2.0.x/) for the web interface. The user interacts with the tool through a web interface.