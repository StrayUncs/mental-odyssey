import os
import getpass
from xml.parsers.expat import model
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent

basic_agent = None
advice_agent = None

def __init__():
    global basic_agent, advice_agent
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    
    model = init_chat_model("gpt-5")

    BASIC_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    )

    basic_agent = create_agent(
        model,
        tools=[greeting_tool],
        system_prompt=BASIC_AGENT_PROMPT,
    )

    # query = "Hello, my name is Bob, I did not self harm today."

    # for step in basic_agent.stream(
    #     {"messages": [{"role": "user", "content": query}]}
    # ):
    #     for update in step.values():
    #         for message in update.get("messages", []):
    #             message.pretty_print()

    ## second agent - advice 
    ADVICE_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    )
    
    advice_agent = create_agent(
        model,
        tools=[advice_tool],
        system_prompt=ADVICE_AGENT_PROMPT,
    )

    # query = "Hello, my name is Alice, I did self harm today."

    # for step in advice_agent.stream(
    #     {"messages": [{"role": "user", "content": query}]}
    # ):
    #     for update in step.values():
    #         for message in update.get("messages", []):
    #             message.pretty_print()
    
    ## supervisor agent 

    SUPERVISOR_PROMPT = (
        "You are a helpful personal assistant. "
        "You MUST decide whether to call one of these tools: schedule_basic(request) or schedule_advice(request). "
        "Use schedule_basic when the user asks to create, modify, or check calendar events, availability, or meeting times. "
        "Use schedule_advice when the user asks to send notifications, reminders, or any email-like communication. "
        "When you decide to call a tool, OUTPUT EXACTLY one line beginning with: CALL_TOOL: <tool_name>(<natural language request>) "
        "For example, If the user says they did not self harm, respond: "
        "CALL_TOOL: schedule_basic('good job not harming yourself') "
        "If the user says they did self harm respond: "
        "CALL_TOOL: schedule_advice('take care and seek help if needed') "
        "After the tool runs and returns its result, include the tool result verbatim and then continue with any follow-up message to the user. "
        "Do not invent or guess tool outputs — always call the appropriate tool and relay its returned text. "
        "If no tool is needed, answer directly as the assistant without calling any tools."
    )

    supervisor_agent = create_agent(
        model,
        tools=[schedule_basic, schedule_advice],
        system_prompt=SUPERVISOR_PROMPT,
    )

    query = "Hello, my name is Bob, I did not self harm today."

    for step in supervisor_agent.stream(
        {"messages": [{"role": "user", "content": query}]}
    ):
        for update in step.values():
            for message in update.get("messages", []):
                message.pretty_print()
            

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
    """Schedule calendar events using natural language.

    Use this when the user wants to create, modify, or check calendar appointments.
    Handles date/time parsing, availability checking, and event creation.

    Input: Natural language scheduling request (e.g., 'meeting with design team
    next Tuesday at 2pm')
    """
    global basic_agent
    if basic_agent is None:
        raise RuntimeError("basic_agent not initialized")
    print("schedule_basic CALLED with:", request)
    result = basic_agent.invoke({"messages": [{"role": "user", "content": request}]})
    print("BASIC TOOL RAW RESULT:", result)
    # normalize common return shapes to a string
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)


@tool
def schedule_advice(request: str) -> str:
    """Send emails using natural language.

    Use this when the user wants to send notifications, reminders, or any email
    communication. Handles recipient extraction, subject generation, and email
    composition.

    Input: Natural language email request (e.g., 'send them a reminder about
    the meeting')
    """

    global advice_agent
    if advice_agent is None:
        raise RuntimeError("advice_agent not initialized")
    print("schedule_advice CALLED with:", request)
    result = advice_agent.invoke({"messages": [{"role": "user", "content": request}]})
    print("ADVICE TOOL RAW RESULT:", result)
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "text", None) or getattr(last, "content", None) or str(last)
    return str(result)

__init__()