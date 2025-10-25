from typing_extensions import TypedDict
from typing import Annotated
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

from .llm_client import get_llm
from .tools import build_tools

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def build_graph():
    llm = get_llm()
    tools = build_tools()
    # bind tools onto llm
    llm_with_tools = llm.bind_tools(tools=tools)

    def tool_calling_llm(state: State):
        # state["messages"] should be a list of AnyMessage (e.g., HumanMessage)
        return {"messages": [llm_with_tools.invoke(state["messages"]) ]}

    builder = StateGraph(State)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", "tool_calling_llm")
    graph = builder.compile()
    return graph


def run_graph(graph, user_text: str):
    # create initial message and invoke graph
    from langchain_core.messages import HumanMessage
    messages = graph.invoke({"messages": [HumanMessage(content=user_text)]})
    return messages