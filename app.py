import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load local .env for local development
load_dotenv()

# Try Streamlit secrets first, then fall back to local .env
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not api_key:
    st.error("GROQ_API_KEY not found. Add it to Streamlit secrets or your local .env file.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="Basic LLM Chatbot", page_icon="🤖")
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
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a helpful, simple, and clear AI assistant."},
                        *st.session_state.messages
                    ]
                )
                reply = response.choices[0].message.content
                st.write(reply)
            except Exception as e:
                st.error(str(e))
                st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})