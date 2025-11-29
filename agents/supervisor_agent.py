from langchain.agents import create_agent
from xml.parsers.expat import model

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