from langchain.tools import tool
from .text_util import extract_text

def _template_fallback_classify(user_message: str) -> str:
    msg = (user_message or "").lower()
    high_risk = ["kill", "bomb", "suicide", "hurt", "attack"]
    medium_risk = ["threat", "bomb", "weapon"]
    low_risk = ["stupid", "idiot", "hate", "jerk"]
    for w in high_risk:
        if w in msg:
            return "UNSAFE: violent or self-harm instruction | SEVERITY: high"
    for w in medium_risk:
        if w in msg:
            return "UNSAFE: violent or illicit instruction | SEVERITY: medium"
    for w in low_risk:
        if w in msg:
            return "UNSAFE: abusive language | SEVERITY: low"
    return "SAFE"

def _template_fallback_rephrase(user_message: str) -> str:
    return "I felt upset by that and would like to discuss it calmly."


def _call_model_with_fallback(system: str, user_message: str) -> str:
    # lazy import agents to avoid circular imports
    try:
        import agents
    except Exception:
        agents = None

    model = getattr(agents, "model", None) if agents is not None else None
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]
    if model is None:
        # choose fallback based on system content
        if "classify" in (system or "").lower():
            return _template_fallback_classify(user_message)
        return _template_fallback_rephrase(user_message)

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

    # final fallback
    if "classify" in (system or "").lower():
        return _template_fallback_classify(user_message)
    return _template_fallback_rephrase(user_message)


@tool
def moderation_tool(user_message: str) -> str:
    """
    Classify user message safety. Return empty string for SAFE, otherwise a single-line UNSAFE response.
    """
    print("moderation_tool CALLED with:", user_message)
    system_prompt = (
        "You are a safety classifier. For the single user message, decide if it is SAFE or UNSAFE. "
        "If SAFE, output exactly: SAFE\n"
        "If UNSAFE, output a single short line following this format (no extra text):\n"
        "UNSAFE: <brief reason> | SEVERITY: <low|medium|high>\n"
        "Reason should be one short phrase. Choose severity: high for imminent harm/violent instructions, "
        "medium for explicit threats or illegal instructions, low for insults/abuse. "
        "Output only the classification line."
    )
    out = _call_model_with_fallback(system_prompt, user_message).strip()
    if out.upper() == "SAFE":
        return ""
    if out:
        return out.splitlines()[0]
    return ""


@tool
def rephrase_tool(user_message: str) -> str:
    """
    Rephrase unsafe or rude messages into polite, safe language. Return single-line rephrase.
    """
    print("rephrase_tool CALLED with:", user_message)
    system_prompt = (
        "You are a polite rephraser. Convert the user's sentence into a safe, respectful alternative. "
        "If the original contains threats, violent instructions, self-harm instructions, or explicit abuse, "
        "remove the violent or instructive content and replace with a calm request or statement. "
        "Output exactly the rephrased sentence only (no explanations). Keep it short (<= 30 words)."
    )
    out = _call_model_with_fallback(system_prompt, user_message).strip()
    if out:
        return out.splitlines()[0]
    return _template_fallback_rephrase(user_message)

# @tool
# def moderation_tool(user_message: str) -> str:
#     """
#     Detects unsafe, rude, or illegal content.
#     """
#     print("moderation_tool CALLED with:", user_message)
#     forbidden_words = ["curse1", "curse2"]  # Example placeholder
#     for word in forbidden_words:
#         if word in user_message.lower():
#             return "Please keep the chat respectful and safe."
#     return ""  # Empty string means no issues


# @tool
# def rephrase_tool(user_message: str) -> str:
#     """
#     Converts unsafe or rude messages into polite, safe language.
#     """
#     print("rephrase_tool CALLED with:", user_message)
#     return "Let's rephrase that politely: [insert safer phrasing]."