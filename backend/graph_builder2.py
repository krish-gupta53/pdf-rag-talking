from state_schema import State
from langgraph.graph import StateGraph, START, END
from retrieved_ans import retrieved_ans
from llm_response import llm_response

graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("retrieved_ans", retrieved_ans)
graph_builder.add_node("llm_response", llm_response)

# Add edges
graph_builder.add_edge(START, "retrieved_ans")
graph_builder.add_edge("retrieved_ans", "llm_response")
graph_builder.add_edge("llm_response", END)

build_agent_graphh = graph_builder.compile()
