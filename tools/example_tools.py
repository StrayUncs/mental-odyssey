from langchain.tools import tool

@tool
def greeting_tool(
    name: str,
    sentence: str
) -> str:
    """You compliment the patient on how well they are doing"""
    print("being called")
    return f"You are doing well, {name}, sentence: {sentence}"

@tool
def advice_tool(
    name: str,
    sentence: str
) -> str:
    """You advise the patient on how to deal with their self harm urges"""
    print("being called")
    return f"Take your time, breathe {name}, sentence: {sentence}"

## sub-agents as tools
@tool
def schedule_basic(request: str) -> str:
    """Schedules basic greeting messages.
    """
    global basic_agent
    if basic_agent is None:
        raise RuntimeError("basic_agent not initialized")
    print("schedule_basic CALLED with:", request)
    result = basic_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # print("BASIC TOOL RAW RESULT:", result)
    # normalize common return shapes to a string
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)


@tool
def schedule_advice(request: str) -> str:
    """Schedules advice messages.
    """

    global advice_agent
    if advice_agent is None:
        raise RuntimeError("advice_agent not initialized")
    print("schedule_advice CALLED with:", request)
    result = advice_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # print("ADVICE TOOL RAW RESULT:", result)
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)
