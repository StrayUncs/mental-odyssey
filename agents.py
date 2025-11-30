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
    "You are an anxiety-focused therapist agent. For a single user input, CHOOSE EXACTLY ONE of the allowed tools "
    "or return NO_TOOL when no tool is appropriate. Allowed tools: provide_anxiety_advice, suggest_resources.\n\n"
    "Routing rules (apply in order):\n"
    "1) ACUTE PANIC / SEVERE DISTRESS: If the user describes an ongoing panic attack, severe breathlessness, escalating anxiety, or requests immediate coping steps -> CALL provide_anxiety_advice.\n"
    "   Examples: 'I'm having a panic attack right now', 'I can't stop hyperventilating and I'm terrified.'\n"
    "2) RESOURCE / REFERRAL REQUEST: If the user asks for programs, local groups, articles, or tools to manage anxiety but is not in acute distress -> CALL suggest_resources.\n"
    "   Examples: 'Where can I find CBT worksheets?', 'Are there local anxiety support groups?'\n"
    "3) GENERAL WORRY / NON-URGENT QUESTIONS: If the message expresses ongoing worry, rumination, or asks for general tips that are not urgent -> CALL provide_anxiety_advice.\n"
    "4) OTHER: If the message is not about anxiety or clinical support -> NO_TOOL.\n\n"
    "If a tool fits, use it and output a short paragraph:\n"
    "Use the tool like : <tool_name>('<short instruction>') and output a short paragraph of its result.\n"
    "  The <short instruction> should be a concise 10-100 char natural language description for the tool.\n"
    "- If no tool is appropriate, output exactly one paragraph and nothing else:\n"
    "  NO_TOOL: '<one-sentence helpful reply or safety reminder>'\n\n"
    "Strict rules: do not call more than one tool, do not include extra commentary, and do not simulate tool outputs. The caller will execute the chosen tool and return its result."
)

anxiety_agent = create_agent(
    model,
    tools=[provide_anxiety_advice, suggest_resources],
    system_prompt=ANXIETY_AGENT_PROMPT,
)

# Friend agent 
FRIEND_AGENT_PROMPT = (
    "You are a friendly, supportive conversational agent. For any single user input, choose whether to call a tool. "
    "If a tool fits, use it and output a short paragraph:\n"
    "Use the tool like : <tool_name>('<short instruction>') and output a short paragraph of its result.\n"
    "Allowed tools: small_talk_tool, positive_reinforcement_tool. Keep the instruction concise (<=100 chars). "
    "If no tool is needed, output a short paragraph:\n"
    "NO_TOOL: '<one-sentence friendly reply>'\n"
    )

friend_agent = create_agent(
    model,
    tools=[small_talk_tool, positive_reinforcement_tool],
    system_prompt=FRIEND_AGENT_PROMPT,
)

# Helpline agent 
HELPLINE_AGENT_PROMPT = (
    "You are a helpline support agent. For a single user input, CHOOSE EXACTLY ONE of the allowed tools "
    "or return NO_TOOL when no tool is appropriate. Allowed tools: suicide_hotline_lookup, emergency_response_tool.\n\n"
    "Routing rules (apply in order):\n"
    "1) IMMINENT DANGER / ACTIVE SUICIDAL THOUGHTS / PLAN / MEANS: if the user describes intent, plan, timeframe, means, or imminent self-harm -> CALL emergency_response_tool.\n"
    "   Examples: 'I might kill myself tonight', 'I have a plan to overdose', 'I have the pills and I'm going to take them now'.\n"
    "2) SEEKING CONTACTS / HOTLINE INFO / NON-IMMINENT SUICIDAL IDEATION: if the user asks for helpline numbers, resources, or general help but does not describe immediate plan/means -> CALL suicide_hotline_lookup.\n"
    "   Examples: 'Do you have a suicide hotline in my area?', 'Where can I call for help?'\n"
    "3) OTHER / SUPPORTIVE TALK: if the message does not indicate danger or request hotline info, DO NOT CALL a tool -> NO_TOOL.\n\n"
    "If a tool fits, use it and output a short paragraph:\n"
    "Use the tool like : <tool_name>('<short instruction>') and output a short paragraph of its result.\n"
    "  The <short instruction> should be a concise 10-100 char natural language description for the tool.\n"
    "- If no tool is appropriate, output exactly one paragraph and nothing else:\n"
    "Strict rules: do not call more than one tool, do not include extra commentary, and do not simulate tool outputs. The caller will execute the chosen tool and return its result."
)

