import ollama
import ast


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
        it also removes 3 lines before first { and 1 lines after last }.

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
        start = user_message.find("{")
        end = user_message.rfind("}")
        return (
            ast.literal_eval(user_message[start : end + 1]),
            user_message[: start - 1] + user_message[end + 2 :],
        )


if __name__ == "__main__":
    interface = OllamaInterface()
    print(
        interface.refine_message(
            """
                             I extracted the following fields from your text:

**Summary:** Dentist Appointment
**Description:** Fixing teeth
**Location:** Berlin (assuming EU/Berlin time zone)
**Start Date and Time:** 2024-05-25T09:00:00
**End Date and Time:** Not provided (assuming the appointment ends at some point, but I'll need you to confirm this)

Please let me know if this is correct or if you'd like to add any other details. Also, please confirm your End Date and Time.

Here's a summary of what we have so far:

```
{
  "Summary": "Dentist Appointment",
  "Description": "Fixing teeth",
  "Location": "Berlin",
  "Start Date and Time": "2024-05-25T09:00:00",
  "End Date and Time": "?",
  "Time Zone": "EU/Berlin"
}
```

Would you like to add more events or stop here?"""
        )[0]
    )
