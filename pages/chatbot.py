import streamlit as st
from openai import OpenAI

def main():
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    st.title("💬 Chatbot")
    st.caption("🚀 The Student Whisperer")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Debug statement to confirm the page loads:
    st.write("DEBUG: Chatbot page loaded!")

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Your message:"):
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

if __name__ == '__main__':
    main()
