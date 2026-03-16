from langgraph.graph import StateGraph
from langgraph.graph import END
from agents import ResearchState, searcher_node, writer_node, planner_node

# Create Graph
graph = StateGraph(ResearchState)

# Add nodes
graph.add_node("planner_node", planner_node)
graph.add_node("writer_node", writer_node)
graph.add_node("searcher_node", searcher_node)

# Set edges
graph.add_edge("planner_node", "searcher_node")
graph.add_edge("searcher_node", "writer_node")
graph.add_edge("writer_node", END)

# Set entry point
graph.set_entry_point("planner_node")

# Compile
app = graph.compile()
