from typing_extensions import TypedDict  #Define the State Structure
from langgraph.graph import StateGraph, START, END

class HelloWorldState(TypedDict):
    greeting: str  #This key will store the Greeting message

# Define the node function
def hello_world_node(state: HelloWorldState):
    state['greeting']="Hello World, " +state['greeting']
    return state

# Initialise the graph and add the node
builder =StateGraph(HelloWorldState)
builder.add_node('greet', hello_world_node)

# add edges to graph network
builder.add_edge(START, 'greet')
builder.add_edge('greet', END)

#Compile and run the graph
graph = builder.compile()
result = graph.invoke({"greeting": "from LangGraph!"})
print(result)
