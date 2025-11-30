from langchain.tools import tool
from .text_util import extract_text

def _template_fallback(user_message: str, system_hint: str) -> str:
    hint = (system_hint or "").lower()
    if "conflict" in hint or "argu" in hint or "breakup" in hint:
        return (
            "It can help to pause and use 'I' statements. "
            "Try: 'I feel X when Y happens; can we talk about how to change that?'"
        )
    if "communication" in hint or "phrasing" in hint or "ask for space" in hint:
        return (
            "Use a calm, specific request: 'I need some space this week to recharge. "
            "Can we set a time to talk on Sunday?'"
        )
    return "Try describing one specific behavior you'd like to change and ask for one concrete step."

def _call_model_with_fallback(system: str, user_message: str) -> str:
    # lazy import agents to avoid circular imports
    import agents
    model = getattr(agents, "model", None)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]
    if model is None:
        return _template_fallback(user_message, system)
    for fn_name in ("invoke", "chat", "generate", "__call__", "complete"):
        fn = getattr(model, fn_name, None)
        if callable(fn):
            try:
                if fn_name == "invoke":
                    raw = fn({"messages": messages})
                elif fn_name == "chat":
                    raw = fn(messages=messages)
                elif fn_name == "generate":
                    raw = fn(messages)
                elif fn_name == "__call__":
                    raw = fn(messages)
                else:
                    raw = fn(messages)
                return extract_text(raw)
            except Exception:
                continue
    return _template_fallback(user_message, system)

@tool
def relationship_advice_tool(user_message: str) -> str:
    """
    Provides thoughtful advice for relationship issues using the model.
    """
    print("relationship_advice_tool CALLED with:", user_message)
    system_prompt = (
        "You are a relationship coach. Read the user's short description and provide a "
        "brief, actionable set of steps (2-4 sentences) for addressing the relationship problem. "
        "Be empathetic, practical, and avoid moralizing. Do NOT call tools."
    )
    return _call_model_with_fallback(system_prompt, user_message)

@tool
def communication_tips_tool(user_message: str) -> str:
    """
    Provides tips and phrasing for difficult conversations.
    """
    print("communication_tips_tool CALLED with:", user_message)
    system_prompt = (
        "You are a communication coach. Provide one concise suggested script (1-2 sentences) "
        "the user can say in a difficult conversation, plus a brief rationale (1 sentence). "
        "Keep language calm and specific. Do NOT call tools."
    )
    return _call_model_with_fallback(system_prompt, user_message)

# @tool
# def relationship_advice_tool(user_message: str) -> str:
#     """
#     Provides thoughtful advice for relationship issues.
#     """
#     print("relationship_advice_tool CALLED with:", user_message)
#     return "Consider communicating your feelings clearly and listening actively. Healthy boundaries are important."


# @tool
# def communication_tips_tool(user_message: str) -> str:
#     """
#     Provides tips for phrasing difficult conversations in relationships.
#     """
#     print("communication_tips_tool CALLED with:", user_message)
#     return "Try using 'I feel' statements rather than 'You did' statements. This can reduce conflict and increase understanding."
