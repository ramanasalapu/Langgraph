from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# define state types
class OverallState(TypedDict):
    partial_message: str
    user_input: str
    output_message: str

class InputState(TypedDict):
    user_input : str

class OutputState(TypedDict):
    output_message : str

class PrivateState(TypedDict):
    private_message: str


# define node functions
def add_world(state: InputState)-> OverallState:
    partial_message = state['user_input'] + " World"
    print(f"Node 1 - add_world: Transformed '{state['user_input']}' to '{partial_message}'")
    return {"partial_message": partial_message, "user_input": state["user_input"], "output_message": ""}

def add_exclamation(state: OverallState) -> PrivateState:
    private_message = state["partial_message"] + "!"
    print(f"Node 2 - add_exclamation: Transformed '{state["partial_message"]}' to '{private_message}'")
    return {"private_message": private_message}

def final_message(state: PrivateState) -> OutputState:
    output_message=state["private_message"]
    print(f"Node 3 - final_message: finalized message to '{output_message}'")
    return {"output_message": output_message}


# Build Graph
builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
builder.add_node("add_world", add_world)
builder.add_node("add_exclamation", add_exclamation)
builder.add_node("final_message", final_message)

# Define Edges (Connectivity)
builder.add_edge(START, "add_world")
builder.add_edge("add_world", "add_exclamation")
builder.add_edge("add_exclamation", "final_message")
builder.add_edge("final_message", END)

graph = builder.compile()
result = graph.invoke({"user_input": "Hello"})
print(result)
