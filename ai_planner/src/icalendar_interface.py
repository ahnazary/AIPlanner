"""
Module to write events to an ics file.
"""

import os

from ics import Calendar, Event


class ICalendarInterface:
    """
    Class to write events to an ics file.
    """

    def __init__(self):
        self.calendar = Calendar()

    def add_event(
        self,
        summary: str,
        description: str,
        start_time: str,
        end_time: str,
        location: str = None,
        timezone: str = None,
    ):
        """
        Add an event to the calendar.
        Args:
            event (Event): The event to add.
        """
        event = Event()
        event.name = summary
        event.description = description
        event.begin = start_time
        event.end = end_time
        event.location = location if location else None

        self.calendar.events.add(event)

    def write(self, file_path: os.PathLike = "calendar.ics") -> str:
        """
        Write the calendar to an ics file.

        Args:
            file_path (str): The path to the file to write to.

        Returns:
            str: The absolute path to the file.
        """
        with open(file_path, "w") as file:
            file.writelines(self.calendar)

        return os.path.abspath(file_path)
