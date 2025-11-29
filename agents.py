import os
from xml.parsers.expat import model
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.agents import create_agent
from tools import (greet_user, response_to_greeting,
                   provide_anxiety_advice, suggest_resources,
                   small_talk_tool, positive_reinforcement_tool,
                   suicide_hotline_lookup, emergency_response_tool,
                   relationship_advice_tool, communication_tips_tool,
                   moderation_tool, rephrase_tool)

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


model = init_chat_model("gpt-5")

# Greeting agent 
GREETING_AGENT_PROMPT = (
    "You are a friendly greeting agent in a group therapy chat. "
    "Your task is to recognize greetings from the user and respond politely. "
    "Extract the user's name if given, and respond with a short, kind greeting. "
    "Keep it concise and positive. Respond in a single line."
    )

greeting_agent = create_agent(
    model,
    tools=[greet_user, response_to_greeting],
    system_prompt=GREETING_AGENT_PROMPT,
)

# Anxiety agent definition
ANXIETY_AGENT_PROMPT = (
    "You are an anxiety-focused therapist agent. "
    "Your task is to provide thoughtful, empathetic advice to users expressing anxiety, stress, or worry. "
    "Always respond with understanding and actionable suggestions. "
    "Keep responses calm, reassuring, and concise. Only respond with the advice — do not include explanations about your role."
)

anxiety_agent = create_agent(
    model,
    tools=[provide_anxiety_advice, suggest_resources],
    system_prompt=ANXIETY_AGENT_PROMPT,
)

# Friend agent 
FRIEND_AGENT_PROMPT = (
    "You are a friendly, supportive conversational agent. "
    "Your goal is to engage in a warm, encouraging conversation with the user. "
    "Offer relatable advice, positive reinforcement, or small talk that makes the user feel supported. "
    "Keep responses conversational, kind, and concise."
    )

friend_agent = create_agent(
    model,
    tools=[small_talk_tool, positive_reinforcement_tool],
    system_prompt=FRIEND_AGENT_PROMPT,
)

# Helpline agent 
HELPLINE_AGENT_PROMPT = (
    "You are a helpline support agent. "
    "Your task is to respond to users in crisis, including suicidal thoughts, urgent mental health needs, or requests for help. "
    "Provide immediate support, calming language, and resources such as helpline contacts. "
    "Always prioritize the user's safety. Keep responses clear, empathetic, and concise."
)

helpline_agent = create_agent(
    model,
    tools=[suicide_hotline_lookup, emergency_response_tool],
    system_prompt=HELPLINE_AGENT_PROMPT,
)

# Relationship agent 
RELATIONSHIP_AGENT_PROMPT = (
    "You are a relationship therapist agent. "
    "Your task is to help users with relationship issues or questions, including friendships, family, or romantic relationships. "
    "Provide understanding, thoughtful advice, and constructive suggestions. "
    "Keep responses supportive, professional, and concise."
    )

relationship_agent = create_agent(
    model,
    tools=[relationship_advice_tool, communication_tips_tool],
    system_prompt=RELATIONSHIP_AGENT_PROMPT,
)

# Warden agent 
WARDEN_AGENT_PROMPT = (
    "You are a chat moderation agent. "
    "Your task is to ensure the chat remains safe, lawful, and respectful. "
    "Do not allow cursing, rude language, harassment, or illegal topics. "
    "If necessary, gently warn the user or rephrase messages politely. "
    "Keep moderation messages concise and professional."
    )

warden_agent = create_agent(
    model,
    tools=[moderation_tool, rephrase_tool],
    system_prompt=WARDEN_AGENT_PROMPT,
)
