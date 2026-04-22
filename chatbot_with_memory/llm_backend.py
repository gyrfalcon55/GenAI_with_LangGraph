from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import os 



conn = sqlite3.connect(database='chatBot_db/chatbot.db', check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

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


workflow = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)





















































