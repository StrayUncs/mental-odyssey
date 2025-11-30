from langchain.tools import tool
import agents
from .text_util import extract_text

def _call_model_with_fallback(system: str, user_message: str) -> str:
    """
    Try to call agents.model with a few possible APIs (invoke, chat, __call__).
    Fall back to a template response if no model API is available.
    """
    model = getattr(agents, "model", None)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]
    if model is None:
        # No model available; return a simple templated response
        return _template_fallback(user_message, system)
    # try known call signatures
    for fn_name in ("invoke", "chat", "generate", "__call__", "complete"):
        fn = getattr(model, fn_name, None)
        if callable(fn):
            try:
                # different APIs expect different input shapes; try common ones
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
    return _template_fallback(user_message, system)

def _template_fallback(user_message: str, system_hint: str) -> str:
    # produce a differentiated response based on the intended tool role (system_hint)
    hint = (system_hint or "").lower()
    if "encourag" in hint or "reinforce" in hint:
        # positive reinforcement style
        return (
            "You are doing really well — small steps matter. "
            "Try naming one small thing you accomplished today and build from there. "
            "I'm proud of you for reaching out."
        )
    if "small" in hint or "casual" in hint or "friend" in hint:
        # small talk style
        return (
            "That's interesting — tell me one small thing that made you smile recently. "
            "I'd love to hear more about it."
        )
    # default
    return "Thanks for sharing. Could you say a bit more about how you're feeling right now?"

@tool
def small_talk_tool(user_message: str) -> str:
    """Generates casual, friendly conversation responses."""
    print("small_talk_tool CALLED with:", user_message)
    system_prompt = (
        "You are a friendly, casual conversationalist. Reply in 1-2 short sentences, "
        "use a warm tone, and include a light follow-up question. Do NOT call tools."
    )
    return _call_model_with_fallback(system_prompt, user_message)

@tool
def positive_reinforcement_tool(user_message: str) -> str:
    """Detects sentiment and adds encouragement or support; offer one concrete suggestion."""
    print("positive_reinforcement_tool CALLED with:", user_message)
    system_prompt = (
        "You are a concise encouragement agent. Acknowledge the user's emotion briefly (1 sentence), "
        "validate it, then offer one specific, practical next step (one sentence). Do NOT call tools."
    )
    # prepend small instruction to focus output form
    instruct = user_message
    return _call_model_with_fallback(system_prompt, instruct)

# @tool
# def small_talk_tool(user_message: str) -> str:
#     """
#     Generates casual, friendly conversation responses.
#     """
#     print("small_talk_tool CALLED with:", user_message)
#     return "That sounds interesting! Tell me more about your day."


# @tool
# def positive_reinforcement_tool(user_message: str) -> str:
#     """
#     Detects sentiment and adds encouragement or support.
#     """
#     print("positive_reinforcement_tool CALLED with:", user_message)
#     return "You're doing great! Keep going, small steps are progress too."
