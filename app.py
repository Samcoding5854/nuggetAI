# app.py

import streamlit as st
from kb.retrieve import retrieve_resto_data
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from prompts.prompts import generate_system_prompt

# You need to set your Google API key
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCVxDGFJS_Aw0dDCe3UHY_7Tbf0T3Hq3EU"


# Initialize Streamlit app
st.title("🍽️ Restaurant Chatbot")

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = None
if "chain" not in st.session_state:
    st.session_state.chain = None
if "restaurant_data" not in st.session_state:
    st.session_state.restaurant_data = None
if "data_retrieved" not in st.session_state:
    st.session_state.data_retrieved = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about a restaurant..."):

    # Show user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # First message: retrieve restaurant data
    if not st.session_state.data_retrieved:
        # 1. Retrieve restaurant data
        restaurant_data = retrieve_resto_data(prompt)
        st.session_state.restaurant_data = restaurant_data
        st.session_state.data_retrieved = True

        # 2. Create a system prompt
        system_prompt = generate_system_prompt(restaurant_data)

        # 3. Initialize the memory
        memory = ConversationBufferMemory(memory_key="history", input_key="input", return_messages=True)

        # 4. Setup the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.2,
            system_message=system_prompt,
            convert_system_message_to_human=True
        )

        # 5. Setup the conversation chain
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)

        # Save in session state
        st.session_state.memory = memory
        st.session_state.chain = chain

    # After data retrieved: continue chatting
    chain = st.session_state.chain
    response = chain.predict(input=prompt)

    # Display assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
