"""
Module for custom exceptions.
"""


class NoCredentialsError(Exception):
    """
    Exception raised when no credentials are found.
    """

    def __init__(self, message="No credentials found."):
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
