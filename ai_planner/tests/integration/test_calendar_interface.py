from src.calendar_interface import CalendarInterface


def test_add_event():
    calendar_interface = CalendarInterface()

    event = {
        "summary": "Google I/O 2015",
        "location": "800 Howard St., San Francisco, CA 94103",
        "description": "A chance to hear more about Google's developer products.",
        "start": {
            "dateTime": "2024-05-26T09:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": "2024-05-26T17:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "recurrence": [],
        "attendees": [],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    calendar_interface.add_event(event)
