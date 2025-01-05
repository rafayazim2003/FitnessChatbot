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
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

chatbot = load_chatbot()

# Chatbot conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", placeholder="Type your message here...")

# Chatbot interaction
if user_input:
    # Generate a response using the chatbot
    chat_history = [x[1] for x in st.session_state.history]
    chat_history.append(user_input)
    chat_input = " ".join(chat_history)
    
    response = chatbot(chat_input, max_length=1000, num_return_sequences=1)

    # Save conversation history
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response[0]['generated_text']))

# Display chat history
for speaker, message in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**{speaker}:** {message}")
    else:
        st.markdown(f"*{speaker}:* {message}")
