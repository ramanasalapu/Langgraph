from typing_extensions import TypedDict  #Define the State Structure
from langgraph.graph import StateGraph, START, END  # define the graph

#Modules for Visualize Graph
from langchain_core.runnables.graph import MermaidDrawMethod
import random
import os
import sys
import subprocess

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

#Code to visualize the Graph

# create an output folder if doesn't exists,for now we can save in the current folder represented by
mermaid_png =graph.get_graph(xray=1).draw_mermaid_png(draw_method=MermaidDrawMethod.API)

output_folder = "."
os.makedirs(output_folder, exist_ok=True)
filename =os.path.join(output_folder, f'graph_{random.randint(1,100000)}.png')

with open(filename, 'wb') as f:
    f.write(mermaid_png)

if sys.platform.startswith('darwin'):
    subprocess.call(('open', filename))
elif sys.platform.startswith('linux'):
    subprocess.call(('xdg-open', filename))
elif sys.platform.startswith('win'):
    os.startfile(filename)
