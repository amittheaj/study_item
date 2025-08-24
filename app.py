import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="JPMC Q&A Bot",
    page_icon="🏦",
    layout="centered"
)

# --- UI Styling ---
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f4f8;
        }
        .st-emotion-cache-16txtl3 {
            padding: 2rem 1rem 1rem;
        }
        h1 {
            color: #005ea6; /* JPMC Blue */
        }
    </style>
""", unsafe_allow_html=True)


# --- Main Application Logic ---

st.title("JPMC Q&A Bot")
st.caption("Your specialized assistant for all things JPMorgan Chase")

# --- Function to call the Gemini API ---
def get_gemini_answer(question):
    """
    Fetches an answer from the Gemini API based on the user's question.
    """
    # System prompt to constrain the LLM
    system_prompt = """You are a specialized Q&A assistant for JPMorgan Chase (JPMC). 
    Your sole purpose is to answer questions related to JPMC's business, history, financials, and operations. 
    If a user asks a question that is NOT about JPMC, you MUST respond with: 
    'I am a JPMC specialist and can only answer questions about JPMorgan Chase. Please ask me something related to the company.' 
    Do not answer any questions about other topics, people, or companies."""
    
    full_prompt = f"{system_prompt}\n\nUser's question: \"{question}\""

    # In Streamlit, API keys should be handled via secrets management, but we'll leave it empty here
    # as the execution environment will handle it.
    api_key = "" 
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=AIzaSyCNQtgHZh6S9loCkFgtFcbzbJ1pD2ADqHo"

    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }]
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an exception for bad status codes
        result = response.json()

        if "candidates" in result and result["candidates"]:
            content_part = result["candidates"][0].get("content", {}).get("parts", [{}])[0]
            return content_part.get("text", "Sorry, I couldn't find an answer.")
        else:
            return "Error: Invalid response structure from the API."

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# --- User Input and Response Display ---

# Use a form to group the input and button
with st.form(key='qa_form'):
    user_question = st.text_input(
        "Ask a question about JPMC:", 
        placeholder="e.g., When was JPMorgan Chase founded?",
        key="question_input"
    )
    submit_button = st.form_submit_button(label='Ask Question')

# Process the question when the form is submitted
if submit_button and user_question:
    with st.spinner('Fetching your answer...'):
        answer = get_gemini_answer(user_question)
        
        # Display the answer in a styled box
        st.markdown(
            f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; background-color: #fafafa; margin-top: 20px;">
                <h3 style="color: #333; margin-bottom: 10px;">Answer:</h3>
                <p style="color: #555;">{answer}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
elif submit_button and not user_question:
    st.warning("Please enter a question.")

