import os
import getpass
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

    query = "Hello, my name is Bob, I did not self harm today."

    for step in basic_agent.stream(
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

__init__()