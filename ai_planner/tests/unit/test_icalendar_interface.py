import os

from src.icalendar_interface import ICalendarInterface


def test_add_event():
    icalendar_interface = ICalendarInterface()
    icalendar_interface.add_event(
        summary="Test Event",
        description="This is a test event",
        start_time="2024-06-01T12:00:00",
        end_time="2024-06-01T13:00:00",
    )
    assert len(icalendar_interface.calendar.events) == 1
    assert (
        str(list(icalendar_interface.calendar.events)[0].end)
        == "2024-06-01T13:00:00+00:00"
    )
    assert (
        str(list(icalendar_interface.calendar.events)[0].begin)
        == "2024-06-01T12:00:00+00:00"
    )
    assert list(icalendar_interface.calendar.events)[0].name == "Test Event"
    assert (
        list(icalendar_interface.calendar.events)[0].description
        == "This is a test event"
    )


def test_write():
    icalendar_interface = ICalendarInterface()
    icalendar_interface.add_event(
        summary="Test Event",
        description="This is a test event",
        start_time="2021-06-01T12:00:00",
        end_time="2021-06-01T13:00:00",
    )
    icalendar_interface.write(file_path="test.ics")
    assert os.path.exists("test.ics") is True
    assert os.path.abspath("test.ics") == os.path.abspath("test.ics")
    os.remove("test.ics")
