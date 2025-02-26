
import dotenv
from pages.chatbot import OpenAIChatbot
import streamlit as st


if __name__ == "__main__":
    dotenv.load_dotenv()

    st.sidebar.page_link('app.py', label='Chatbot')

    #Hide this later :)
    st.sidebar.page_link('pages/login.py', label='Login')
    st.sidebar.page_link('pages/profile.py', label='Profile')

    chatbot = OpenAIChatbot()
    chatbot.run()
