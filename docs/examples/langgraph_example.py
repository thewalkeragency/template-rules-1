from langchain_core.messages import HumanMessage
from langgraph.graph import MessageGraph, END

# Define a simple node
def simple_responder(state):
    return HumanMessage(content="Hello! How can I help you today?")

# Create the graph
graph = MessageGraph()
graph.add_node("responder", simple_responder)
graph.set_entry_point("responder")
graph.add_edge("responder", END)

# Compile and run the graph
app = graph.compile()
result = app.invoke(HumanMessage(content="Hi"))
print(result)

# To run this example:
# 1. Install langgraph and langchain-core: pip install langgraph langchain-core
# 2. Save the code and run it: python langgraph_example.py
