
# graph.py

from state_schema import State
from langgraph.graph import StateGraph, START, END
from detect_query import detect_query
from upload_pdf import upload_pdf
from deupload_pdf import deupload_pdf


graph_builder = StateGraph(State)
graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("upload_pdf", upload_pdf)
graph_builder.add_node("deupload_pdf", deupload_pdf)

graph_builder.add_conditional_edges(START, detect_query)
graph_builder.add_edge("upload_pdf", END)
graph_builder.add_edge("deupload_pdf", END)

build_agent_graph= graph_builder.compile()
