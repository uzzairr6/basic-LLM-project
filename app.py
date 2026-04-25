import os
from pathlib import Path

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


# Page config must be before any st.write, st.title, etc.
st.write("Secrets keys available:", list(st.secrets.keys()))
st.set_page_config(
    page_title="Basic LLM Chatbot",
    page_icon="🤖"
)


# Load .env file from the same folder as app.py
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


# First try local .env
api_key = os.getenv("GROQ_API_KEY")


# Then try Streamlit secrets
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None


# Temporary debug lines
st.write("Looking for .env at:", env_path)
st.write("Local env key found:", bool(os.getenv("GROQ_API_KEY")))

try:
    st.write("Streamlit secret found:", "GROQ_API_KEY" in st.secrets)
except Exception:
    st.write("Streamlit secret found:", False)


if not api_key:
    st.error("GROQ_API_KEY not found. Add it to your local .env file or Streamlit secrets.")
    st.stop()


client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


st.title("🤖 Basic LLM Chatbot")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input("Type your message here...")


if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful, simple, and clear AI assistant."
                        },
                        *st.session_state.messages
                    ]
                )

                reply = response.choices[0].message.content
                st.write(reply)

            except Exception as e:
                st.error(str(e))
                st.stop()

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })