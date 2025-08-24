import streamlit as st
import google.generativeai as genai
import os

# ----------------------
# Setup Gemini API
# ----------------------
# It is best practice to store API keys in environment variables for security.
# Replace this line with your actual API key for local testing,
# or set it as an an environment variable in your deployment environment.
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # Fallback for local testing if not set in env variables
    API_KEY = "AIzaSyCb9UhHRcbIMKPuNWSH-nt34dF0upxeCOY"

genai.configure(api_key=API_KEY)

# Use a specific model that supports chat functionality.
model = genai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat()

# ----------------------
# Streamlit Page Config
# ----------------------
st.set_page_config(page_title="Kadoh AI Chat", page_icon="🤖", layout="wide")

# ----------------------
# Custom CSS Styling
# ----------------------
st.markdown("""
    <style>
    body {
        background-color: black;
        color: white;
    }
    .user-message {
        background-color: #1E3A8A; /* blue */
        padding: 10px;
        border-radius: 12px;
        margin: 5px;
        text-align: right;
        color: white;
        max-width: 70%;
        float: right;
        clear: both;
        word-wrap: break-word;
    }
    .bot-message {
        background-color: #065F46; /* green */
        padding: 10px;
        border-radius: 12px;
        margin: 5px;
        text-align: left;
        color: white;
        max-width: 70%;
        float: left;
        clear: both;
        word-wrap: break-word;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# Initialize session state
# ----------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------
# Chat Display
# ----------------------
st.markdown("<h2 style='text-align:center;'>🤖 Chat with Kadoh AI</h2>", unsafe_allow_html=True)

# Build the entire conversation HTML as a single string
chat_html = ""
for role, msg in st.session_state.history:
    if role == "user":
        chat_html += f"<div class='user-message'>{msg}</div>"
    else:
        chat_html += f"<div class='bot-message'>{msg}</div>"

# Render the messages directly without a container
st.markdown(chat_html, unsafe_allow_html=True)

# ----------------------
# Custom Input at Bottom
# ----------------------
# Use st.chat_input which provides a built-in text input with a send button
# and handles the logic more cleanly.
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.history.append(("user", user_input))

    # Get bot response
    response = chat.send_message(user_input)
    st.session_state.history.append(("bot", response.text))
    
    # Rerun the app to update the chat display with the new messages
    st.rerun()