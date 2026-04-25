import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="Basic LLM Chatbot", page_icon="🤖")
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
st.title("🤖 Basic LLM Chatbot")

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