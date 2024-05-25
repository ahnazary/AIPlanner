import ast

import ollama


class OllamaInterface:
    def __init__(self):
        self.ollama = ollama

    def chat(self, user_message, model: str = "aiplanner") -> str:
        """
        Method to chat with the AI planner model

        Args:
        -----
        user_message: str
            The message from the user
        model: str
            The model to use for the conversation

        Returns:
        --------
        str
            The response from the AI planner model
        """
        response = self.ollama.chat(
            model=model, messages=[{"role": "user", "content": user_message}]
        )
        return str(response["message"]["content"])

    def refine_message(self, user_message: str) -> tuple:
        """
        Method to refine the user message before showing it in the UI.
        It seperates extracts the json object from the bot message string to add it to calcender.
        The method cuts content between { and } if they exist.

        it returns the json object extracted from the message and the rest of the message.
        Args:
        -----
        user_message: str
            The message from the user

        Returns:
        --------
        str
            The refined message
        """
        if "{" not in user_message:
            return None, user_message
        start = user_message.find("{")
        end = user_message.rfind("}")
        return (ast.literal_eval(user_message[start : end + 1]), user_message)
