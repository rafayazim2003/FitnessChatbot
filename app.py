import pandas as pd
import cohere
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables 
load_dotenv()  
cohere_api_key = os.environ["COHERE_API_KEY"]
co = cohere.Client(cohere_api_key)

# --- Dataset Loading ---
def load_exercise_data(csv_file):
    df = pd.read_csv(csv_file)
    # You can clean and process the data as needed here
    return df 

# Load your dataset
exercise_data = load_exercise_data('megaGymDataset.csv') 

# --- Process User Queries ---
def gather_user_preferences():
    goal = st.selectbox("What's your main fitness goal?", 
                        ["Weight Loss", "Build Muscle", "Endurance", "General Fitness"])
    experience = st.radio("What's your experience level?", 
                          ["Beginner", "Intermediate", "Advanced"])
    restrictions = st.checkbox("Any injuries or limitations?")
    # Add more questions here if needed

    return {"goal": goal, "experience": experience, "restrictions": restrictions}

def process_query(query, exercise_data, user_preferences):
    if user_preferences is None:
        # Gather preferences if not already passed in
        user_preferences = gather_user_preferences()
    
    if user_asks_about_exercise(query):
        exercise = extract_exercise_name(query)
        description = describe_exercise(exercise, exercise_data)
        return description
    
    # For other types of fitness queries, use Cohere
    prompt = craft_fitness_prompt(query, exercise_data, user_preferences)  # Create a fitness-focused prompt
    response = co.generate( 
        model='command-nightly',  
        prompt=prompt,   
        stop_sequences=["--"]) 
    return response.generations[0].text

# --- Helper Functions ---
def user_asks_about_exercise(query):
    # Simple keyword detection for exercise-related queries
    return "describe" in query or "how to" in query 

def extract_exercise_name(query):
    # Basic extraction (you may want to improve this with NLP)
    return query.split("describe ")[1] if "describe" in query else ""

def describe_exercise(exercise, data):
    # Look up exercise in your dataset and create a description
    exercise_row = data[data['exercise_name'].str.contains(exercise, case=False, na=False)]
    if not exercise_row.empty:
        return exercise_row.iloc[0]['description']  # Assuming 'description' column contains the details
    else:
        return "Sorry, I couldn't find that exercise."

def craft_fitness_prompt(query, data, user_preferences):
    # You can build a more detailed prompt based on user preferences and the query
    prompt = f"User has the goal of {user_preferences['goal']} and is at {user_preferences['experience']} level. "
    prompt += f"User has the following restrictions: {'Yes' if user_preferences['restrictions'] else 'No'}. "
    prompt += f"User query: {query}"
    return prompt

# --- Streamlit UI ---
st.title("Fitness Knowledge Bot")

# If no preferences are stored in session, gather them
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = gather_user_preferences()

user_input = st.text_input("Ask me about workouts or fitness...")

if st.button("Submit"): 
    # Process query with the stored user preferences
    chatbot_response = process_query(user_input, exercise_data, st.session_state.user_preferences)
    st.write("Chatbot:", chatbot_response)

