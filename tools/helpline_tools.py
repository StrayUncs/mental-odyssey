from langchain.tools import tool

@tool
def suicide_hotline_lookup(location: str = "UK") -> str:
    """
    Returns helpline info based on location. Default is UK.
    """
    return "If you are in danger or thinking about suicide, please call the Samaritans at 116 123 (UK) or your local helpline."

@tool
def emergency_response_tool(user_message: str) -> str:
    """
    Generates an urgent response in crisis situations.
    """
    return "It sounds like you're in crisis. Please reach out immediately to a trained professional or call your local emergency helpline."
