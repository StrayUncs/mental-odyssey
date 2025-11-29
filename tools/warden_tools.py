from langchain.tools import tool

@tool
def moderation_tool(user_message: str) -> str:
    """
    Detects unsafe, rude, or illegal content.
    """
    forbidden_words = ["curse1", "curse2"]  # Example placeholder
    for word in forbidden_words:
        if word in user_message.lower():
            return "Please keep the chat respectful and safe."
    return ""  # Empty string means no issues


@tool
def rephrase_tool(user_message: str) -> str:
    """
    Converts unsafe or rude messages into polite, safe language.
    """
    return "Let's rephrase that politely: [insert safer phrasing]."