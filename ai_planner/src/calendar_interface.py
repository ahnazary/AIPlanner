"""
This module is not being used in the current version of the project.
"""

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.config import SCOPES
from src.exceptions import NoCredentialsError


class CalendarInterface:
    def __init__(self) -> None:
        pass

    def setup_service(self):
        creds = None
        # check if the token.json and credentials.json files exist in the root directory
        if not os.path.exists("credentials.json") or not os.path.exists("token.json"):
            raise NoCredentialsError()

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        service = build("calendar", "v3", credentials=creds)

        return service

    def add_event(self, event, calendarId: str = "primary"):
        """
        Method that adds an event to the user's primary calendar

        Args:
        -----
        event: dict
            Dictionary containing the event details
            The general structure of the event dictionary is as follows:
            (Checkout this link for more details:
            https://developers.google.com/calendar/api/v3/reference/events)

            {
                "kind": "calendar#event",
                "etag": etag,
                "id": string,
                "status": string,
                "htmlLink": string,
                "created": datetime,
                "updated": datetime,
                "summary": string,
                "description": string,
                "location": string,
                "colorId": string,
                "creator": {
                    "id": string,
                    "email": string,
                    "displayName": string,
                    "self": boolean
                },
                "organizer": {
                    "id": string,
                    "email": string,
                    "displayName": string,
                    "self": boolean
                },
                "start": {
                    "date": date,
                    "dateTime": datetime,
                    "timeZone": string
                },
                "end": {
                    "date": date,
                    "dateTime": datetime,
                    "timeZone": string
                },
                "endTimeUnspecified": boolean,
                "recurrence": [
                    string
                ],
                "recurringEventId": string,
                "originalStartTime": {
                    "date": date,
                    "dateTime": datetime,
                    "timeZone": string
                },
                "transparency": string,
                "visibility": string,
                "iCalUID": string,
                "sequence": integer,
                "attendees": [
                    {
                    "id": string,
                    "email": string,
                    "displayName": string,
                    "organizer": boolean,
                    "self": boolean,
                    "resource": boolean,
                    "optional": boolean,
                    "responseStatus": string,
                    "comment": string,
                    "additionalGuests": integer
                    }
                ],
                "attendeesOmitted": boolean,
                "extendedProperties": {
                    "private": {
                    (key): string
                    },
                    "shared": {
                    (key): string
                    }
                },
                "hangoutLink": string,
                "conferenceData": {
                    "createRequest": {
                    "requestId": string,
                    "conferenceSolutionKey": {
                        "type": string
                    },
                    "status": {
                        "statusCode": string
                    }
                    },
                    "entryPoints": [
                    {
                        "entryPointType": string,
                        "uri": string,
                        "label": string,
                        "pin": string,
                        "accessCode": string,
                        "meetingCode": string,
                        "passcode": string,
                        "password": string
                    }
                    ],
                    "conferenceSolution": {
                    "key": {
                        "type": string
                    },
                    "name": string,
                    "iconUri": string
                    },
                    "conferenceId": string,
                    "signature": string,
                    "notes": string,
                },
                "gadget": {
                    "type": string,
                    "title": string,
                    "link": string,
                    "iconLink": string,
                    "width": integer,
                    "height": integer,
                    "display": string,
                    "preferences": {
                    (key): string
                    }
                },
                "anyoneCanAddSelf": boolean,
                "guestsCanInviteOthers": boolean,
                "guestsCanModify": boolean,
                "guestsCanSeeOtherGuests": boolean,
                "privateCopy": boolean,
                "locked": boolean,
                "reminders": {
                    "useDefault": boolean,
                    "overrides": [
                    {
                        "method": string,
                        "minutes": integer
                    }
                    ]
                },
                "source": {
                    "url": string,
                    "title": string
                },
                "workingLocationProperties": {
                    "type": string,
                    "homeOffice": (value),
                    "customLocation": {
                    "label": string
                    },
                    "officeLocation": {
                    "buildingId": string,
                    "floorId": string,
                    "floorSectionId": string,
                    "deskId": string,
                    "label": string
                    }
                },
                "outOfOfficeProperties": {
                    "autoDeclineMode": string,
                    "declineMessage": string
                },
                "focusTimeProperties": {
                    "autoDeclineMode": string,
                    "declineMessage": string,
                    "chatStatus": string
                },
                "attachments": [
                    {
                    "fileUrl": string,
                    "title": string,
                    "mimeType": string,
                    "iconLink": string,
                    "fileId": string
                    }
                ],
                "eventType": string
                }
        """
        service = self.setup_service()
        event = service.events().insert(calendarId="primary", body=event).execute()
        print("Event created: %s" % (event.get("htmlLink")))
