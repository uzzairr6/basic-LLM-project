# 

import os
from pathlib import Path

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


st.set_page_config(
    page_title="Basic LLM Chatbot",
    page_icon="🤖"
)

load_dotenv(Path(__file__).parent / ".env")


def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY")


@st.cache_resource
def get_client(api_key):
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )


api_key = get_api_key()

if not api_key:
    st.error("GROQ_API_KEY not found. Add it to your local .env file or Streamlit secrets.")
    st.stop()


client = get_client(api_key)


st.title("🤖 Basic LLM Chatbot")
st.write("Ask me anything. This chatbot uses Groq API with an OpenAI-compatible client.")

if "messages" not in st.session_state:
    st.session_state.messages = []


if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


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
        with st.spinner("Generating response..."):
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