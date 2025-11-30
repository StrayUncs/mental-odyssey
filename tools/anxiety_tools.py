from langchain.tools import tool

from .text_util import extract_text

def _template_fallback(user_message: str, system_hint: str) -> str:
    hint = (system_hint or "").lower()
    if "panic" in hint or "can't breathe" in hint or "hyperventil" in hint:
        return (
            "If you are having a panic attack: try a 4-4-4 breathing exercise (inhale 4s, hold 4s, exhale 4s). "
            "If you feel unsafe, contact local emergency services now."
        )
    if "cbt" in hint or "resources" in hint or "worksheets" in hint:
        return (
            "Try CBT worksheets, grounding exercises, or apps like Headspace/Calm. "
            "Search for 'CBT anxiety worksheets' for free guides and exercises."
        )
    return "I'm sorry you're struggling — try grounding, breathing, and tell me one small detail about what's happening."


def _call_model_with_fallback(system: str, user_message: str) -> str:
    # lazy import to avoid circular dependencies
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
def provide_anxiety_advice(user_message: str) -> str:
    """
    Provides concise, practical coping steps for anxiety or panic.
    """
    print("provide_anxiety_advice CALLED with:", user_message)
    system_prompt = (
        "You are a calm anxiety-coping assistant. For the given user message, "
        "output 2-4 short sentences: 1) acknowledge the feeling, 2) give 1-2 concrete coping steps "
        "(breathing/grounding/exposure-style tip), and 3) a short next-step suggestion. "
        "Keep tone empathetic and concise. Do NOT call tools."
    )
    return _call_model_with_fallback(system_prompt, user_message)

@tool
def suggest_resources(user_message: str) -> str:
    """
    Suggests tangible resources (apps, worksheets, brief referrals) for anxiety management.
    """
    print("suggest_resources CALLED with:", user_message)
    system_prompt = (
        "You are a resource recommender for anxiety management. Given a short user request, "
        "return a bulleted or comma-separated list (<=3 items) of high-quality resources: apps, free worksheets, "
        "and a short note about when to use them. Keep it practical and concise. Do NOT call tools."
    )
    return _call_model_with_fallback(system_prompt, user_message)

# @tool
# def provide_anxiety_advice(user_message: str) -> str:
#     """
#     Provides tips for coping with anxiety, stress, or worry.
#     """
#     print("provide_anxiety_advice CALLED with:", user_message)
#     return "Here are some coping strategies: take deep breaths, focus on grounding techniques, and try to challenge anxious thoughts calmly."


# @tool
# def suggest_resources(user_message: str) -> str:
#     """
#     Suggests resources for anxiety management (articles, exercises, apps).
#     """
#     print("suggest_resources CALLED with:", user_message)
#     return "You can check out anxiety management apps like Headspace or Calm, or read articles on mindfulness and CBT techniques."
