import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage, ChatMessage
from langchain.memory import ConversationBufferMemory
from kb.retrieve import retrieve_resto_data
from prompts.prompts import generate_system_prompt

# 🎓 AI Data Science Tutor - Your interactive learning assistant!
st.title("🍴 Zomato Chatbot 🤖")
st.subheader("🍽️ Your personal assistant for restaurant recommendations, food queries, and dining tips!")

# Set your Google API key
API_KEY = "AIzaSyCVxDGFJS_Aw0dDCe3UHY_7Tbf0T3Hq3EU"

# Initialize AI model with LangChain
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=API_KEY)
memory = ConversationBufferMemory()


# Function to check if the question is related to Data Science
def is_data_science_related(question):
    prompt = f"Is the following question related to restaurant explanation or food? Respond with only True or False.\n\nQuestion: {question}"
    response = chat_model.invoke([HumanMessage(content=prompt)])
    return response.content.strip().lower() == "true"

if "restaurant_data_added" not in st.session_state:
    st.session_state.restaurant_data_added = False

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, SystemMessage):
        continue
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    emoji = "🧑‍💻" if role == "user" else "🤖"
    st.chat_message(role).write(f"{emoji} {msg.content}")

# Handle user input
user_input = st.chat_input("Welcome to Zomato! How can I help you with restaurants today?")
if not st.session_state.restaurant_data_added and user_input:
    restaurant_data = retrieve_resto_data(user_input)
    system_prompt = generate_system_prompt(restaurant_data)
    st.session_state.messages.append(SystemMessage(content=system_prompt))
    st.session_state.restaurant_data_added = True
                                         
if user_input:
    if is_data_science_related(user_input):
        # Save user message
        st.session_state.messages.append(HumanMessage(content=user_input))
        
        # Get AI response
        response = chat_model.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        
        # Display chat
        st.chat_message("user").write(f"🧑‍💻 {user_input}")
        st.chat_message("assistant").write(f"🤖 {response.content}")
    else:
        st.chat_message("assistant").write("🚫 I can only assist with restaurant-related topics! Try asking about food, dining, or restaurant recommendations. 🍴")