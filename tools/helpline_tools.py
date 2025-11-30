from langchain.tools import tool
import agents 
from .text_util import extract_text

def _template_fallback(user_message: str, system_hint: str) -> str:
    hint = (system_hint or "").lower()
    if "crisis" in hint or "imminent" in hint or "self-harm" in hint:
        return (
            "If you are in immediate danger or thinking about suicide, please call your local emergency services now. "
            "If you're in the UK call Samaritans 116 123; in the US call 988. "
            "You are not alone — please reach out for immediate help."
        )
    return "I hear you — if this is an emergency please contact local services now. If not, please tell me more so I can help."

def _call_model_with_fallback(system: str, user_message: str) -> str:
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
def suicide_hotline_lookup(location: str = "UK") -> str:
    """
    Return concise, location-aware helpline info using the model when available.
    """
    print("suicide_hotline_lookup CALLED with:", location)
    system_prompt = (
        "You are a crisis resource assistant. Given a short location string, return a single concise line with "
        "the most relevant suicide prevention hotline and emergency contact for that location. "
        "If location is ambiguous, provide a general international emergency guidance line. "
        "Do NOT call any tools; return only the contact information in plain text."
    )
    user_msg = f"Provide hotline information for location: {location}"
    return _call_model_with_fallback(system_prompt, user_msg)

@tool
def emergency_response_tool(user_message: str) -> str:
    """
    Generate an immediate, safety-focused response for crisis messages.
    """
    print("emergency_response_tool CALLED with:", user_message)
    system_prompt = (
        "You are an urgent crisis-response assistant. The user message may indicate imminent self-harm or danger. "
        "Output a brief, direct safety plan: acknowledge the danger, instruct immediate emergency contacts if needed, "
        "provide one grounding step the user can do now, and encourage contacting trained professionals. "
        "Keep output to 2-4 short sentences. Do NOT call tools."
    )
    return _call_model_with_fallback(system_prompt, user_message)

# @tool
# def suicide_hotline_lookup(location: str = "UK") -> str:
#     """
#     Returns helpline info based on location. Default is UK.
#     """
#     print("suicide_hotline_lookup CALLED with:", location)
#     return "If you are in danger or thinking about suicide, please call the Samaritans at 116 123 (UK) or your local helpline."

# @tool
# def emergency_response_tool(user_message: str) -> str:
#     """
#     Generates an urgent response in crisis situations.
#     """
#     print("emergency_response_tool CALLED with:", user_message)
#     return "It sounds like you're in crisis. Please reach out immediately to a trained professional or call your local emergency helpline."
