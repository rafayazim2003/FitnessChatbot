
import openai
import pandas as pd
import streamlit as st

# Access the OpenAI API key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key

# --- Dataset Loading (Adapt this to your actual dataset) ---
def load_exercise_data(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Replace 'cleaned_megaGymDataset.csv' with your actual filename or path to your dataset
exercise_data = load_exercise_data('cleaned_megaGymDataset.csv')

# --- Gather User Preferences ---
def gather_user_preferences():
    goal = st.selectbox(
        "What's your main fitness goal?", 
        ["Weight Loss", "Build Muscle", "Endurance", "General Fitness"]
    )
    experience = st.radio(
        "What's your experience level?",
        ["Beginner", "Intermediate", "Advanced"]
    )
    restrictions = st.text_area(
        "Any injuries or limitations? (Optional)", 
        placeholder="E.g., knee pain, lower back issues, etc."
    )

    return {"goal": goal, "experience": experience, "restrictions": restrictions}

# --- Process User Queries ---
def process_query(query, exercise_data, user_preferences):
    if not user_preferences:
        # Gather preferences if not already done
        user_preferences = gather_user_preferences()

    # Construct the prompt
    prompt = craft_fitness_prompt(query, exercise_data, user_preferences)

    # Call the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use gpt-3.5-turbo if needed
            messages=[
                {"role": "system", "content": "You are a fitness expert."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract and return the response content
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        # Handle OpenAI errors gracefully
        return f"An error occurred while processing your request: {str(e)}"

# --- Helper Functions ---
def craft_fitness_prompt(query, data, user_preferences):
    # Build a detailed prompt for the AI
    goal = user_preferences.get("goal")
    experience = user_preferences.get("experience")
    restrictions = user_preferences.get("restrictions")
    restrictions_text = (
        "no restrictions" if not restrictions else f"the following restrictions: {restrictions}"
    )

    return (
        f"User Query: {query}\n"
        f"User Info: Goal: {goal}, Experience: {experience}, Restrictions: {restrictions_text}.\n"
        f"Exercise Data (sample):\n{data.head(3).to_string(index=False)}\n"
        f"Provide a concise and helpful answer tailored to the user's preferences."
    )

# --- Streamlit UI ---
st.title("Fitness Knowledge Bot")

# Initialize user preferences in session state
if 'user_preferences' not in st.session_state:
    st.session_state['user_preferences'] = gather_user_preferences()

# User input for fitness-related queries
user_input = st.text_input("Ask me about workouts or fitness...")

if st.button("Submit"): 
    # Process the query and display the response
    chatbot_response = process_query(user_input, exercise_data, st.session_state['user_preferences'])
    st.write("Chatbot Response:", chatbot_response)

