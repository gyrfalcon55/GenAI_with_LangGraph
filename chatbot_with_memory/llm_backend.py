from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


checkpoint = InMemorySaver()

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.3
)

class ChatBot(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def Input(state: ChatBot):
    user_input = state['messages']
    result = llm.invoke(user_input)

    return {'messages':[result]}

graph = StateGraph(ChatBot)

graph.add_node('User_input',Input)

graph.add_edge(START,'User_input')
graph.add_edge('User_input',END)

workflow = graph.compile(checkpointer=checkpoint)





















































