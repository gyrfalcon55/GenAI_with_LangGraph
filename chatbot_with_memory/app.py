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

    result = workflow.invoke({'messages':[HumanMessage(content=user_input)]}, config=config)
    ai_message = result['messages'][-1].content

    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    with st.chat_message("assistant"):
        
        st.write(ai_message)

