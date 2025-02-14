"""The main file of the project."""

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv  
from openai import AzureOpenAI 
load_dotenv()
import os

# Set OpenAI API key 
client = AzureOpenAI(
  azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"],
  api_key = os.environ["AZURE_OPENAI_API_KEY"],  
  api_version="2024-08-01-preview"
)

st.title("💬 Chatbot")
st.caption("🚀 The Student Whisperer")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
