from langchain.tools import tool

@tool
def relationship_advice_tool(user_message: str) -> str:
    """
    Provides thoughtful advice for relationship issues.
    """
    return "Consider communicating your feelings clearly and listening actively. Healthy boundaries are important."


@tool
def communication_tips_tool(user_message: str) -> str:
    """
    Provides tips for phrasing difficult conversations in relationships.
    """
    return "Try using 'I feel' statements rather than 'You did' statements. This can reduce conflict and increase understanding."
