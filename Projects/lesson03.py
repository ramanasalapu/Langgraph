from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

#Define a Simple State class
class HelloWorldState(TypedDict):
    message: str

#initializing the state
state ={"message": "Hi!"}


def hello_world_node(state: HelloWorldState):
    state["message"]="Hello World"
    return state


builder_graph = StateGraph(HelloWorldState)
builder_graph.add_node()
