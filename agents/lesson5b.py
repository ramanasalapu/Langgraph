import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model='gpt-4o-mini', api_key=openai_api_key)


def call_llm(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages[-1].content)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)
workflow.add_node("call_llm", call_llm)

workflow.add_edge(START, "call_llm")
workflow.add_edge("call_llm", END)

app = workflow.compile()

def interact_with_agent():
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("ending the conversations")
        break

    input_message = {"messages": [("human", user_input)]}

    for chunk in app.stream(input_message, stream_mode='values'):
        chunk["messages"][-1].pretty_print()

interact_with_agent()
