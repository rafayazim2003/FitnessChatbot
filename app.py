import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Title of the app
st.title("Fitness Chatbot 💪")
st.write("Ask me anything about fitness, workouts, or meal plans!")

# Load the chatbot model
@st.cache_resource
def load_chatbot():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return pipeline("conversational", model=model, tokenizer=tokenizer)

chatbot = load_chatbot()

# Chatbot conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", placeholder="Type your message here...")

# Chatbot interaction
if user_input:
    from transformers import Conversation
    conversation = Conversation(user_input)
    result = chatbot(conversation)

    # Save conversation history
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", result.generated_responses[-1]))

# Display chat history
for speaker, message in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**{speaker}:** {message}")
    else:
        st.markdown(f"*{speaker}:* {message}")

