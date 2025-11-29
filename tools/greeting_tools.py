from langchain.tools import tool

@tool
def greet_user(name: str, sentence: str) -> str:
    """
    Greets a new user joining the chat.
    If a sentence is provided, respond to it in a friendly, positive way.
    """
    return f"Hello {name}! {sentence or 'How are you feeling today?'}"

@tool
def response_to_greeting(name: str, sentence: str) -> str:
    """
    Responds to a user's greeting after initial welcome.
    Keep responses warm and friendly.
    """
    return f"Hi {name}, {sentence or 'nice to see you again!'}"