from llm_backend import workflow
import streamlit as st 
from langchain.messages import HumanMessage

st.title("----- My_ChatBot -----")


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input("Type your message : ")

config = {'configurable':{'thread_id':'1'}}

if user_input:

    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        for message_chunk, metadata in workflow.stream(
            {"messages": [HumanMessage(content=user_input)]},
            stream_mode="messages",
            config=config
        ):
            if message_chunk.content:
                full_response += message_chunk.content
                placeholder.markdown(full_response)

        # Store final response
        st.session_state['message_history'].append({
            'role': 'assistant',
            'content': full_response
        })

    