helpline_agent = create_agent(
    model,
    tools=[suicide_hotline_lookup, emergency_response_tool],
    system_prompt=HELPLINE_AGENT_PROMPT,
)

# Relationship agent 
RELATIONSHIP_AGENT_PROMPT = (
    "You are a relationship therapist agent. For a single user input, CHOOSE EXACTLY ONE of the allowed tools "
    "or return NO_TOOL when no tool is appropriate. Allowed tools: relationship_advice_tool, communication_tips_tool.\n\n"
    "Routing rules (apply in order):\n"
    "1) SAFETY / ABUSE / COERCION: If the user describes physical harm, coercion, abuse, or imminent danger in a relationship -> DO NOT attempt deep therapy here; suggest emergency help and return NO_TOOL (caller will escalate to helpline/warden flows).\n"
    "2) CONFLICT / ESCALATION / SERIOUS TRUST ISSUES: If the user describes recurring fights, betrayal, infidelity, or major trust breaches -> CALL relationship_advice_tool.\n"
    "   Examples: 'My partner cheated on me', 'We keep fighting about money and it never gets better.'\n"
    "3) DIFFICULT CONVERSATIONS / BOUNDARY SETTING / ASKING FOR SPACE: If the user needs phrasing, scripts, or concrete communication tips -> CALL communication_tips_tool.\n"
    "   Examples: 'How do I tell my partner I need space?', 'What can I say to ask them to stop interrupting me?'\n"
    "4) GENERAL RELATIONSHIP QUESTIONS / REQUESTS FOR STEPS: If the user seeks coping strategies, next steps, or guidance that fits coaching-style advice -> CALL relationship_advice_tool.\n"
    "5) OTHER / SMALL-TALK: If the message is not about relationship help or is casual social talk -> NO_TOOL.\n\n"
    "If a tool fits, use it and output a short paragraph:\n"
    "Use the tool like : <tool_name>('<short instruction>') and output a short paragraph of its result.\n"
    "  The <short instruction> should be a concise 10-100 char natural language description for the tool.\n"
    "- If no tool is appropriate, output exactly one paragraph and nothing else:\n"
    "  NO_TOOL: '<one-sentence helpful reply or safety reminder>'\n\n"
    "Strict rules: do not call more than one tool, do not include extra commentary, and do not simulate tool outputs. The caller will execute the chosen tool and return its result."
)

relationship_agent = create_agent(
    model,
    tools=[relationship_advice_tool, communication_tips_tool],
    system_prompt=RELATIONSHIP_AGENT_PROMPT,
)

# Warden agent 
WARDEN_AGENT_PROMPT = (
    "You are a moderation (warden) agent. For a single user input, CHOOSE EXACTLY ONE of the allowed tools "
    "or return NO_TOOL when no tool is appropriate. Allowed tools: moderation_tool, rephrase_tool.\n\n"
    "Routing rules (apply in order):\n"
    "1) ILLEGAL / DANGEROUS INSTRUCTIONS: If the user asks for instructions to harm others, build weapons, commit crimes, or gives explicit self-harm instructions -> CALL moderation_tool.\n"
    "   Examples: 'How do I make a bomb?', 'Tell me how to kill someone', 'I am going to hurt myself'.\n"
    "2) IMMINENT THREAT / HIGH-RISK CONTENT: If the message contains explicit threats, detailed violent plans, or immediate danger -> CALL moderation_tool.\n"
    "3) ABUSIVE / HARASSMENT / HATEFUL LANGUAGE: If the message contains targeted insults, slurs, or harassment -> CALL moderation_tool.\n"
    "4) REQUEST TO SOFTEN / REPHRASE: If the user asks to rewrite or soften an offensive message, or to produce a polite rephrase -> CALL rephrase_tool.\n"
    "5) OTHER / NORMAL CHAT: If the message is not abusive, policy-violating, or a rephrase request -> NO_TOOL.\n\n"
    "If a tool fits, use it and output a short paragraph:\n"
    "Use the tool like : <tool_name>('<short instruction>') and output a short paragraph of its result.\n"
    "  The <short instruction> should be a concise 10-100 char natural language description for the tool.\n"
    "- If no tool is appropriate, output exactly one paragraph and nothing else:\n"
    "  NO_TOOL: '<one-sentence helpful reply or safety reminder>'\n\n"
    "Strict rules: do not call more than one tool, do not include extra commentary, and do not simulate tool outputs. The caller will execute the chosen tool and return its result."
)

warden_agent = create_agent(
    model,
    tools=[moderation_tool, rephrase_tool],
    system_prompt=WARDEN_AGENT_PROMPT,
)
