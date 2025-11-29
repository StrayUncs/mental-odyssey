from langchain.tools import tool

@tool
def provide_anxiety_advice(user_message: str) -> str:
    """
    Provides tips for coping with anxiety, stress, or worry.
    """
    return "Here are some coping strategies: take deep breaths, focus on grounding techniques, and try to challenge anxious thoughts calmly."


@tool
def suggest_resources(user_message: str) -> str:
    """
    Suggests resources for anxiety management (articles, exercises, apps).
    """
    return "You can check out anxiety management apps like Headspace or Calm, or read articles on mindfulness and CBT techniques."
