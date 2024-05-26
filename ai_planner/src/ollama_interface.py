"""
Modukle to interface with the Ollama AI planner
"""

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
        MEthod to extract event in python dictionary format from the bot message
        It extracts the json object from the bot message string.
        The method cuts content between { and } if they exist.

        Args:
        -----
        user_message: str
            The message from the user

        Returns:
        --------
        tuple
            A tuple containing the python dictionary event and the user message
        """
        if "{" not in user_message:
            return None, user_message
        start = user_message.find("{")
        end = user_message.rfind("}")
        return (ast.literal_eval(user_message[start : end + 1]), user_message)
