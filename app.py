import cohere
import pandas as pd
import streamlit as st

# Access the API key from Streamlit Secrets
cohere_api_key = st.secrets["COHERE_API_KEY"]

# Initialize the Cohere client with the API key
co = cohere.Client(cohere_api_key)

# --- Dataset Loading (Adapt this to your actual dataset) ---
def load_exercise_data(csv_file):
    df = pd.read_csv(csv_file)
    # ... perform any necessary data cleaning or column extraction ...
    return df 

# Replace 'your_data.csv' with the actual filename or path to your dataset
exercise_data = load_exercise_data('megaGymDataset.csv') 

# --- Process User Queries ---
def gather_user_preferences():
    goal = st.selectbox("What's your main fitness goal?", 
                        ["Weight Loss", "Build Muscle", "Endurance", "General Fitness"])
    experience = st.radio("What's your experience level?",
                          ["Beginner", "Intermediate", "Advanced"])
    restrictions = st.checkbox("Any injuries or limitations?")
    # Add more questions here if necessary

    return goal, experience, restrictions

def process_query(query, exercise_data, user_preferences=None):
    if user_preferences is None:
         # First time - Gather preferences
         goal, experience, restrictions = gather_user_preferences()
         return process_query(query, exercise_data, 
                              user_preferences={"goal": goal, 
                                                "experience": experience, 
                                                "restrictions": restrictions})

    # 2. General Workout or Fitness Questions using Cohere
    prompt = craft_fitness_prompt(query, exercise_data)  # Helper function below
    response = co.generate( 
        model='command-nightly',  
        prompt=prompt,   
        stop_sequences=["--"]) 
    return response.generations[0].text

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

def craft_fitness_prompt(query, data):
    # Construct a custom prompt for Cohere to generate a fitness response
    return "User Query: " + query

# --- Streamlit UI ---
st.title("Fitness Knowledge Bot")

# Gather user preferences right at the start
user_preferences = gather_user_preferences() 

# User input for asking fitness-related questions
user_input = st.text_input("Ask me about workouts or fitness...")

if st.button("Submit"): 
    # Process the query and display response
    chatbot_response = process_query(user_input, exercise_data, user_preferences)
    st.write("Chatbot Response:", chatbot_response)
 


