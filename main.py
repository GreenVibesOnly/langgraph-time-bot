import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from langgraph.graph import MessageGraph, END
from langgraph.prebuilt import ToolNode
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


# Load environment variables
load_dotenv()


# Return current UTC time
@tool
def get_current_time():
    """Return the current UTC time"""
    return {"utc": datetime.now(timezone.utc).isoformat()}


# Wrap tools
tools = [get_current_time]
tool_node = ToolNode(tools)


# Initialize LLM
llm = ChatOpenAI(model="gpt-4o",
                 openai_api_key=os.getenv("OPENAI_API_KEY"))


# Agent prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a very polite and helpful assistant."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


# Create agent and executor
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)


# Decide next step: call tool or end
def should_continue(messages):
    return "call_tool" if getattr(messages[-1], "tool_calls", None) else "end"


# Agent node logic
def run_agent(messages):
    try:
        response = agent_executor.invoke({
            "input": messages[-1].content,  # last user request
            "chat_history": messages
        })
        output = response.get("output", "Sorry, something went wrong.")
    except Exception as e:
        output = f"Error calling model: {str(e)}"
    return messages + [AIMessage(content=output)]


# Build the graph
graph = MessageGraph()
graph.set_entry_point("agent")
graph.add_node("agent", run_agent)
graph.add_node("tools", tool_node)
graph.add_conditional_edges(
    "agent",
    should_continue,
    {"call_tool": "tools", "end": END}
)


# Compile the graph
compiled_graph = graph.compile()


# Register graph
graphs = {
    "graph": compiled_graph
}
