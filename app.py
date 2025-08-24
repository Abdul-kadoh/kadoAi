import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions as google_exceptions
import os

# ----------------------
# Setup Gemini API
# ----------------------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    API_KEY = "AIzaSyC04X6NytrmscDS2aCny12GzcAofrPcb5o"  # ⚠️ Replace with your own for production

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

chat_html = ""
for role, msg in st.session_state.history:
    if role == "user":
        chat_html += f"<div class='user-message'>{msg}</div>"
    else:
        chat_html += f"<div class='bot-message'>{msg}</div>"
st.markdown(chat_html, unsafe_allow_html=True)

# ----------------------
# Chat Input
# ----------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.history.append(("user", user_input))

    try:
        # Only keep last 10 messages to reduce token usage
        trimmed_history = st.session_state.history[-10:]

        # Send only the user input (not full history) to Gemini
        response = chat.send_message(user_input)

        st.session_state.history.append(("bot", response.text))

    except google_exceptions.ResourceExhausted:
        st.session_state.history.append(
            ("bot", "⚠️ API quota exhausted. Please wait a while or upgrade your plan.")
        )

    except Exception as e:
        st.session_state.history.append(
            ("bot", f"⚠️ An unexpected error occurred: {str(e)}")
        )

    st.rerun()
