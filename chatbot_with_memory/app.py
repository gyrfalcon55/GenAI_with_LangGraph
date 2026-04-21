from llm_backend import workflow
import streamlit as st 
from langchain.messages import HumanMessage
import uuid
from langchain_core.messages import HumanMessage, AIMessage

st.title("----- My_ChatBot -----")

def genearte_uuid():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = genearte_uuid()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    state = workflow.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])



if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = genearte_uuid()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])




user_input = st.chat_input("Type your message : ")

config = {'configurable':{'thread_id':st.session_state['thread_id']}}

st.sidebar.title('LangGraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    t_id = str(thread_id)
    if st.sidebar.button(f"Conversation_id - {t_id[-4:]}"):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages


if user_input:

    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        def ai_only_stream():
            for message_chunk, metadata in workflow.stream(
                {"messages": [HumanMessage(content=user_input)]},
                stream_mode="messages",
                config=config
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())
        # Store final response
        st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    

