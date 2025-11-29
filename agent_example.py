import os
import getpass
from xml.parsers.expat import model
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent

basic_agent = None
advice_agent = None
supervisor_agent = None

def __init__():
    global basic_agent, advice_agent, supervisor_agent
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    
    model = init_chat_model("gpt-5")

    BASIC_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    "Please only respond with a single line greeting message."
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
    "Please only respond with a single line advice message."
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
        "Use schedule_basic when the user did not self harm "
        "Use schedule_advice when the user did self harm "
        "When you decide to call a tool, OUTPUT EXACTLY one line beginning with: CALL_TOOL: <tool_name>(<tool_result>) "
        "After the tool runs and returns its result, include the tool result verbatim and then continue with any follow-up message to the user. "
        "Do not invent or guess tool outputs — always call the appropriate tool and relay its returned text. "
        "If no tool is needed, answer directly as the assistant without calling any tools."
    )

    supervisor_agent = create_agent(
        model,
        tools=[schedule_basic, schedule_advice],
        system_prompt=SUPERVISOR_PROMPT,
    )

    # for step in supervisor_agent.stream(
    #     {"messages": [{"role": "user", "content": query}]}
    # ):
    #     for update in step.values():
    #         for message in update.get("messages", []):
    #             message.pretty_print()
    
    # tool_output = None
    # for step in supervisor_agent.stream({"messages": [{"role": "user", "content": query}] }):
    #     # inspect every update for common tool-result shapes
    #     for update in step.values():
    #         if isinstance(update, dict):
    #             # common keys
    #             for key in ("tool_result", "tool_response", "tool_output", "result"):
    #                 if key in update and update[key]:
    #                     tool_output = update[key]
    #             # messages array
    #             for m in update.get("messages", []):
    #                 tool_output = getattr(m, "content", None) or getattr(m, "text", None) or tool_output
    #         else:
    #             # object-like updates (some LangChain versions)
    #             if hasattr(update, "tool_result") and getattr(update, "tool_result"):
    #                 tool_output = getattr(update, "tool_result")
    #             for m in getattr(update, "messages", []) or []:
    #                 tool_output = getattr(m, "content", None) or getattr(m, "text", None) or tool_output
    #     if tool_output:
    #         print(tool_output)
    #         break
            

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