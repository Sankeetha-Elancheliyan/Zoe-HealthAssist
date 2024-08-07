import streamlit as st
from streamlit import columns
from model import models_response, messages_user
import time
import pandas as pd
from appoint import get_indent
from sql import insert_data , retrieve_appointments

st.set_page_config(initial_sidebar_state="collapsed")

st.title("Hospital Assistant Chatbot")
# Create a container for the tab container
tab_container = st.container()

# Create a container for the chat history
chat_container = st.container()

# Create an empty element to hold the chat input
input_container = st.empty()

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if not st.session_state.password_correct:
        password = st.sidebar.text_input("Enter admin password", type="password")
        if password == "admin123":
            st.session_state.password_correct = True
        else:
            st.sidebar.error("Incorrect password")
    
    return st.session_state.password_correct

with tab_container:
    tab1, tab2 = st.tabs(["Chat", "Appointments"])


with tab1:
    # st.title("Hospital Assistant Chatbot")
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = time.time()

    if "chat_closed" not in st.session_state:
        st.session_state.chat_closed = False

    def get_conversation_text(messages):
        conversation = []
        for message in messages:
            if message["role"] != "system" :
                conversation.append(f"{message['role'].capitalize()}: {message['content']}")
        return "\n".join(conversation)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = messages_user.copy()

    if not st.session_state.chat_closed:
        # Display chat messages from history on app rerun
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] != "system":
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
        
        # React to user input
        with input_container:
            if prompt := st.chat_input("What can I help you with?"):
                # Display user message in chat message container
                with chat_container:
                    st.chat_message("user").markdown(prompt)
                
                with st.spinner("Assistant is thinking..."):
                    # Add user message to chat history
                    st.session_state.messages, response = models_response(st.session_state.messages, prompt)
                    print(st.session_state.messages)
                
                # Display assistant response in chat message container
                with chat_container:
                    st.chat_message("assistant").markdown(response)

        current_time = time.time()
        if current_time - st.session_state.last_activity > 300:  # 5 minutes
            conversation_text = get_conversation_text(st.session_state.messages)
            res = get_indent(conversation_text)
            insert_data(res)
            st.session_state.chat_closed = True
            st.warning("Chat closed due to inactivity. Conversation saved.")
        else:
            st.session_state.last_activity = current_time

        if st.button("Close Chat"):
            conversation_text = get_conversation_text(st.session_state.messages)
            res = get_indent(conversation_text)
            insert_data(res)
            st.session_state.chat_closed = True
            st.success("Chat closed. Conversation saved.")

    else:
        st.info("Chat is closed. Start a new conversation to continue.")
        if st.button("Start New Chat"):
            st.session_state.messages = messages_user.copy()
            st.session_state.chat_closed = False
            st.experimental_rerun()

with tab2:
    if check_password():
        st.title("Appointments")
        appointments = retrieve_appointments()
        
        if not appointments:
            st.info("No appointments found.")
        else:
            # Convert appointments to a pandas DataFrame
            df = pd.DataFrame(appointments, columns=['Patient', 'Contact', 'Reason', 'Doctor', 'Date', 'Time'])
            
            # Display the DataFrame as a table
            st.table(df)

        if st.button("Refresh Appointments"):
            st.rerun()
    else:
        st.warning("This tab is only accessible to admins. Please enter the admin password in the sidebar.")
