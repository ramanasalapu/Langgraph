from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
# print(openai_api_key)


# Initialise the ChatOpenAI LLM Model
model = ChatOpenAI(model='gpt-4o-mini', api_key=openai_api_key)
# print(model)


#Node function to handle User Query and to call LLM
def call_llm(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages[-1].content)
    return {"messages": [response]}

# Define Graph flow
workflow = StateGraph(MessagesState)

# add the node to call the LLM
workflow.add_node("call_llm", call_llm)

# Define the Edges
workflow.add_edge(START, "call_llm")
workflow.add_edge("call_llm", END)

# Compile the workflow
app = workflow.compile()

# sample User Input message
input_message ={"messages": [("human", "what's the capital of Kenya?")]}

# Run the workflow
for chunk in app.stream(input_message, stream_mode='values'):
    chunk["messages"][-1].pretty_print()
