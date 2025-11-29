import os
from xml.parsers.expat import model
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


model = init_chat_model("gpt-5")

# greeting agent 
GREETING_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    "Please only respond with a single line advice message."
    )

greeting_agent = create_agent(
    model,
    tools=[greeting_tool],
    system_prompt=GREETING_AGENT_PROMPT,
)

# anxiety agent definition
ANXIETY_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    "Please only respond with a single line greeting message."
    )

anxiety_agent = create_agent(
    model,
    tools=[greeting_tool],
    system_prompt=ANXIETY_AGENT_PROMPT,
)

# friend agent 
FRIEND_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    "Please only respond with a single line advice message."
    )

friend_agent = create_agent(
    model,
    tools=[greeting_tool],
    system_prompt=FRIEND_AGENT_PROMPT,
)

# helpline agent 
HELPLINE_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    "Please only respond with a single line greeting message."
    )

helpline_agent = create_agent(
    model,
    tools=[greeting_tool],
    system_prompt=BASIC_AGENT_PROMPT,
)

# relationship agent 
RELATIONSHIP_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    "Please only respond with a single line advice message."
    )

relationship_agent = create_agent(
    model,
    tools=[greeting_tool],
    system_prompt=RELATIONSHIP_AGENT_PROMPT,
)

# supervisor agent 
SUPERVISOR_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    "Please only respond with a single line greeting message."
    )

supervisor_agent = create_agent(
    model,
    tools=[greeting_tool],
    system_prompt=SUPERVISOR_AGENT_PROMPT,
)

# warden agent 
WARDEN_AGENT_PROMPT = (
    "You are a greeting agent"
    "Please parse the natural language greeting from the user into name and sentence"
    "Now output back a nice greeting to the user"
    "Please only respond with a single line advice message."
    )

warden_agent = create_agent(
    model,
    tools=[greeting_tool],
    system_prompt=WARDEN_AGENT_PROMPT,
)
