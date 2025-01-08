import openai
import pandas as pd
import streamlit as st

# Access the OpenAI API key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key

# --- Dataset Loading (Adapt this to your actual dataset) ---
def load_exercise_data(csv_file):
    df = pd.read_csv(csv_file)
    # Perform any necessary data cleaning or column extraction
    return df

# Replace 'cleaned_megaGymDataset.csv' with the actual filename or path to your dataset
exercise_data = load_exercise_data('cleaned_megaGymDataset.csv')

# --- Process User Queries ---
def gather_user_preferences():
    goal = st.selectbox("What's your main fitness goal?", 
                        ["Weight Loss", "Build Muscle", "Endurance", "General Fitness"])
    experience = st.radio("What's your experience level?", 
                          ["Beginner", "Intermediate", "Advanced"])
    restrictions = st.checkbox("Any injuries or limitations?")
    # Add more questions here if necessary

    return {"goal": goal, "experience": experience, "restrictions": restrictions}

def process_query(query, exercise_data, user_preferences=None):
    if user_preferences is None:
        # First time - Gather preferences
        user_preferences = gather_user_preferences()
        st.session_state.user_preferences = user_preferences  # Save preferences to session_state
        return process_query(query, exercise_data, user_preferences)

    # General Workout or Fitness Questions using OpenAI
    prompt = craft_fitness_prompt(query, exercise_data, user_preferences)  # Helper function below
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with "gpt-3.5-turbo" if using GPT-3.5
        messages=[{"role": "system", "content": "You are a fitness expert."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# --- Helper Functions ---
def user_asks_about_exercise(query):
    # Simple keyword detection, make this smarter if needed
    return "describe" in query or "how to" in query 

def extract_exercise_name(query):
    # Basic extraction, improve with NLP techniques if necessary
    return query.split("describe ")[1] 

def describe_exercise(exercise, data):
    # Lookup exercise in the dataset and construct a description
    return "Description from dataset here..."  # Modify with actual lookup logic

def craft_fitness_prompt(query, data, user_preferences):
    # Construct a custom prompt for OpenAI to generate a fitness response
    goal = user_preferences.get("goal")
    experience = user_preferences.get("experience")
    restrictions = user_preferences.get("restrictions")
    restrictions_text = "with no restrictions" if not restrictions else f"with the following restrictions: {restrictions}"

    return (
        f"User Query: {query}\n"
        f"User Info: Goal: {goal}, Experience: {experience}, Restrictions: {restrictions_text}.\n"
        f"Exercise Data: {data.head(3).to_string(index=False)}\n"
        f"Provide a concise and helpful answer."
    )

# --- Streamlit UI ---
st.title("Fitness Knowledge Bot")

# Initialize session state if not already present
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = None

# If user preferences haven't been gathered yet, gather them
if st.session_state.user_preferences is None:
    st.session_state.user_preferences = gather_user_preferences()

# User input for asking fitness-related questions
user_input = st.text_input("Ask me about workouts or fitness...")

if st.button("Submit"):
    # Process the query and display response
    chatbot_response = process_query(user_input, exercise_data, st.session_state.user_preferences)
    st.write("Chatbot Response:", chatbot_response)
