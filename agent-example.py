import os
import getpass
from xml.parsers.expat import model
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent



def __init__():
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
    
    ## sub-agents as tools
    @tool
    def schedule_basic(request: str) -> str:
        """Schedule calendar events using natural language.

        Use this when the user wants to create, modify, or check calendar appointments.
        Handles date/time parsing, availability checking, and event creation.

        Input: Natural language scheduling request (e.g., 'meeting with design team
        next Tuesday at 2pm')
        """
        result = basic_agent.invoke({
            "messages": [{"role": "user", "content": request}]
        })
        return result["messages"][-1].text


    @tool
    def schedule_advice(request: str) -> str:
        """Send emails using natural language.

        Use this when the user wants to send notifications, reminders, or any email
        communication. Handles recipient extraction, subject generation, and email
        composition.

        Input: Natural language email request (e.g., 'send them a reminder about
        the meeting')
        """
        result = advice_agent.invoke({
            "messages": [{"role": "user", "content": request}]
        })
        return result["messages"][-1].text
    
    ## supervisor agent 

    SUPERVISOR_PROMPT = (
    "You are a helpful personal assistant. "
    "You can choose to give a greeting or advice to patients. "
    "Break down user requests into appropriate tool calls and coordinate the results. "
    "When a request involves multiple actions, use multiple tools in sequence."
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

__init__()