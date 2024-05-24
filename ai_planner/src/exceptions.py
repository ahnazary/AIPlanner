"""
Module for custom exceptions.
"""


class NoCredentialsError(Exception):
    """
    Exception raised when no credentials are found.
    """

    def __init__(
        self,
        message="""
        No credentials found. 
        Make sure a file named 'credentials.json' is present in the root directory. 
        Check this link for more information:
        https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application
        """,
    ):
        self.message = message
        super().__init__(self.message)


class NoEventsError(Exception):
    """
    Exception raised when no events are found.
    """

    def __init__(self, message="No events found."):
        self.message = message
        super().__init__(self.message)


class NoOpenAITokenError(Exception):
    """
    Exception raised when no OpenAI token is found.
    """

    def __init__(self, message="No OpenAI token found."):
        self.message = message
        super().__init__(self.message)
