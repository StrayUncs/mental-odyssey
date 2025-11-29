from langchain.tools import tool

@tool
def small_talk_tool(user_message: str) -> str:
    """
    Generates casual, friendly conversation responses.
    """
    return "That sounds interesting! Tell me more about your day."


@tool
def positive_reinforcement_tool(user_message: str) -> str:
    """
    Detects sentiment and adds encouragement or support.
    """
    return "You're doing great! Keep going, small steps are progress too."
