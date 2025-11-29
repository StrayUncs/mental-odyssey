import os
import getpass
from xml.parsers.expat import model
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from agents import anxiety_agent, greeting_agent, friend_agent, helpline_agent, relationship_agent, warden_agent

def __init__():
    global supervisor_agent
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    
    model = init_chat_model("gpt-5")
    
    ## supervisor agent 

    SUPERVISOR_PROMPT = (
        "You are a supervisor router whose job is to examine a single user input and choose EXACTLY one tool to handle it. "
        "Available tools (choose one): schedule_helpline, schedule_warden, schedule_anxiety, schedule_friend, schedule_relationship, schedule_greeting. "
        "Apply these rules in order and pick the first that matches:\n"
        "1) IMMINENT SELF-HARM / DANGER: If the user expresses intent, plan, means, imminent danger, or requests emergency help -> CALL schedule_helpline.\n"
        "2) POLICY / SAFETY / INAPPROPRIATE: If the message is illegal, sexually explicit, violent, abusive, or otherwise violates safety -> CALL schedule_warden.\n"
        "3) ANXIETY / PANIC / STRESS: If the user expresses worry, panic, chronic anxiety, or asks for coping strategies -> CALL schedule_anxiety.\n"
        "4) FRIENDLY SUPPORT / CHECK-IN: If the user wants casual encouragement, companionship, or a friendly check-in -> CALL schedule_friend.\n"
        "5) RELATIONSHIP HELP: If the user asks about relationships, conflict resolution, communication, or partner issues -> CALL schedule_relationship.\n"
        "6) GREETING / INTRODUCTION: If the input is a greeting, self-introduction, or simple social salutation -> CALL schedule_greeting.\n\n"
    )

    supervisor_agent = create_agent(
        model,
        tools=[schedule_anxiety, schedule_friend, schedule_greeting, schedule_helpline, schedule_relationship, schedule_warden],
        system_prompt=SUPERVISOR_PROMPT,
    )

## sub-agents as tools
@tool
def schedule_greeting(request: str) -> str:
    """Schedules basic greeting messages.
    """
    global greeting_agent
    if greeting_agent is None:
        raise RuntimeError("greeting_agent not initialized")
    print("schedule_greeting CALLED with:", request)
    result = greeting_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # print("GREETING TOOL RAW RESULT:", result)
    # normalize common return shapes to a string
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)


@tool
def schedule_friend(request: str) -> str:
    """Schedules messages to be a friend for support.
    """
    global friend_agent
    if friend_agent is None:
        raise RuntimeError("friend_agent not initialized")
    print("schedule_friend CALLED with:", request)
    result = friend_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # print("FRIEND TOOL RAW RESULT:", result)
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)

@tool
def schedule_anxiety(request: str) -> str:
    """Schedules anxiety related help messages.
    """
    global anxiety_agent
    if anxiety_agent is None:
        raise RuntimeError("anxiety_agent not initialized")
    print("schedule_anxiety CALLED with:", request)
    result = anxiety_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # print("ANXIETY TOOL RAW RESULT:", result)
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)

@tool
def schedule_helpline(request: str) -> str:
    """Schedules helpline support messages for very serious issues.
    """
    global helpline_agent
    if helpline_agent is None:
        raise RuntimeError("helpline_agent not initialized")
    print("schedule_helpline CALLED with:", request)
    result = helpline_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # print("HELPLINE TOOL RAW RESULT:", result)
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)

@tool
def schedule_relationship(request: str) -> str:
    """Schedules relationship support messages.
    """
    global relationship_agent
    if relationship_agent is None:
        raise RuntimeError("relationship_agent not initialized")
    print("schedule_relationship CALLED with:", request)
    result = relationship_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # print("RELATIONSHIP TOOL RAW RESULT:", result)
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)

@tool
def schedule_warden(request: str) -> str:
    """Schedules redirect messages for invalid or inappropriate inputs.
    """
    global warden_agent
    if warden_agent is None:
        raise RuntimeError("warden_agent not initialized")
    print("schedule_warden CALLED with:", request)
    result = warden_agent.invoke({"messages": [{"role": "user", "content": request}]})
    # print("WARDEN TOOL RAW RESULT:", result)
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)

# function to run queries from other files
def run_query(query: str) -> str:
    global supervisor_agent
    if supervisor_agent is None:
        __init__()  # lazy init if not already done
    tool_output = None
    for step in supervisor_agent.stream({"messages": [{"role": "user", "content": query}] }):
        for update in step.values():
            if isinstance(update, dict):
                for key in ("tool_result", "tool_response", "tool_output", "result"):
                    if key in update and update[key]:
                        tool_output = update[key]
                for m in update.get("messages", []):
                    tool_output = getattr(m, "content", None) or getattr(m, "text", None) or tool_output
            else:
                if hasattr(update, "tool_result") and getattr(update, "tool_result"):
                    tool_output = getattr(update, "tool_result")
                for m in getattr(update, "messages", []) or []:
                    tool_output = getattr(m, "content", None) or getattr(m, "text", None) or tool_output
        if tool_output:
            return tool_output
    return ""

__init__()
