from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver



from langgraph.graph.message import add_messages

class MessageState(TypedDict):

    messages : Annotated[list[BaseMessage], add_messages]



llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.3
)

def chat_node(state: MessageState):
    messages = state['messages']

    response = llm.invoke(messages)

    return {'messages':[response]}


graph = StateGraph(MessageState)

checkpointer = MemorySaver()

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

compiled_graph = graph.compile(checkpointer=checkpointer)

thread_id = '1'

while True:

    user_input = input("Type here: ")

    print("User_msg: ",user_input)

    if user_input.strip().lower() in ['exit','quit','bye']:
        break

    config = {'configurable':{'thread_id':thread_id}}

    response = compiled_graph.invoke({'messages':[HumanMessage(content=user_input)]},config=config)

    print("AI_msg: ",response['messages'][-1].content)




















